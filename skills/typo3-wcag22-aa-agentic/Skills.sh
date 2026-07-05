#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="typo3-wcag22-aa-agentic"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(pwd)"
SKILLS_DIR="${HOME}/.skills"
FORCE=0

print_help() {
  cat <<'EOF'
TYPO3 WCAG 2.2 AA Agentic Skill helper

Usage:
  ./Skills.sh install [--skills-dir ~/.skills]
  ./Skills.sh scaffold --project /path/to/typo3-project [--force]
  ./Skills.sh init --project /path/to/typo3-project [--force]
  ./Skills.sh help

Commands:
  install   Copy this whole skill bundle into a local skills directory.
  scaffold  Copy runnable accessibility tooling from project-template into a TYPO3 project.
  init      Alias for scaffold.

Examples:
  ./Skills.sh install --skills-dir "$HOME/.skills"
  ./Skills.sh scaffold --project "$HOME/projects/my-typo3-site"

Notes:
  - scaffold does not run npm install automatically.
  - existing files are not overwritten unless --force is used.
  - credentials such as AXE_API_KEY must be stored in environment variables.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    install|scaffold|init|help|-h|--help)
      COMMAND="$1"; shift ;;
    --project)
      PROJECT_DIR="${2:?Missing value for --project}"; shift 2 ;;
    --skills-dir)
      SKILLS_DIR="${2:?Missing value for --skills-dir}"; shift 2 ;;
    --force)
      FORCE=1; shift ;;
    *)
      echo "Unknown argument: $1" >&2
      print_help
      exit 2 ;;
  esac
done

COMMAND="${COMMAND:-help}"

copy_tree_no_overwrite() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  (cd "$src" && find . -type d -print) | while read -r dir; do
    mkdir -p "$dst/$dir"
  done
  (cd "$src" && find . -type f -print) | while read -r file; do
    local target="$dst/$file"
    if [[ -e "$target" && "$FORCE" != "1" ]]; then
      echo "skip existing: $target"
    else
      cp "$src/$file" "$target"
      echo "copy: $target"
    fi
  done
}

case "$COMMAND" in
  help|-h|--help)
    print_help
    ;;
  install)
    mkdir -p "$SKILLS_DIR"
    TARGET="$SKILLS_DIR/$SKILL_NAME"
    if [[ -e "$TARGET" ]]; then
      if [[ "$FORCE" == "1" ]]; then
        rm -rf "$TARGET"
      else
        echo "Skill already exists: $TARGET"
        echo "Use --force to replace it."
        exit 1
      fi
    fi
    cp -R "$SCRIPT_DIR" "$TARGET"
    echo "Installed skill to: $TARGET"
    ;;
  scaffold|init)
    if [[ ! -d "$PROJECT_DIR" ]]; then
      echo "Project directory does not exist: $PROJECT_DIR" >&2
      exit 1
    fi
    copy_tree_no_overwrite "$SCRIPT_DIR/project-template" "$PROJECT_DIR"
    chmod +x "$PROJECT_DIR/scripts/run-a11y.sh" 2>/dev/null || true
    echo
    echo "Scaffold complete. Next:"
    echo "  cd '$PROJECT_DIR'"
    echo "  cp .a11y/a11y.config.example.yml .a11y/a11y.config.yml"
    echo "  npm install"
    echo "  npx playwright install chromium"
    echo "  npm run a11y:all"
    ;;
  *)
    print_help
    exit 2
    ;;
esac
