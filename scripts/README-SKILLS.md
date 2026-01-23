# Skills Catalog Quick Reference

## Quick Commands

```bash
# List all 160+ skills
python claude-skills-catalog.py list | head -20

# Search for skills
python claude-skills-catalog.py search react
python claude-skills-catalog.py search marketing
python claude-skills-catalog.py search testing

# Get recommendations for FilterFlix development
python claude-skills-catalog.py recommend extension_development
python claude-skills-catalog.py recommend marketing_launch
python claude-skills-catalog.py recommend backend_api
python claude-skills-catalog.py recommend automation

# Generate install script
python claude-skills-catalog.py bulk-install marketing_launch
chmod +x install-marketing_launch-skills.sh
./install-marketing_launch-skills.sh

# Browse by publisher
python claude-skills-catalog.py publisher anthropics
python claude-skills-catalog.py publisher coreyhaines31

# View tree structure
python claude-skills-catalog.py tree
```

## Python API

```python
from claude_skills_catalog import (
    skills,                         # All 160+ skills
    get_skills_by_category,         # Filter by category
    get_skills_by_publisher,        # Filter by publisher
    get_filterflix_recommendations, # FilterFlix-specific
    search_skills,                  # Keyword search
    generate_install_command,       # Generate npx command
    generate_bulk_install_script,   # Generate shell script
)

# Example: Install all frontend skills
frontend = get_skills_by_category('frontend', 'react')
for skill in frontend:
    print(generate_install_command(skill))

# Example: Get marketing recommendations
marketing = get_filterflix_recommendations('marketing_launch')
generate_bulk_install_script(marketing, 'install-marketing.sh')
```

## FilterFlix Recommendation Categories

1. **extension_development** - Chrome extension development skills
2. **marketing_launch** - Product launch and SEO skills
3. **backend_api** - API and database development skills
4. **documentation** - Docs and presentation creation
5. **automation** - CI/CD and workflow automation

## Available Skill Categories

- `frontend` - React, Vue, web design, UI/UX
- `backend` - APIs, databases, Node.js
- `mobile` - React Native, Expo, native dev
- `testing` - Unit, E2E, QA
- `marketing` - SEO, copywriting, CRO, ads
- `design` - UI/UX, design systems
- `devops` - CI/CD, deployment
- `documentation` - PDF, presentations
- `architecture` - System design, patterns
- `authentication` - Auth implementation
- `productivity` - Planning, debugging
- `communication` - Writing, feedback
- `content` - Articles, images, graphics
- `workflow` - Git, agents, tooling

## Popular Publishers

- **anthropics** - Official Claude skills
- **coreyhaines31** - Marketing skills (15+)
- **obra** - Development superpowers
- **softaworks** - Professional toolkit
- **vercel-labs** - Frontend best practices
- **expo** - React Native ecosystem
- **wshobson** - Advanced patterns (20+)

---

Full documentation: [/docs/SKILLS_CATALOG.md](../docs/SKILLS_CATALOG.md)
