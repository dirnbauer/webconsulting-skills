# webconsulting Claude Marketplace

AI-augmented development environment for enterprise TYPO3 projects. This repository provides **Agent Skills** that transform Claude into a specialized TYPO3 Solutions Architect.

> **Attribution:** The majority of skills in this repository are derived from the excellent work by
> **[Netresearch DTT GmbH](https://github.com/netresearch)**. We recommend using their original
> repositories for the latest updates. A few additional skills are specific to webconsulting.at.

## Quick Start

```bash
# Clone the repository
git clone git@github.com:dirnbauer/claude-cursor-typo3-skills.git
cd claude-cursor-typo3-skills

# Install skills
chmod +x install.sh
./install.sh

# Restart Cursor IDE
```

### Alternative: Composer Agent Skill Plugin

For automatic skill loading in PHP projects, use Netresearch's Composer plugin:

```bash
composer require --dev netresearch/composer-agent-skill-plugin
```

This plugin automatically discovers and loads agent skills from your Composer dependencies.
See: https://github.com/netresearch/composer-agent-skill-plugin

### Alternative: Composer from GitHub (VCS)

Install this skills package directly from GitHub without Packagist.

**1. Add the repository to your project's `composer.json`:**

```json
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/dirnbauer/claude-cursor-typo3-skills"
        }
    ]
}
```

**2. Require the package:**

```bash
composer require --dev webconsulting/claude-typo3-skills:dev-main
```

The Composer plugin will automatically run `install.sh` after installation to deploy skills to `~/.claude/skills` and generate Cursor rules.

## What's Included

### Agent Skills

| Skill | Purpose | Origin |
|-------|---------|--------|
| **TYPO3 Development** | | |
| `typo3-datahandler` | Transactional database operations via DataHandler | Netresearch |
| `typo3-ddev` | Local DDEV development environment | Netresearch |
| `typo3-testing` | Unit, functional, E2E, architecture testing | Netresearch |
| `typo3-conformance` | Extension standards compliance checker | Netresearch |
| `typo3-docs` | Documentation using docs.typo3.org standards | Netresearch |
| `typo3-core-contributions` | TYPO3 Core contribution workflow (Gerrit, Forge) | Netresearch |
| **Upgrade & Migration** | | |
| `typo3-rector` | TYPO3 upgrade patterns with Rector | Netresearch |
| `typo3-update` | TYPO3 v13/v14 migration guide (prefers v14) | Netresearch |
| `typo3-extension-upgrade` | Systematic extension upgrades (Rector, Fractor) | Netresearch |
| **Security & Operations** | | |
| `typo3-security` | Security hardening checklist | Netresearch |
| `typo3-seo` | SEO configuration with EXT:seo | Netresearch |
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS) | Netresearch |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security | Netresearch |
| **PHP & Tools** | | |
| `php-modernization` | PHP 8.x patterns, PHPStan, DTOs, enums | Netresearch |
| `cli-tools` | CLI tool management and auto-installation | Netresearch |
| `context7` | Library documentation lookup via REST API | Netresearch |
| **WebConsulting Specific** | | |
| `webconsulting-branding` | Design tokens, MDX components, brand guidelines | webconsulting |
| `ui-design-patterns` | Practical UI design patterns, accessibility | webconsulting |

### Cursor Integration

- **Master Architect Rule**: Defines Claude as Senior TYPO3 Solutions Architect
- **MCP Configuration**: Placeholder for DDEV, Hetzner, and MySQL servers

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude / Cursor IDE                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌───────────┐  ┌───────────────┐  │
│  │   Skills (How-To)   │  │   Rules   │  │  MCP Servers  │  │
│  ├─────────────────────┤  ├───────────┤  ├───────────────┤  │
│  │ TYPO3 Development   │  │ Master    │  │ DDEV (local)  │  │
│  │ Upgrade & Migration │  │ Architect │  │ Hetzner       │  │
│  │ Security & Ops      │  │           │  │ MySQL         │  │
│  │ PHP & Tools         │  │           │  │               │  │
│  │ WebConsulting       │  │           │  │               │  │
│  └─────────────────────┘  └───────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### MCP Servers

Edit `.cursor/mcp.json` to add your MCP server configurations:

```json
{
  "mcpServers": {
    "ddev": {
      "command": "npx",
      "args": ["-y", "@codingsasi/ddev-mcp"]
    },
    "hetzner": {
      "command": "npx",
      "args": ["-y", "mcp-hetzner"],
      "env": {
        "HCLOUD_TOKEN": "${HCLOUD_TOKEN}"
      }
    }
  }
}
```

### Updating Skills

```bash
# Pull latest changes
git pull origin main

# Re-run installation
./install.sh
```

## Technology Stack

- **PHP 8.2+** with strict types
- **TYPO3 v13/v14** (preferring v14)
- **DDEV** for local development
- **Hetzner Cloud** for hosting
- **Fluid/Twig** templating
- **TailwindCSS** for styling

## Excluded Technologies

This marketplace explicitly excludes:
- Go
- Jira
- Non-PHP backends

## Netresearch Skill Repositories

The following Netresearch repositories are the source for most skills:

- https://github.com/netresearch/typo3-ddev-skill
- https://github.com/netresearch/typo3-testing-skill
- https://github.com/netresearch/typo3-conformance-skill
- https://github.com/netresearch/typo3-docs-skill
- https://github.com/netresearch/typo3-core-contributions-skill
- https://github.com/netresearch/typo3-extension-upgrade-skill
- https://github.com/netresearch/security-audit-skill
- https://github.com/netresearch/enterprise-readiness-skill
- https://github.com/netresearch/php-modernization-skill
- https://github.com/netresearch/cli-tools-skill
- https://github.com/netresearch/context7-skill

## Contributing

1. Create a skill in `skills/your-skill-name/SKILL.md`
2. Follow the SKILL.md format (see existing skills)
3. Run `./install.sh` to test
4. Submit a pull request

## License

MIT License - webconsulting.at

## Acknowledgements

We are deeply grateful to **[Netresearch DTT GmbH](https://www.netresearch.de/)** for their
outstanding contributions to the TYPO3 community. Their excellent methodology and best practices
have been invaluable in shaping these guidelines.

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices
Adapted by webconsulting.at for this skill collection
