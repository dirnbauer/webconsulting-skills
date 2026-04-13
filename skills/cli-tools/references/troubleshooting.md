# Troubleshooting

## PATH Issues

When a tool installs but still shows "command not found":

1. **Check where it was installed:**
   ```bash
   # Common install locations
   ls -la ~/.local/bin/<tool>
   ls -la ~/.cargo/bin/<tool>
   ls -la ~/.npm-global/bin/<tool>
   ls -la /usr/local/bin/<tool>
   ```

2. **Ensure PATH includes common directories:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.npm-global/bin:$PATH"
   ```

3. **Reload shell configuration:**
   ```bash
   source ~/.bashrc        # or ~/.zshrc
   hash -r                 # Clear command cache
   exec $SHELL             # Restart shell
   ```

## Installation Blocked (Permission/System Restrictions)

When system prevents normal installation, use these alternatives:

1. **Docker (no install required):**
   ```bash
   # Run tool in container
   docker run --rm -v "$PWD:/work" -w /work <tool-image> <tool> <args>

   # Create alias for convenience
   alias <tool>='docker run --rm -v "$PWD:/work" -w /work <tool-image> <tool>'
   ```

2. **Manual binary download:**
   ```bash
   # Download release binary directly
   curl -L <release-url> -o ~/.local/bin/<tool>
   chmod +x ~/.local/bin/<tool>
   ```

3. **Compile from source:**
   ```bash
   git clone <repo-url>
   cd <repo>
   make && make install PREFIX=~/.local
   ```

4. **Use package manager with user scope:**
   ```bash
   pip install --user <tool>
   npm install -g <tool> --prefix ~/.npm-global
   cargo install <tool>  # Installs to ~/.cargo/bin
   ```
