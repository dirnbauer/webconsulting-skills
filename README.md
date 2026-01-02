# webconsulting Claude Marketplace

AI-augmented development environment for enterprise TYPO3 projects. This repository provides **Agent Skills** that transform Claude into a specialized TYPO3 Solutions Architect.

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

## What's Included

### Agent Skills

| Skill | Purpose |
|-------|---------|
| `webconsulting-branding` | Design tokens, MDX components, brand guidelines |
| `typo3-datahandler` | Transactional database operations via DataHandler |
| `typo3-ddev` | Local DDEV development environment |
| `typo3-seo` | SEO configuration with EXT:seo |
| `typo3-security` | Security hardening checklist |
| `typo3-rector` | TYPO3 upgrade patterns with Rector |
| `typo3-update` | TYPO3 v13/v14 migration guide (prefers v14) |

### Cursor Integration

- **Master Architect Rule**: Defines Claude as Senior TYPO3 Solutions Architect
- **MCP Configuration**: Placeholder for DDEV, Hetzner, and MySQL servers

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude / Cursor IDE                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Skills    │  │   Rules     │  │    MCP Servers      │  │
│  │  (How-To)   │  │  (Context)  │  │   (Execution)       │  │
│  ├─────────────┤  ├─────────────┤  ├─────────────────────┤  │
│  │ Branding    │  │ Master      │  │ DDEV (local)        │  │
│  │ DataHandler │  │ Architect   │  │ Hetzner (hosting)   │  │
│  │ DDEV        │  │             │  │ MySQL (database)    │  │
│  │ SEO         │  │             │  │                     │  │
│  │ Security    │  │             │  │                     │  │
│  │ Rector      │  │             │  │                     │  │
│  │ Update      │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
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

## Contributing

1. Create a skill in `skills/your-skill-name/SKILL.md`
2. Follow the SKILL.md format (see existing skills)
3. Run `./install.sh` to test
4. Submit a pull request

## License

MIT License - webconsulting.at

