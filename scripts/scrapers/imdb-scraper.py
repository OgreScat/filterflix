#!/usr/bin/env python3
"""
FilterFlix IMDb Parents Guide Scraper
Extracts content warnings and estimates timestamps from IMDb

Usage:
    python imdb-scraper.py tt1745960 130  # Top Gun: Maverick, 130 min runtime
    python imdb-scraper.py tt0468569 152  # The Dark Knight, 152 min runtime
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional
import time


class IMDbScraper:
    """Scraper for IMDb Parents Guide content warnings"""

    BASE_URL = "https://www.imdb.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    CATEGORIES = {
        "nudity": ["advisory-nudity", "nudity", "sex"],
        "violence": ["advisory-violence", "violence", "gore"],
        "profanity": ["advisory-profanity", "profanity", "language"],
        "substances": ["advisory-alcohol", "alcohol", "drugs", "smoking"],
        "frightening": ["advisory-frightening", "frightening", "intense"],
    }

    # Patterns for estimating timestamps from scene descriptions
    TIME_PATTERNS = {
        r"opening|beginning|starts?|first\s+scene|intro": 0.05,
        r"early|first\s+\d+\s+minutes?|within.*first": 0.12,
        r"about\s+\d+\s+minutes?\s+in": "extract",  # Special: extract number
        r"quarter|15\s*%|1\/4": 0.25,
        r"mid-?way|middle|halfway|around\s+the\s+middle": 0.50,
        r"3\/4|three.?quarters?|75\s*%": 0.75,
        r"later|toward.*end|near.*end|last\s+third": 0.80,
        r"climax|final|ending|last\s+scene|conclusion": 0.90,
    }

    SEVERITY_KEYWORDS = {
        10: ["extremely graphic", "very explicit", "hardcore"],
        9: ["graphic", "explicit", "disturbing", "brutal", "extreme"],
        8: ["intense", "strong", "bloody", "gory", "harsh"],
        7: ["considerable", "significant", "multiple", "frequent"],
        6: ["moderate", "several", "noticeable"],
        5: ["some", "occasional", "brief but"],
        4: ["mild", "brief", "implied", "suggested"],
        3: ["minimal", "minor", "light"],
        2: ["very brief", "barely", "quick"],
        1: ["none", "no", "absent"],
    }

    def __init__(self, rate_limit: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.rate_limit = rate_limit
        self.last_request = 0

    def _rate_limit_wait(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()

    def scrape_parents_guide(self, imdb_id: str) -> Dict:
        """
        Scrape IMDb Parents Guide for a movie

        Args:
            imdb_id: IMDb ID (e.g., 'tt1745960')

        Returns:
            Dictionary with title and categorized warnings
        """
        self._rate_limit_wait()

        url = f"{self.BASE_URL}/title/{imdb_id}/parentalguide"
        print(f"Fetching: {url}", file=sys.stderr)

        try:
            response = self.session.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return {"imdb_id": imdb_id, "title": None, "warnings": {}, "error": str(e)}

        soup = BeautifulSoup(response.text, "lxml")

        # Get movie title
        title_elem = soup.select_one('h3[itemprop="name"] a, [data-testid="hero-title-block__title"]')
        title = title_elem.get_text(strip=True) if title_elem else None

        # Alternative title extraction
        if not title:
            title_elem = soup.select_one('title')
            if title_elem:
                title = title_elem.get_text().split(' - ')[0].strip()

        result = {
            "imdb_id": imdb_id,
            "title": title,
            "warnings": {},
            "severity_votes": {},
        }

        # Extract warnings for each category
        for category, selectors in self.CATEGORIES.items():
            warnings = []
            for selector in selectors:
                # Try ID-based selection
                section = soup.find(id=selector)
                if section:
                    items = section.find_all("li", class_=lambda c: c and "ipl-zebra-list__item" in c)
                    if not items:
                        items = section.find_all("li")
                    warnings.extend([item.get_text(strip=True) for item in items])

                # Try section header approach
                header = soup.find(string=re.compile(selector, re.I))
                if header:
                    parent = header.find_parent("section") or header.find_parent("div")
                    if parent:
                        items = parent.find_all("li")
                        warnings.extend([item.get_text(strip=True) for item in items])

            # Deduplicate and clean
            seen = set()
            clean_warnings = []
            for w in warnings:
                w_clean = re.sub(r'\s+', ' ', w).strip()
                if w_clean and w_clean not in seen and len(w_clean) > 10:
                    seen.add(w_clean)
                    clean_warnings.append(w_clean)

            result["warnings"][category] = clean_warnings

        return result

    def estimate_timestamp_position(self, description: str, runtime_minutes: int) -> float:
        """
        Estimate the position (0-1) of a scene based on description

        Args:
            description: Scene description text
            runtime_minutes: Movie runtime in minutes

        Returns:
            Estimated position as fraction (0-1) of movie runtime
        """
        desc_lower = description.lower()

        # Check for explicit time mentions (e.g., "about 45 minutes in")
        time_match = re.search(r'(\d+)\s*minutes?\s*(in|into)', desc_lower)
        if time_match:
            minutes = int(time_match.group(1))
            return min(minutes / runtime_minutes, 0.95)

        # Check for pattern matches
        for pattern, position in self.TIME_PATTERNS.items():
            if position == "extract":
                continue
            if re.search(pattern, desc_lower):
                return position

        # Default: middle of movie (with some randomization based on hash)
        hash_offset = (hash(description) % 20 - 10) / 100  # -0.1 to +0.1
        return 0.5 + hash_offset

    def estimate_severity(self, description: str, category: str) -> int:
        """
        Estimate severity (1-10) based on description keywords

        Args:
            description: Scene description
            category: Content category

        Returns:
            Severity rating 1-10
        """
        desc_lower = description.lower()

        # Check for severity keywords (highest to lowest)
        for severity, keywords in sorted(self.SEVERITY_KEYWORDS.items(), reverse=True):
            for keyword in keywords:
                if keyword in desc_lower:
                    return severity

        # Default severities by category
        defaults = {
            "nudity": 6,
            "violence": 6,
            "profanity": 4,
            "substances": 5,
            "frightening": 5,
        }
        return defaults.get(category, 5)

    def generate_timestamps(
        self,
        warnings: Dict[str, List[str]],
        runtime_minutes: int,
        imdb_id: str,
    ) -> List[Dict]:
        """
        Generate timestamp objects from warnings

        Args:
            warnings: Dictionary of category -> list of descriptions
            runtime_minutes: Movie runtime in minutes

        Returns:
            List of timestamp objects
        """
        timestamps = []
        runtime_seconds = runtime_minutes * 60

        for category, descriptions in warnings.items():
            for desc in descriptions:
                # Estimate position
                position = self.estimate_timestamp_position(desc, runtime_minutes)
                start_seconds = int(runtime_seconds * position)

                # Estimate segment duration based on description
                duration = 30  # Default 30 seconds
                if "scene" in desc.lower():
                    duration = 45
                if "sequence" in desc.lower() or "throughout" in desc.lower():
                    duration = 90
                if "brief" in desc.lower() or "quick" in desc.lower():
                    duration = 15

                end_seconds = min(start_seconds + duration, runtime_seconds - 10)

                timestamps.append({
                    "start": self._format_time(start_seconds),
                    "end": self._format_time(end_seconds),
                    "type": category,
                    "severity": self.estimate_severity(desc, category),
                    "description": desc[:300],  # Truncate long descriptions
                    "source": "IMDb Parents Guide - estimated",
                    "verified": False,
                })

        # Sort by start time
        timestamps.sort(key=lambda x: x["start"])

        return timestamps

    def _format_time(self, seconds: int) -> str:
        """Format seconds as HH:MM:SS"""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def process_movie(self, imdb_id: str, runtime_minutes: int) -> Dict:
        """
        Full pipeline: scrape, estimate, and output

        Args:
            imdb_id: IMDb ID
            runtime_minutes: Movie runtime

        Returns:
            Complete FilterFlix timestamp object
        """
        # Scrape
        data = self.scrape_parents_guide(imdb_id)

        if data.get("error"):
            return data

        # Generate timestamps
        timestamps = self.generate_timestamps(
            data["warnings"],
            runtime_minutes,
            imdb_id,
        )

        # Build final output
        return {
            "title": data["title"] or "Unknown",
            "imdb_id": imdb_id,
            "runtime_minutes": runtime_minutes,
            "platforms": [],  # To be filled manually
            "timestamps": timestamps,
            "metadata": {
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "contributors": ["FilterFlix Auto-Scraper"],
                "confidence_score": 0.5,
                "source": "IMDb Parents Guide",
                "needs_verification": True,
                "version": 1,
            },
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python imdb-scraper.py <imdb_id> <runtime_minutes>")
        print("Example: python imdb-scraper.py tt1745960 130")
        sys.exit(1)

    imdb_id = sys.argv[1]
    runtime = int(sys.argv[2])

    # Validate IMDb ID format
    if not re.match(r'^tt\d+$', imdb_id):
        print(f"Error: Invalid IMDb ID format: {imdb_id}", file=sys.stderr)
        print("Expected format: tt followed by numbers (e.g., tt1745960)", file=sys.stderr)
        sys.exit(1)

    scraper = IMDbScraper()
    result = scraper.process_movie(imdb_id, runtime)

    # Output JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
