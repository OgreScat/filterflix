#!/usr/bin/env python3
"""
FilterFlix Timestamp Aggregator
Combines data from multiple sources and calculates confidence scores

Usage:
    python aggregate-timestamps.py --imdb tt1745960 --runtime 130 --output top-gun.json
    python aggregate-timestamps.py --batch movies.txt --output-dir ./timestamps/
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional
import hashlib


def merge_timestamps(sources: List[Dict]) -> Dict:
    """
    Merge timestamps from multiple sources

    Args:
        sources: List of timestamp data objects from different sources

    Returns:
        Merged timestamp object with confidence scores
    """
    if not sources:
        return None

    # Use first source as base
    merged = {
        "title": sources[0].get("title", "Unknown"),
        "imdb_id": sources[0].get("imdb_id", ""),
        "runtime_minutes": sources[0].get("runtime_minutes", 0),
        "platforms": [],
        "timestamps": [],
        "metadata": {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "sources": [],
            "confidence_score": 0.0,
            "version": 1,
        },
    }

    # Collect all platforms
    platforms = set()
    for source in sources:
        platforms.update(source.get("platforms", []))
        if source.get("metadata", {}).get("source"):
            merged["metadata"]["sources"].append(source["metadata"]["source"])
    merged["platforms"] = list(platforms)

    # Collect all timestamps with source tracking
    all_timestamps = []
    for source_idx, source in enumerate(sources):
        source_name = source.get("metadata", {}).get("source", f"Source {source_idx}")
        for ts in source.get("timestamps", []):
            ts_copy = ts.copy()
            ts_copy["_source"] = source_name
            ts_copy["_source_idx"] = source_idx
            all_timestamps.append(ts_copy)

    # Group similar timestamps (within 30 seconds of each other)
    grouped = group_similar_timestamps(all_timestamps)

    # Merge each group
    for group in grouped:
        merged_ts = merge_timestamp_group(group)
        merged["timestamps"].append(merged_ts)

    # Sort by start time
    merged["timestamps"].sort(key=lambda x: x["start"])

    # Calculate overall confidence
    if merged["timestamps"]:
        avg_confidence = sum(ts.get("confidence", 0.5) for ts in merged["timestamps"]) / len(merged["timestamps"])
        merged["metadata"]["confidence_score"] = round(avg_confidence, 2)

    return merged


def group_similar_timestamps(timestamps: List[Dict], threshold_seconds: int = 30) -> List[List[Dict]]:
    """
    Group timestamps that refer to the same scene (within threshold)

    Args:
        timestamps: List of timestamp objects
        threshold_seconds: Time window for grouping

    Returns:
        List of groups, each group is a list of related timestamps
    """
    if not timestamps:
        return []

    # Parse all start times
    def parse_time(ts):
        start = ts.get("start", "00:00:00")
        parts = start.split(":")
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    # Sort by start time
    sorted_ts = sorted(timestamps, key=parse_time)

    groups = []
    current_group = [sorted_ts[0]]
    current_time = parse_time(sorted_ts[0])

    for ts in sorted_ts[1:]:
        ts_time = parse_time(ts)

        # Check if same category and within threshold
        if (ts_time - current_time <= threshold_seconds and
            ts.get("type") == current_group[0].get("type")):
            current_group.append(ts)
        else:
            groups.append(current_group)
            current_group = [ts]
            current_time = ts_time

    groups.append(current_group)

    return groups


def merge_timestamp_group(group: List[Dict]) -> Dict:
    """
    Merge a group of similar timestamps into one

    Args:
        group: List of related timestamp objects

    Returns:
        Single merged timestamp with confidence score
    """
    if len(group) == 1:
        ts = group[0].copy()
        ts.pop("_source", None)
        ts.pop("_source_idx", None)
        ts["confidence"] = 0.5
        ts["sources_count"] = 1
        return ts

    # Multiple sources agree - higher confidence
    sources = set(ts.get("_source", "Unknown") for ts in group)

    # Average the times
    def parse_time(start):
        parts = start.split(":")
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    def format_time(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    avg_start = sum(parse_time(ts["start"]) for ts in group) // len(group)
    avg_end = sum(parse_time(ts["end"]) for ts in group) // len(group)
    avg_severity = sum(ts.get("severity", 5) for ts in group) // len(group)

    # Combine descriptions
    descriptions = list(set(ts.get("description", "")[:100] for ts in group))
    combined_desc = " | ".join(descriptions[:3])

    # Calculate confidence based on number of sources agreeing
    confidence = min(0.5 + (len(sources) * 0.15), 0.95)

    return {
        "start": format_time(avg_start),
        "end": format_time(avg_end),
        "type": group[0].get("type", "unknown"),
        "severity": avg_severity,
        "description": combined_desc,
        "verified": len(sources) >= 3,
        "confidence": round(confidence, 2),
        "sources_count": len(sources),
        "sources": list(sources),
    }


def calculate_quality_score(timestamp_data: Dict) -> float:
    """
    Calculate overall quality score for a timestamp file

    Factors:
    - Number of timestamps
    - Variety of types
    - Confidence scores
    - Verification status
    """
    timestamps = timestamp_data.get("timestamps", [])

    if not timestamps:
        return 0.0

    score = 0.0

    # Coverage (more timestamps = more thorough)
    coverage_score = min(len(timestamps) / 20, 1.0) * 0.3
    score += coverage_score

    # Type variety
    types = set(ts.get("type") for ts in timestamps)
    variety_score = len(types) / 5 * 0.2
    score += variety_score

    # Average confidence
    avg_confidence = sum(ts.get("confidence", 0.5) for ts in timestamps) / len(timestamps)
    score += avg_confidence * 0.3

    # Verification rate
    verified = sum(1 for ts in timestamps if ts.get("verified"))
    verification_score = verified / len(timestamps) * 0.2
    score += verification_score

    return round(score, 2)


def main():
    parser = argparse.ArgumentParser(description="Aggregate timestamps from multiple sources")
    parser.add_argument("--imdb", help="IMDb ID to process")
    parser.add_argument("--runtime", type=int, help="Runtime in minutes")
    parser.add_argument("--sources", nargs="+", help="Source JSON files to merge")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--batch", help="Batch file with list of movies")
    parser.add_argument("--output-dir", help="Output directory for batch processing")

    args = parser.parse_args()

    if args.sources:
        # Merge provided source files
        sources = []
        for source_path in args.sources:
            if os.path.exists(source_path):
                with open(source_path) as f:
                    sources.append(json.load(f))

        merged = merge_timestamps(sources)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(merged, f, indent=2)
        else:
            print(json.dumps(merged, indent=2))

    else:
        print("Usage examples:")
        print("  Merge multiple sources:")
        print("    python aggregate-timestamps.py --sources imdb.json reddit.json --output merged.json")
        print("")
        print("  Batch process:")
        print("    python aggregate-timestamps.py --batch movies.txt --output-dir ./timestamps/")


if __name__ == "__main__":
    main()
