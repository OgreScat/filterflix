#!/usr/bin/env python3
"""
Claude Code Skills Catalog (Extracted January 2026)
====================================================

A comprehensive collection of popular skills from skills.sh, organized for easy reference
and integration with FilterFlix development workflows.

Usage:
    from claude_skills_catalog import skills, get_skills_by_category, install_skill

    # List all skills
    for skill in skills:
        print(skill)

    # Get specific categories
    frontend_skills = get_skills_by_category('frontend', 'react', 'ui')
    marketing_skills = get_skills_by_category('marketing', 'seo')

    # Generate install commands
    install_skill('anthropics/skills/frontend-design')
"""

# Full catalog of skills from skills.sh (January 2026)
skills = [
    "vercel-labs/agent-skills/vercel-react-best-practices",
    "vercel-labs/agent-skills/web-design-guidelines",
    "remotion-dev/skills/remotion-best-practices",
    "anthropics/skills/frontend-design",
    "anthropics/skills/skill-creator",
    "expo/skills/building-native-ui",
    "vercel-labs/agent-browser/agent-browser",
    "expo/skills/upgrading-expo",
    "better-auth/skills/better-auth-best-practices",
    "expo/skills/native-data-fetching",
    "coreyhaines31/marketingskills/seo-audit",
    "expo/skills/expo-dev-client",
    "expo/skills/expo-deployment",
    "squirrelscan/skills/audit-website",
    "expo/skills/expo-api-routes",
    "coreyhaines31/marketingskills/copywriting",
    "expo/skills/expo-tailwind-setup",
    "expo/skills/expo-cicd-workflows",
    "expo/skills/use-dom",
    "callstackincubator/agent-skills/react-native-best-practices",
    "coreyhaines31/marketingskills/marketing-psychology",
    "coreyhaines31/marketingskills/programmatic-seo",
    "anthropics/skills/pdf",
    "coreyhaines31/marketingskills/marketing-ideas",
    "hyf0/vue-skills/vue-best-practices",
    "coreyhaines31/marketingskills/pricing-strategy",
    "supabase/agent-skills/supabase-postgres-best-practices",
    "coreyhaines31/marketingskills/social-content",
    "coreyhaines31/marketingskills/copy-editing",
    "better-auth/skills/create-auth-skill",
    "anthropics/skills/pptx",
    "coreyhaines31/marketingskills/launch-strategy",
    "anthropics/skills/xlsx",
    "obra/superpowers/brainstorming",
    "coreyhaines31/marketingskills/page-cro",
    "coreyhaines31/marketingskills/analytics-tracking",
    "coreyhaines31/marketingskills/competitor-alternatives",
    "anthropics/skills/docx",
    "coreyhaines31/marketingskills/onboarding-cro",
    "jimliu/baoyu-skills/baoyu-slide-deck",
    "coreyhaines31/marketingskills/schema-markup",
    "coreyhaines31/marketingskills/email-sequence",
    "jimliu/baoyu-skills/baoyu-article-illustrator",
    "coreyhaines31/marketingskills/paid-ads",
    "coreyhaines31/marketingskills/signup-flow-cro",
    "coreyhaines31/marketingskills/free-tool-strategy",
    "coreyhaines31/marketingskills/paywall-upgrade-cro",
    "coreyhaines31/marketingskills/form-cro",
    "coreyhaines31/marketingskills/referral-program",
    "anthropics/skills/webapp-testing",
    "coreyhaines31/marketingskills/popup-cro",
    "jimliu/baoyu-skills/baoyu-cover-image",
    "coreyhaines31/marketingskills/ab-test-setup",
    "nextlevelbuilder/ui-ux-pro-max-skill/ui-ux-pro-max",
    "jimliu/baoyu-skills/baoyu-xhs-images",
    "anthropics/skills/mcp-builder",
    "jimliu/baoyu-skills/baoyu-comic",
    "obra/superpowers/test-driven-development",
    "anthropics/skills/canvas-design",
    "jimliu/baoyu-skills/baoyu-post-to-wechat",
    "obra/superpowers/systematic-debugging",
    "jimliu/baoyu-skills/baoyu-post-to-x",
    "anthropics/skills/doc-coauthoring",
    "obra/superpowers/writing-plans",
    "obra/superpowers/executing-plans",
    "softaworks/agent-toolkit/daily-meeting-update",
    "softaworks/agent-toolkit/agent-md-refactor",
    "softaworks/agent-toolkit/session-handoff",
    "softaworks/agent-toolkit/commit-work",
    "softaworks/agent-toolkit/codex",
    "softaworks/agent-toolkit/gemini",
    "softaworks/agent-toolkit/qa-test-planner",
    "softaworks/agent-toolkit/meme-factory",
    "softaworks/agent-toolkit/dependency-updater",
    "softaworks/agent-toolkit/domain-name-brainstormer",
    "softaworks/agent-toolkit/gepetto",
    "softaworks/agent-toolkit/mermaid-diagrams",
    "softaworks/agent-toolkit/writing-clearly-and-concisely",
    "anthropics/skills/theme-factory",
    "softaworks/agent-toolkit/reducing-entropy",
    "softaworks/agent-toolkit/feedback-mastery",
    "softaworks/agent-toolkit/marp-slide",
    "softaworks/agent-toolkit/difficult-workplace-conversations",
    "softaworks/agent-toolkit/skill-judge",
    "softaworks/agent-toolkit/plugin-forge",
    "softaworks/agent-toolkit/crafting-effective-readmes",
    "softaworks/agent-toolkit/command-creator",
    "softaworks/agent-toolkit/professional-communication",
    "softaworks/agent-toolkit/humanizer",
    "softaworks/agent-toolkit/c4-architecture",
    "obra/superpowers/using-superpowers",
    "obra/superpowers/verification-before-completion",
    "obra/superpowers/subagent-driven-development",
    "obra/superpowers/requesting-code-review",
    "obra/superpowers/writing-skills",
    "obra/superpowers/dispatching-parallel-agents",
    "obra/superpowers/using-git-worktrees",
    "obra/superpowers/receiving-code-review",
    "obra/superpowers/finishing-a-development-branch",
    "anthropics/skills/web-artifacts-builder",
    "anthropics/skills/algorithmic-art",
    "anthropics/skills/internal-comms",
    "anthropics/skills/brand-guidelines",
    "anthropics/skills/template-skill",
    "anthropics/skills/slack-gif-creator",
    "jimliu/baoyu-skills/baoyu-infographic",
    "jimliu/baoyu-skills/baoyu-image-gen",
    "jimliu/baoyu-skills/baoyu-url-to-markdown",
    "jimliu/baoyu-skills/baoyu-compress-image",
    "jimliu/baoyu-skills/baoyu-danger-gemini-web",
    "jimliu/baoyu-skills/baoyu-danger-x-to-markdown",
    "jimliu/baoyu-skills/release-skills",
    "op7418/youtube-clipper-skill/youtube-clipper",
    "op7418/humanizer-zh/humanizer-zh",
    "f/awesome-chatgpt-prompts/skill-lookup",
    "f/awesome-chatgpt-prompts/prompt-lookup",
    "langgenius/dify/frontend-code-review",
    "langgenius/dify/skill-creator",
    "langgenius/dify/web-design-guidelines",
    "langgenius/dify/vercel-react-best-practices",
    "langgenius/dify/component-refactoring",
    "langgenius/dify/frontend-testing",
    "anthropics/claude-code/frontend-design",
    "wshobson/agents/tailwind-design-system",
    "wshobson/agents/api-design-principles",
    "wshobson/agents/typescript-advanced-types",
    "wshobson/agents/postgresql-table-design",
    "wshobson/agents/architecture-patterns",
    "wshobson/agents/responsive-design",
    "wshobson/agents/python-performance-optimization",
    "wshobson/agents/nodejs-backend-patterns",
    "wshobson/agents/code-review-excellence",
    "wshobson/agents/sql-optimization-patterns",
    "wshobson/agents/e2e-testing-patterns",
    "wshobson/agents/github-actions-templates",
    "wshobson/agents/prompt-engineering-patterns",
    "wshobson/agents/web-component-design",
    "wshobson/agents/mobile-ios-design",
    "wshobson/agents/modern-javascript-patterns",
    "wshobson/agents/react-native-architecture",
    "wshobson/agents/python-testing-patterns",
    "wshobson/agents/fastapi-templates",
    "superdesigndev/superdesign-skill/superdesign",
    "benjitaylor/agentation/agentation",
    "giuseppe-trisciuoglio/developer-kit/shadcn-ui",
    "jezweb/claude-skills/tanstack-query",
    "boristane/agent-skills/logging-best-practices",
    "hyf0/vue-skills/vueuse-best-practices",
    "hyf0/vue-skills/pinia-best-practices",
    "vercel/turborepo/turborepo",
    "intellectronica/agent-skills/context7",
    "cloudai-x/threejs-skills/threejs-animation",
    "onmax/nuxt-skills/vue",
    "onmax/nuxt-skills/nuxt",
]


# ============================================================================
# SKILL CATEGORIZATION AND FILTERING
# ============================================================================

SKILL_CATEGORIES = {
    'frontend': ['react', 'vue', 'frontend', 'ui', 'web-design', 'tailwind', 'shadcn', 'canvas'],
    'backend': ['backend', 'api', 'postgres', 'supabase', 'nodejs', 'fastapi', 'database'],
    'mobile': ['expo', 'react-native', 'native', 'ios', 'mobile'],
    'testing': ['testing', 'test', 'qa', 'e2e'],
    'marketing': ['marketing', 'seo', 'copywriting', 'cro', 'analytics', 'social', 'ads'],
    'design': ['design', 'ui-ux', 'web-design', 'superdesign', 'canvas'],
    'devops': ['cicd', 'deployment', 'github-actions', 'workflow'],
    'documentation': ['pdf', 'pptx', 'xlsx', 'docx', 'slide', 'marp'],
    'architecture': ['architecture', 'patterns', 'c4'],
    'authentication': ['auth', 'better-auth'],
    'productivity': ['brainstorming', 'planning', 'debugging', 'code-review', 'commit'],
    'communication': ['communication', 'writing', 'professional', 'feedback'],
    'content': ['article', 'infographic', 'comic', 'image-gen', 'cover'],
    'workflow': ['superpowers', 'agent-toolkit', 'git-worktrees', 'session-handoff'],
}

# FilterFlix-specific skill recommendations
FILTERFLIX_RECOMMENDED = {
    'extension_development': [
        'anthropics/skills/frontend-design',
        'vercel-labs/agent-skills/web-design-guidelines',
        'anthropics/skills/webapp-testing',
        'wshobson/agents/web-component-design',
        'wshobson/agents/code-review-excellence',
    ],
    'marketing_launch': [
        'coreyhaines31/marketingskills/seo-audit',
        'coreyhaines31/marketingskills/copywriting',
        'coreyhaines31/marketingskills/launch-strategy',
        'coreyhaines31/marketingskills/social-content',
        'coreyhaines31/marketingskills/page-cro',
        'coreyhaines31/marketingskills/schema-markup',
    ],
    'backend_api': [
        'wshobson/agents/api-design-principles',
        'wshobson/agents/nodejs-backend-patterns',
        'supabase/agent-skills/supabase-postgres-best-practices',
        'wshobson/agents/postgresql-table-design',
    ],
    'documentation': [
        'anthropics/skills/pdf',
        'anthropics/skills/pptx',
        'softaworks/agent-toolkit/crafting-effective-readmes',
        'anthropics/skills/doc-coauthoring',
    ],
    'automation': [
        'expo/skills/expo-cicd-workflows',
        'wshobson/agents/github-actions-templates',
        'softaworks/agent-toolkit/dependency-updater',
        'obra/superpowers/test-driven-development',
    ],
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_skills_by_category(*categories):
    """
    Get skills matching one or more categories or keywords.

    Args:
        *categories: Variable number of category names or keywords

    Returns:
        List of matching skill IDs

    Example:
        >>> get_skills_by_category('frontend', 'react')
        >>> get_skills_by_category('marketing')
    """
    matching_skills = []
    search_terms = set()

    # Gather all search terms from category mappings
    for cat in categories:
        cat_lower = cat.lower()
        if cat_lower in SKILL_CATEGORIES:
            search_terms.update(SKILL_CATEGORIES[cat_lower])
        else:
            search_terms.add(cat_lower)

    # Search through skills
    for skill in skills:
        skill_lower = skill.lower()
        if any(term in skill_lower for term in search_terms):
            matching_skills.append(skill)

    return matching_skills


def get_skills_by_publisher(publisher):
    """
    Get all skills from a specific publisher.

    Args:
        publisher: Publisher name (e.g., 'anthropics', 'vercel-labs')

    Returns:
        List of skill IDs from that publisher

    Example:
        >>> get_skills_by_publisher('anthropics')
    """
    return [skill for skill in skills if skill.startswith(f"{publisher}/")]


def get_filterflix_recommendations(category=None):
    """
    Get FilterFlix-specific skill recommendations.

    Args:
        category: Optional category ('extension_development', 'marketing_launch', etc.)
                 If None, returns all recommendations

    Returns:
        Dictionary or list of recommended skills

    Example:
        >>> get_filterflix_recommendations('marketing_launch')
        >>> get_filterflix_recommendations()  # All recommendations
    """
    if category:
        return FILTERFLIX_RECOMMENDED.get(category, [])
    return FILTERFLIX_RECOMMENDED


def generate_install_command(skill_id):
    """
    Generate npx install command for a skill.

    Args:
        skill_id: Full skill ID (publisher/repo/skill-name)

    Returns:
        Shell command string

    Example:
        >>> generate_install_command('anthropics/skills/frontend-design')
        'npx skills add anthropics/skills/frontend-design'
    """
    return f"npx skills add {skill_id}"


def generate_bulk_install_script(skill_ids, output_file='install-skills.sh'):
    """
    Generate a shell script to install multiple skills.

    Args:
        skill_ids: List of skill IDs
        output_file: Output filename for the script

    Example:
        >>> recommendations = get_filterflix_recommendations('extension_development')
        >>> generate_bulk_install_script(recommendations, 'install-dev-skills.sh')
    """
    with open(output_file, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('# Auto-generated skill installation script\n')
        f.write(f'# Generated: {__import__("datetime").datetime.utcnow().isoformat()}Z\n\n')
        f.write('set -e  # Exit on error\n\n')

        for skill_id in skill_ids:
            f.write(f'echo "Installing {skill_id}..."\n')
            f.write(f'{generate_install_command(skill_id)}\n\n')

        f.write('echo "All skills installed successfully!"\n')

    # Make executable
    import os
    os.chmod(output_file, 0o755)

    return output_file


def search_skills(query):
    """
    Search skills by keyword.

    Args:
        query: Search query string

    Returns:
        List of matching skill IDs

    Example:
        >>> search_skills('testing')
        >>> search_skills('design')
    """
    query_lower = query.lower()
    return [skill for skill in skills if query_lower in skill.lower()]


def list_publishers():
    """
    Get unique list of all publishers.

    Returns:
        Sorted list of publisher names
    """
    publishers = set()
    for skill in skills:
        publisher = skill.split('/')[0]
        publishers.add(publisher)
    return sorted(publishers)


def print_skill_tree():
    """
    Print skills organized by publisher in a tree structure.
    """
    publishers = {}

    for skill in skills:
        parts = skill.split('/')
        publisher = parts[0]
        rest = '/'.join(parts[1:])

        if publisher not in publishers:
            publishers[publisher] = []
        publishers[publisher].append(rest)

    for publisher in sorted(publishers.keys()):
        print(f"\n{publisher}/")
        for skill in sorted(publishers[publisher]):
            print(f"  └── {skill}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Command-line interface for the skills catalog."""
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  list                          - List all skills")
        print("  publishers                    - List all publishers")
        print("  tree                          - Show skills in tree format")
        print("  search <query>                - Search for skills")
        print("  category <category>           - Get skills by category")
        print("  publisher <name>              - Get skills by publisher")
        print("  recommend [category]          - FilterFlix recommendations")
        print("  install <skill-id>            - Generate install command")
        print("  bulk-install <category>       - Generate bulk install script")
        print("\nCategories:")
        for cat in sorted(SKILL_CATEGORIES.keys()):
            print(f"  - {cat}")
        return

    command = sys.argv[1]

    if command == 'list':
        for skill in skills:
            print(skill)

    elif command == 'publishers':
        for pub in list_publishers():
            print(pub)

    elif command == 'tree':
        print_skill_tree()

    elif command == 'search' and len(sys.argv) > 2:
        query = sys.argv[2]
        results = search_skills(query)
        print(f"Found {len(results)} skills matching '{query}':\n")
        for skill in results:
            print(skill)

    elif command == 'category' and len(sys.argv) > 2:
        category = sys.argv[2]
        results = get_skills_by_category(category)
        print(f"Found {len(results)} skills in category '{category}':\n")
        for skill in results:
            print(skill)

    elif command == 'publisher' and len(sys.argv) > 2:
        publisher = sys.argv[2]
        results = get_skills_by_publisher(publisher)
        print(f"Found {len(results)} skills from '{publisher}':\n")
        for skill in results:
            print(skill)

    elif command == 'recommend':
        category = sys.argv[2] if len(sys.argv) > 2 else None
        recommendations = get_filterflix_recommendations(category)

        if category:
            print(f"FilterFlix recommendations for '{category}':\n")
            for skill in recommendations:
                print(skill)
        else:
            print("FilterFlix skill recommendations by category:\n")
            for cat, skill_list in recommendations.items():
                print(f"\n{cat}:")
                for skill in skill_list:
                    print(f"  - {skill}")

    elif command == 'install' and len(sys.argv) > 2:
        skill_id = sys.argv[2]
        print(generate_install_command(skill_id))

    elif command == 'bulk-install' and len(sys.argv) > 2:
        category = sys.argv[2]
        recommendations = get_filterflix_recommendations(category)
        if recommendations:
            output_file = generate_bulk_install_script(
                recommendations,
                f'install-{category}-skills.sh'
            )
            print(f"Generated installation script: {output_file}")
            print(f"\nTo install, run:")
            print(f"  ./{output_file}")
        else:
            print(f"Unknown category: {category}")
            print(f"Available categories: {', '.join(FILTERFLIX_RECOMMENDED.keys())}")

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see available commands")


if __name__ == '__main__':
    main()
