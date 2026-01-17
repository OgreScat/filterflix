# FilterFlix - Claude Code Launch Protocol

## Quick Start (Copy/Paste into Claude Code)

```
I'm continuing FilterFlix development. The complete MVP is built:
- Chrome extension in /extension (manifest.json, content.js, popup.html/js, styles.css)
- Timestamp schema + 5 sample movies in /timestamps
- IMDb scraper in /scripts/scrapers
- Landing page in /docs (index.html, contribute.html)

NEXT PRIORITIES:
1. Initialize git repo and push to GitHub
2. Enable GitHub Pages for filterflix.app
3. Test Chrome extension locally on Netflix
4. Use Perplexity MCP to research: "current VidAngel ClearPlay market 2025 competitors"

I have Perplexity MCP configured. You have full system access. Execute autonomously.
```

## Quad-Engine Integration

### Engine 1: Claude Code (Execution)
- Full file system access via DevHQ
- Git operations, testing, deployment
- Code modifications and debugging

### Engine 2: Perplexity Pro (Research via MCP)
When you need research, use the Perplexity MCP tool:
- Market validation queries
- Competitor analysis
- Legal precedent verification
- Technical best practices

### Engine 3: Claude Coworker (Planning/Synthesis)
- Strategic decision making
- Architecture reviews
- User experience optimization

### Engine 4: Grok/X Premium (Social Validation)
For X-based validation, search:
- "#contentfiltering" sentiment
- VidAngel user discussions
- Parent streaming preferences
- Family Movie Act mentions

## Git Setup Commands

```bash
cd /Volumes/DevHQ/FilterFlix
git init
git add .
git commit -m "FilterFlix MVP - Chrome extension + landing page

- Chrome extension with skip/mute/blur filtering
- Netflix, Prime, Disney+, HBO, Hulu support
- Timestamp JSON schema with 5 sample movies
- IMDb Parents Guide scraper (Python)
- Landing page with email capture
- Community contribution system

Family Movie Act 2005 compliant.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Create GitHub repo (requires gh CLI)
gh repo create filterflix --private --source=. --push
```

## GitHub Pages DNS Setup

After pushing to GitHub:

1. Go to repo Settings → Pages
2. Source: Deploy from branch → main → /docs
3. Custom domain: filterflix.app
4. Enforce HTTPS: ✓

DNS Records (at your registrar):
```
Type    Host    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     filterflix.github.io
```

## Chrome Extension Testing

1. Open `chrome://extensions`
2. Enable Developer Mode (top right)
3. Click "Load unpacked"
4. Select the `extension/` folder
5. Navigate to Netflix
6. Demo timestamps trigger at: 0:30, 2:00, 5:00

## Perplexity MCP Research Prompts

Copy these into Claude Code when you need research:

```
Use Perplexity to search: "VidAngel vs Disney lawsuit 2023 2024 outcome"
```

```
Use Perplexity to search: "Chrome extension content filtering streaming 2025"
```

```
Use Perplexity to search: "Family Movie Act 17 USC 110 recent cases"
```

## X/Grok Validation Searches

For social validation via Grok:
- "site:x.com VidAngel users 2024"
- "site:x.com content filtering Netflix parents"
- "site:x.com ClearPlay streaming"

---

*Built during paternity leave. For families who love great stories.*
