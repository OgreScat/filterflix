# FilterFlix - Smart Content Filtering for Streaming

> Skip, mute, or blur unwanted scenes on Netflix, Prime Video, Disney+, HBO Max, and Hulu.

## 🎯 What is FilterFlix?

FilterFlix is a Chrome extension that lets you filter content on streaming platforms. Uses community-curated timestamps to automatically skip, mute, or blur scenes based on your preferences.

**Family Movie Act 2005 Compliant** - Legal content filtering for private home viewing.

## 📁 Project Structure

```
FilterFlix/
├── extension/           # Chrome extension source
│   ├── manifest.json    # Extension manifest (Manifest V3)
│   ├── content.js       # Content script (filtering logic)
│   ├── popup.html       # Settings popup UI
│   ├── popup.js         # Popup logic
│   └── styles.css       # Injected styles
│
├── timestamps/          # Timestamp data
│   ├── schema.json      # JSON schema for validation
│   └── sample-movies/   # Sample timestamp files
│
├── scripts/             # Utility scripts
│   ├── timestamp-tools.js    # Timestamp utilities
│   └── scrapers/             # Data acquisition scripts
│       ├── imdb-scraper.py   # IMDb Parents Guide scraper
│       └── aggregate-timestamps.py
│
└── docs/                # Landing page (GitHub Pages)
    ├── index.html       # Main landing page
    ├── contribute.html  # Timestamp submission form
    ├── CNAME           # Custom domain config
    └── robots.txt
```

## 🚀 Quick Start

### Load Extension in Chrome (Developer Mode)

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Navigate to Netflix and start watching!

### Test Filtering

The extension includes demo timestamps that will trigger at:
- 00:00:30 (profanity test)
- 00:02:00 (violence test)
- 00:05:00 (nudity test)

## ⚙️ Configuration

Click the FilterFlix icon in Chrome toolbar to access settings:

- **Enable/Disable** - Master toggle
- **Filter Mode** - Skip / Mute / Blur
- **Content Types** - Nudity, Profanity, Violence
- **Severity Threshold** - 1 (filter everything) to 10 (only extreme)

## 📊 Timestamp Format

```json
{
  "title": "Movie Title",
  "imdb_id": "tt1234567",
  "runtime_minutes": 120,
  "platforms": ["netflix", "prime"],
  "timestamps": [
    {
      "start": "00:23:45",
      "end": "00:24:30",
      "type": "nudity",
      "severity": 7,
      "description": "Brief nudity in bedroom scene",
      "verified": false
    }
  ]
}
```

## 🔧 Development

### Prerequisites

- Chrome browser
- Python 3.9+ (for scrapers)
- Node.js (optional, for development)

### Run IMDb Scraper

```bash
cd scripts/scrapers
pip install requests beautifulsoup4 lxml
python imdb-scraper.py tt1745960 130  # Top Gun: Maverick
```

### Deploy Landing Page

Landing page is served via GitHub Pages from the `docs/` folder.

```bash
git add docs/
git commit -m "Update landing page"
git push
```

## 🤝 Contributing

### Submit Timestamps

1. Visit [filterflix.app/contribute.html](https://filterflix.app/contribute.html)
2. Fill in the timestamp form
3. Earn credits for verified submissions!

### Credit System

| Action | Credits |
|--------|---------|
| Submit timestamp | +10 |
| Timestamp verified | +20 bonus |
| Verify others' timestamps | +2 |
| **100 credits** | **= 1 month free** |

## 📜 Legal

FilterFlix operates under the **Family Movie Act of 2005** (17 USC § 110(11)), which permits technology that enables private home viewing with filtering of objectionable content.

- ✅ Works with your own streaming subscriptions
- ✅ No copying or redistribution of content
- ✅ User-controlled filtering preferences
- ✅ Private home viewing only

## 🗺️ Roadmap

- [x] Chrome extension MVP
- [x] Netflix support
- [x] Basic timestamp format
- [ ] Prime Video optimization
- [ ] Disney+ optimization
- [ ] Community contribution portal
- [ ] Mobile app (future)
- [ ] Firefox extension (future)

## 📧 Contact

- Website: [filterflix.app](https://filterflix.app)
- Email: support@filterflix.app
- Domain owned: ✅

## 📄 License

Copyright © 2025 FilterFlix. All rights reserved.

---

*Built during paternity leave. For families who love great stories.*
