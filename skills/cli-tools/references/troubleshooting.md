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

## Node/nvm: global installs land off-PATH (a `node` shim hijacks npm's prefix)

When a global install succeeds (`npm i -g <tool>` reports "added N packages") but
`command -v <tool>` then fails — or `npm prefix -g` points at a Node version that
isn't your active/default one — suspect a **manual `node` symlink on PATH ahead of
nvm** (commonly `~/.local/bin/node`, often created to give another tool a stable
node).

Because that shim is first on PATH, **every** `node`/`npm` resolves through it, so
npm's global prefix is locked to that Node's tree — and globals (eslint, pnpm,
prettier, …) land in a `bin/` that isn't on PATH. npm self-update can also hit the
wrong tree.

Diagnose:

```bash
command -v node                 # may show only the shim, e.g. ~/.local/bin/node
node -p 'process.execPath'      # the REAL node the shim points at
npm prefix -g                   # the prefix globals install into
nvm version default             # what nvm thinks the default is
```

If `process.execPath` / `npm prefix -g` disagree with the nvm default, the shim is
the cause.

Fix — remove or re-point the shim identified above (the `node` on PATH that is
**not** under `~/.nvm` — commonly `~/.local/bin/node`, but use the path your
diagnosis returned), then align the nvm default:

```bash
SHIM=~/.local/bin/node          # <- replace with the shim path from the diagnosis
rm "$SHIM"                      # or: ln -sf "$(nvm which default)" "$SHIM"
nvm alias default node          # point default at the newest installed Node
hash -r
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
