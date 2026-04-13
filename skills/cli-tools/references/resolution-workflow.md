# Missing Tool Resolution Workflow

## Phase 1: Diagnostic (BEFORE attempting install)

1. **Check if tool exists elsewhere:**
   ```bash
   which <tool>           # Is it installed but not in PATH?
   command -v <tool>      # Alternative check
   type -a <tool>         # Show all locations
   ```

2. **Why might it be missing?**
   - **PATH issue**: Tool installed but shell can't find it (check `~/.local/bin`, `/usr/local/bin`)
   - **Version conflict**: Multiple versions installed, wrong one active
   - **Shell state**: Installed in current session but shell hash table stale (`hash -r`)
   - **Package manager isolation**: Installed via pip/npm/cargo but not in global PATH

3. **If tool exists but not in PATH:**
   ```bash
   # Find the binary in common locations (avoids slow full-disk scans)
   find /usr/local/bin /usr/bin /opt -maxdepth 3 -type f -name "<tool>" 2>/dev/null
   find "$HOME/.local/bin" -maxdepth 1 -type f -name "<tool>" 2>/dev/null

   # Add to PATH temporarily
   export PATH="$PATH:/path/to/tool/directory"
   ```

## Phase 2: Installation

1. Extract tool name from error
2. Lookup in [binary_to_tool_map.md](./binary_to_tool_map.md) (e.g., `rg` -> `ripgrep`)
3. Install: `scripts/install_tool.sh <tool> install`

## Phase 3: Verification (AFTER install)

1. **Confirm installation succeeded:**
   ```bash
   which <tool>           # Should show path
   <tool> --version       # Should show version
   ```

2. **If "command not found" persists after install:**
   ```bash
   hash -r                # Clear shell's command hash
   source ~/.bashrc       # Reload shell configuration
   # Or start a new shell session
   ```

3. **Retry original command**
