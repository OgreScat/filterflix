# Claude Code Skills Catalog

A comprehensive catalog of 160+ popular skills from skills.sh (extracted January 2026), organized and categorized for FilterFlix development.

## What are Skills?

Skills are specialized capabilities you can add to Claude Code to enhance its expertise in specific areas like frontend development, marketing, testing, and more. Each skill provides best practices, patterns, and domain-specific knowledge.

## Quick Start

### Basic Usage

```python
# Import the catalog
from scripts.claude_skills_catalog import (
    skills,
    get_skills_by_category,
    get_filterflix_recommendations,
    generate_install_command
)

# List all 160+ skills
print(f"Total skills available: {len(skills)}")

# Get skills for frontend development
frontend_skills = get_skills_by_category('frontend', 'react')
print(frontend_skills)

# Get FilterFlix-specific recommendations
recommended = get_filterflix_recommendations('extension_development')
for skill in recommended:
    print(generate_install_command(skill))
```

### Command Line Interface

```bash
# View all available commands
python scripts/claude-skills-catalog.py

# List all skills
python scripts/claude-skills-catalog.py list

# Search for specific skills
python scripts/claude-skills-catalog.py search testing
python scripts/claude-skills-catalog.py search marketing

# Browse by category
python scripts/claude-skills-catalog.py category frontend
python scripts/claude-skills-catalog.py category devops

# Browse by publisher
python scripts/claude-skills-catalog.py publisher anthropics
python scripts/claude-skills-catalog.py publisher vercel-labs

# View as tree structure
python scripts/claude-skills-catalog.py tree

# Get FilterFlix recommendations
python scripts/claude-skills-catalog.py recommend
python scripts/claude-skills-catalog.py recommend extension_development

# Generate install command
python scripts/claude-skills-catalog.py install anthropics/skills/frontend-design

# Generate bulk install script
python scripts/claude-skills-catalog.py bulk-install marketing_launch
./install-marketing_launch-skills.sh
```

## FilterFlix Recommendations

We've curated skill sets specifically for FilterFlix development phases:

### Extension Development
Essential skills for building and improving the Chrome extension:
- `anthropics/skills/frontend-design` - Frontend design patterns
- `vercel-labs/agent-skills/web-design-guidelines` - Web design best practices
- `anthropics/skills/webapp-testing` - Web app testing strategies
- `wshobson/agents/web-component-design` - Web component patterns
- `wshobson/agents/code-review-excellence` - Code review standards

### Marketing & Launch
Skills for product marketing and growth:
- `coreyhaines31/marketingskills/seo-audit` - SEO optimization
- `coreyhaines31/marketingskills/copywriting` - Marketing copy
- `coreyhaines31/marketingskills/launch-strategy` - Product launch planning
- `coreyhaines31/marketingskills/social-content` - Social media content
- `coreyhaines31/marketingskills/page-cro` - Conversion rate optimization
- `coreyhaines31/marketingskills/schema-markup` - Schema.org markup

### Backend API
Skills for building the timestamp API and database:
- `wshobson/agents/api-design-principles` - RESTful API design
- `wshobson/agents/nodejs-backend-patterns` - Node.js backend patterns
- `supabase/agent-skills/supabase-postgres-best-practices` - Supabase/Postgres
- `wshobson/agents/postgresql-table-design` - Database design

### Documentation
Skills for creating docs, presentations, and reports:
- `anthropics/skills/pdf` - PDF generation
- `anthropics/skills/pptx` - PowerPoint presentations
- `softaworks/agent-toolkit/crafting-effective-readmes` - README writing
- `anthropics/skills/doc-coauthoring` - Document collaboration

### Automation & CI/CD
Skills for automating workflows:
- `expo/skills/expo-cicd-workflows` - CI/CD pipelines
- `wshobson/agents/github-actions-templates` - GitHub Actions
- `softaworks/agent-toolkit/dependency-updater` - Dependency management
- `obra/superpowers/test-driven-development` - TDD practices

## Skill Categories

The catalog organizes skills into these categories:

- **Frontend** (40+ skills): React, Vue, Tailwind, UI/UX, web components
- **Backend** (15+ skills): APIs, databases, Node.js, FastAPI
- **Mobile** (10+ skills): React Native, Expo, native development
- **Testing** (8+ skills): Unit testing, E2E, QA planning
- **Marketing** (25+ skills): SEO, copywriting, CRO, analytics, social media
- **Design** (12+ skills): UI/UX, design systems, visual design
- **DevOps** (6+ skills): CI/CD, deployment, GitHub Actions
- **Documentation** (8+ skills): PDF, PowerPoint, Excel, Word
- **Architecture** (5+ skills): System design, patterns, C4 diagrams
- **Authentication** (3+ skills): Auth implementation and best practices
- **Productivity** (10+ skills): Planning, debugging, code review
- **Communication** (5+ skills): Writing, feedback, professional comms
- **Content** (8+ skills): Articles, infographics, images
- **Workflow** (15+ skills): Agent superpowers, tooling, Git workflows

## Top Publishers

### Anthropics
Official Claude skills covering core capabilities:
- `frontend-design`, `webapp-testing`, `pdf`, `pptx`, `xlsx`, `docx`
- `skill-creator`, `mcp-builder`, `canvas-design`, `theme-factory`
- `web-artifacts-builder`, `algorithmic-art`, `brand-guidelines`

### Corey Haines (marketingskills)
Comprehensive marketing and growth skills:
- SEO, copywriting, CRO, analytics, social media, paid ads
- Launch strategy, pricing, onboarding, email sequences
- 15+ specialized marketing skills

### Obra (superpowers)
Development workflow superpowers:
- `test-driven-development`, `systematic-debugging`, `brainstorming`
- `writing-plans`, `executing-plans`, `verification-before-completion`
- `subagent-driven-development`, `dispatching-parallel-agents`
- Git workflows and code review skills

### Softaworks (agent-toolkit)
Professional development and communication:
- Documentation, meetings, session handoff, commit workflows
- Diagrams (Mermaid, C4), communication, feedback
- QA planning, dependency management, domain brainstorming

### Vercel Labs
Frontend and web development:
- `vercel-react-best-practices`, `web-design-guidelines`
- `agent-browser` for web automation

### Expo
React Native and mobile development:
- Full Expo development workflow skills
- Deployment, CI/CD, Tailwind setup, API routes

### wshobson (agents)
Advanced development patterns:
- API design, TypeScript, PostgreSQL, architecture
- Testing patterns, GitHub Actions, responsive design
- 20+ technical skills covering full-stack development

## Installation Examples

### Install a Single Skill

```bash
npx skills add anthropics/skills/frontend-design
```

### Install FilterFlix Recommended Set

```python
from scripts.claude_skills_catalog import (
    get_filterflix_recommendations,
    generate_bulk_install_script
)

# Generate installation script for extension development
recommendations = get_filterflix_recommendations('extension_development')
generate_bulk_install_script(recommendations, 'install-dev-skills.sh')

# Run the script
# ./install-dev-skills.sh
```

### Install All Marketing Skills

```bash
# Using the CLI
python scripts/claude-skills-catalog.py bulk-install marketing_launch

# This creates: install-marketing_launch-skills.sh
# Then run it:
./install-marketing_launch-skills.sh
```

## Search and Discovery

### By Keyword

```python
from scripts.claude_skills_catalog import search_skills

# Find testing-related skills
testing_skills = search_skills('testing')

# Find design skills
design_skills = search_skills('design')

# Find CRO skills
cro_skills = search_skills('cro')
```

### By Publisher

```python
from scripts.claude_skills_catalog import get_skills_by_publisher

# Get all Anthropic official skills
anthropic_skills = get_skills_by_publisher('anthropics')

# Get all marketing skills from Corey Haines
marketing_skills = get_skills_by_publisher('coreyhaines31')
```

### By Category

```python
from scripts.claude_skills_catalog import get_skills_by_category

# Frontend development
frontend = get_skills_by_category('frontend')

# Backend development
backend = get_skills_by_category('backend', 'api', 'database')

# DevOps and automation
devops = get_skills_by_category('devops', 'cicd')
```

## Use Cases for FilterFlix

### Phase 1: Extension MVP
Focus on frontend, testing, and web design skills to polish the Chrome extension.

```bash
python scripts/claude-skills-catalog.py recommend extension_development
```

### Phase 2: Marketing Launch
Prepare landing page, SEO, and launch materials.

```bash
python scripts/claude-skills-catalog.py recommend marketing_launch
```

### Phase 3: Backend API
Build timestamp submission and verification API.

```bash
python scripts/claude-skills-catalog.py recommend backend_api
```

### Phase 4: Automation
Automate timestamp scraping, testing, and deployment.

```bash
python scripts/claude-skills-catalog.py recommend automation
```

## Contributing

This catalog was extracted from skills.sh in January 2026. To update:

1. Visit [skills.sh](https://skills.sh) leaderboard
2. Extract trending and top-rated skills
3. Update `skills` list in `claude-skills-catalog.py`
4. Update category mappings if new skill types emerge

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Multi-agent orchestration guide
- [README.md](../README.md) - FilterFlix project overview
- [CLAUDE_CODE_LAUNCH.md](../CLAUDE_CODE_LAUNCH.md) - Claude Code setup

---

*For families who love great stories.*
