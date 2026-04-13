---
name: cli-tools
description: "Use when ANY command fails with 'command not found', when installing CLI tools (ripgrep, fd, jq, yq, bat, etc.), auditing project environments, or batch-updating tools. Triggers on: command not found, install tool, missing binary, environment audit, update tools, which, apt install, brew install."
license: "(MIT AND CC-BY-SA-4.0)"
compatibility: "Requires bash, common package managers."
metadata:
  version: "1.6.0"
  repository: "https://github.com/netresearch/cli-tools-skill"
  author: "Netresearch DTT GmbH"
allowed-tools:
  - "Bash(apt:*)"
  - "Bash(brew:*)"
  - "Bash(npm:*)"
  - "Bash(pip:*)"
  - "Read"
  - "Write"
---

# CLI Tools Skill

Install, audit, update, and recommend CLI tools across 74 cataloged entries.

## Triggers

- **Reactive**: `command not found` errors -- auto-resolve
- **Proactive**: "check environment", "install X", "update tools"
- **Advisory**: Recommend modern alternatives (`grep`->`rg`, `find`->`fd`, JSON->`jq`)

## Preferred Modern Tools

Recommend over legacy equivalents. See `references/preferred-tools.md` for examples.

| Legacy | Modern | Legacy | Modern |
|--------|--------|--------|--------|
| `grep -r` | `rg` | `diff` | `difft` |
| `find` | `fd` | `time` | `hyperfine` |
| grep on JSON | `jq` | `cat` | `bat` |
| sed on YAML | `yq` | `cloc` | `tokei`/`scc` |
| awk on CSV | `qsv` | grep for sec | `semgrep` |
| sed on TOML | `dasel` | | |

## Workflows

### Missing Tool Resolution

1. **Diagnose**: `which <tool>`, `command -v <tool>`, `type -a <tool>`
2. **Map binary**: Check `references/binary_to_tool_map.md` (`rg`->`ripgrep`, `ansible`->`ansible-core`, `batcat`->`bat`)
3. **Install**: `scripts/install_tool.sh <tool> install`
4. **Verify**: `which <tool>` + `<tool> --version`; if still missing: `hash -r`, check PATH

See `references/resolution-workflow.md` for full diagnostic steps.

### Environment Audit

Run `scripts/check_environment.sh audit .` and `scripts/detect_project_type.sh`, then cross-reference with `references/project_type_requirements.md` for per-type tool lists.

### Batch Update

`scripts/auto_update.sh` (all managers) or `scripts/install_tool.sh <tool> update` (single).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Installed but not found | `hash -r` or add dir to PATH |
| No sudo | `cargo install`, `pip install --user`, manual binary |
| Debian `bat`=`batcat`, `fd`=`fdfind` | Symlink to `~/.local/bin/` |

See `references/troubleshooting.md` for Docker fallbacks and permission workarounds.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/install_tool.sh` | Install/update/uninstall/status |
| `scripts/auto_update.sh` | Batch update package managers |
| `scripts/check_environment.sh` | Audit environment and PATH |
| `scripts/detect_project_type.sh` | Detect project type |

## References

| File | Purpose |
|------|---------|
| `references/binary_to_tool_map.md` | Binary-to-catalog mapping |
| `references/project_type_requirements.md` | Tools per project type |
| `references/preferred-tools.md` | Modern tool usage patterns |
| `references/resolution-workflow.md` | Diagnostic/install/verify flow |
| `references/troubleshooting.md` | PATH, permissions, fallbacks |

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/cli-tools-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
