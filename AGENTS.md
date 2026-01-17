# FilterFlix Multi-Agent Orchestration Guide

## The Quad Engine

```
┌─────────────────────────────────────────────────────────────────┐
│                     FILTERFLIX COMMAND CENTER                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │   CLAUDE     │◄──►│   CLAUDE     │◄──►│  PERPLEXITY  │     │
│   │   COWORKER   │    │    CODE      │    │     PRO      │     │
│   │  (Planning)  │    │ (Execution)  │    │  (Research)  │     │
│   └──────────────┘    └──────────────┘    └──────────────┘     │
│          │                   │                   │              │
│          └───────────────────┼───────────────────┘              │
│                              │                                  │
│                    ┌─────────▼─────────┐                        │
│                    │    GROK / X       │                        │
│                    │   (Validation)    │                        │
│                    └───────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Engine Responsibilities

### 1. Claude Coworker (This Session)
**Role:** Strategic Planning & Synthesis

- High-level architecture decisions
- User experience optimization
- Cross-engine coordination
- Documentation and guides
- Complex multi-file generation

**Triggers:** Planning sessions, architecture reviews, documentation needs

### 2. Claude Code
**Role:** Autonomous Execution

- File system operations
- Git commands and GitHub integration
- Package installation and testing
- Code debugging and iteration
- Terminal-based workflows

**Triggers:** "Execute", "Run", "Deploy", "Test", "Build"

### 3. Perplexity Pro (via MCP)
**Role:** Real-Time Research

- Market intelligence
- Competitor analysis
- Legal/compliance verification
- Technical best practices
- Current event context

**Triggers:** "Research", "Verify", "What's current", "Find examples"

### 4. Grok / X Premium
**Role:** Social Validation

- Community sentiment analysis
- User pain point discovery
- Competitor user feedback
- Trend identification
- Real-world use cases

**Triggers:** "Validate with X", "What are people saying", "Social proof"

---

## Workflow Patterns

### Pattern A: Research → Plan → Execute

```
1. [Perplexity] Research current market state
2. [Coworker] Synthesize findings into strategy
3. [X/Grok] Validate approach with social data
4. [Code] Execute implementation
```

### Pattern B: Build → Validate → Iterate

```
1. [Code] Build feature or component
2. [Perplexity] Check against best practices
3. [X/Grok] Gauge user interest/feedback
4. [Coworker] Plan iteration based on data
5. [Code] Implement changes
```

### Pattern C: Issue → Research → Resolve

```
1. [Code] Encounter error or blocker
2. [Perplexity] Research solutions
3. [Coworker] Evaluate options
4. [Code] Implement fix
```

---

## Claude Code Integration Commands

### Initialize Project on DevHQ

```bash
# Copy FilterFlix to your Mac
# In Claude Code, run:
mkdir -p /Volumes/DevHQ/FilterFlix
cp -r ~/Downloads/FilterFlix/* /Volumes/DevHQ/FilterFlix/
cd /Volumes/DevHQ/FilterFlix
git init
```

### Using Perplexity MCP

When you need research in Claude Code:
```
Use the Perplexity tool to search: "your query here"
```

The MCP server handles authentication automatically.

### Git Workflow

```bash
# Daily development
git add -A
git commit -m "Description of changes

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push

# Feature branch workflow
git checkout -b feature/timestamp-api
# ... make changes ...
git commit -m "Add timestamp API endpoint"
git push -u origin feature/timestamp-api
```

---

## X/Grok Research Queries

### Market Validation
- "VidAngel users 2024 2025 reviews"
- "ClearPlay streaming service opinions"
- "content filtering Netflix parents"
- "Family Movie Act streaming"

### Competitor Intelligence
- "VidAngel vs Disney lawsuit outcome"
- "streaming content filter alternatives"
- "parental controls Netflix limitations"

### Feature Ideas
- "what scenes do parents skip in movies"
- "content warnings streaming wishlist"
- "skip scene button Netflix request"

---

## Key Decision Framework

When facing a decision point:

1. **Is it a coding/execution task?** → Claude Code
2. **Need current market/technical info?** → Perplexity Pro
3. **Need real user validation?** → Grok/X
4. **Need strategic synthesis?** → Claude Coworker

---

## Priority Stack (Paternity Leave Context)

Given fragmented time windows:

1. **Highest ROI:** Automated workflows (scrapers, CI/CD)
2. **Medium ROI:** Community contribution system
3. **Lower ROI:** Manual content creation

Focus on building systems that work while you're with the kids.

---

## Emergency Protocols

### If Extension Breaks
```
Claude Code: Check console errors in chrome://extensions
Perplexity: Search specific error message
Code: Fix and test
```

### If Legal Question Arises
```
Perplexity: Research Family Movie Act precedents
X/Grok: Check for similar concerns from VidAngel users
Coworker: Synthesize and advise
```

### If Deployment Fails
```
Code: Check GitHub Actions logs
Perplexity: Research error pattern
Code: Implement fix
```

---

*For families who love great stories.*
