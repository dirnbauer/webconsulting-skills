# Preferred Tools - Detailed Reference

Modern CLI tools that replace legacy Unix utilities with faster, safer, and more ergonomic alternatives. Organized by domain.

---

## File Search & Code Navigation

### rg (ripgrep) instead of grep

**Install:** `cargo install ripgrep` or `apt install ripgrep`

ripgrep is a line-oriented search tool that recursively searches directories for a regex pattern. It respects `.gitignore` rules by default and is typically 10x faster than grep on large codebases.

```bash
# Basic search (recursive by default, unlike grep)
rg 'TODO|FIXME'

# Search specific file types
rg -t py 'import asyncio'

# Search with context lines
rg -C 3 'def process'

# Fixed string search (no regex interpretation)
rg -F 'array[0]'

# Search hidden files and ignored files too
rg -uu 'SECRET_KEY'

# Count matches per file
rg -c 'error' --sort path

# JSON output for piping to jq
rg --json 'pattern' | jq 'select(.type == "match")'
```

**Configuration** (`~/.ripgreprc`, set via `RIPGREP_CONFIG_PATH`):
```
--smart-case
--max-columns=200
--glob=!.git
--glob=!node_modules
--glob=!vendor
```

### fd instead of find

**Install:** `cargo install fd-find` or `apt install fd-find`

fd is a fast, user-friendly alternative to find. It respects `.gitignore`, uses regex by default, and has sensible defaults (ignores hidden files, colorized output).

```bash
# Find files by name (regex by default)
fd 'test.*\.py$'

# Find by extension
fd -e json

# Find directories only
fd -t d src

# Find and execute command on each result
fd -e log -x gzip {}

# Find files modified in last 24h
fd --changed-within 1d

# Include hidden and ignored files
fd -HI 'config'

# CAUTION: Destructive - preview matches with `fd -e tmp` first, then:
fd -e tmp -x rm {}
```

**Configuration** (`.fdignore` in project root, same syntax as `.gitignore`):
```
node_modules
.git
target
dist
```

### rga (ripgrep-all) instead of grep on documents

**Install:** `cargo install ripgrep_all` or download from https://github.com/phiresky/ripgrep-all/releases

Searches inside PDFs, Word documents, Excel files, ZIP archives, SQLite databases, and more by converting them to text on-the-fly.

```bash
# Search PDFs in current directory
rga 'financial statement' ./reports/

# Search inside ZIP archives
rga 'config' ./backups/

# Search Office documents
rga 'quarterly revenue' ./documents/

# Limit to specific adapters
rga --rga-adapters=poppler 'pattern' ./pdfs/
```

### tokei / scc instead of cloc or wc -l

**Install:** `cargo install tokei` or `go install github.com/boyter/scc/v3@latest`

Both are dramatically faster than cloc for counting lines of code and provide accurate language detection. scc additionally estimates code complexity and cost.

```bash
# tokei - fast code statistics
tokei
tokei src/
tokei --sort code    # Sort by code lines

# scc - code statistics with complexity/cost estimates
scc
scc --by-file        # Show per-file stats
scc -f json          # JSON output for processing
scc --no-cocomo      # Skip cost estimate
```

---

## Structured Data Processing

### jq instead of grep/awk/sed on JSON

**Install:** `apt install jq` or download from https://jqlang.github.io/jq/

jq is a lightweight command-line JSON processor. Never use grep/sed/awk on JSON - they break on nested structures, special characters, and multiline values.

```bash
# Extract a field
jq '.name' package.json

# Filter arrays
jq '.[] | select(.status == "active")' data.json

# Transform structure
jq '{name: .metadata.name, version: .spec.version}' manifest.json

# Combine with gh CLI
gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title) (\(.author.login))"'

# Combine with curl
curl -s https://api.example.com/data | jq '.results[].name'

# Slurp multiple JSON objects into array
jq -s '.' *.json

# Raw output (no quotes) for scripting
jq -r '.version' package.json
```

### yq instead of sed/awk on YAML

**Install:** `go install github.com/mikefarah/yq/v4@latest` or `brew install yq` or download binary from https://github.com/mikefarah/yq/releases

Syntax-aware YAML processing that preserves comments and formatting. **Important:** Do NOT use `pip install yq` - that installs kislyuk/yq, a different tool (Python jq wrapper for YAML). This skill documents Mike Farah's Go-based yq.

```bash
# Read a value
yq '.metadata.name' chart.yaml

# Set a value (in-place)
yq -i '.spec.replicas = 3' deployment.yaml

# Merge YAML files
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' base.yaml overlay.yaml

# Convert YAML to JSON
yq -o json '.' config.yaml

# Convert JSON to YAML
yq -P '.' config.json

# Edit array elements
yq -i '.services[0].ports[0] = "8080:80"' docker-compose.yml
```

### dasel instead of sed on TOML/XML/JSON/YAML

**Install:** `go install github.com/tomwright/dasel/v2/cmd/dasel@latest`

Universal data format selector - handles JSON, YAML, TOML, XML, and CSV with a single tool and consistent query syntax.

```bash
# Read from any format (auto-detected)
dasel -f config.toml '.database.host'
dasel -f pom.xml '.project.version'

# Write/update values
dasel put -f config.toml -t string -v 'localhost' '.database.host'

# Convert between formats
dasel -f config.yaml -w json

# Pipe mode
cat data.json | dasel -p json '.users.[0].name'
```

### qsv instead of awk/Python on CSV

**Install:** Download from https://github.com/dathere/qsv/releases

A fast CSV toolkit that correctly handles quoting, headers, encoding, and large files. Dramatically faster than awk/Python for CSV processing.

```bash
# View headers
qsv headers data.csv

# Select columns
qsv select name,email data.csv

# Filter rows
qsv search -s status 'active' data.csv

# Sort by column
qsv sort -s revenue -N -R data.csv    # Numeric, reverse

# Statistics summary
qsv stats data.csv

# Frequency counts
qsv frequency -s category data.csv

# Join two CSVs
qsv join id users.csv user_id orders.csv

# SQL queries on CSV
qsv sqlp 'SELECT name, SUM(amount) FROM data GROUP BY name' data.csv

# Sample random rows
qsv sample 100 large-dataset.csv
```

---

## Git & Diff Tools

### difft (difftastic) instead of diff

**Install:** `cargo install difftastic`

A structural diff tool that understands programming language syntax. Ignores formatting-only changes and provides accurate, readable diffs.

```bash
# Compare two files
difft old.py new.py

# Use as git diff tool
git -c diff.external=difft diff
git -c diff.external=difft show HEAD

# Configure as default git diff tool
git config --global diff.tool difftastic
git config --global difftool.difftastic.cmd 'difft "$LOCAL" "$REMOTE"'
git config --global difftool.prompt false
```

### git absorb instead of git commit --fixup

**Install:** `cargo install git-absorb`

Automatically identifies which staged changes belong to which previous commit and creates fixup commits. Replaces the manual workflow of `git log`, identifying the right commit, then `git commit --fixup=<sha>`.

```bash
# Stage changes then auto-absorb
git add -p
git absorb

# Then squash the fixups
git rebase -i --autosquash main

# Dry run - see what would happen
git absorb --dry-run
```

---

## Security

### semgrep instead of manual grep for security

**Install:** `pip install semgrep` or `brew install semgrep`

AST-aware static analysis with pre-built rulesets for OWASP Top 10, CWEs, and language-specific security patterns. Far more accurate than text-based grep patterns.

```bash
# Run auto-detected rules
semgrep --config auto .

# OWASP Top 10 scan
semgrep --config "p/owasp-top-ten" .

# Language-specific rules
semgrep --config "p/python" .
semgrep --config "p/php" .
semgrep --config "p/javascript" .

# Output as JSON for processing
semgrep --config auto --json . | jq '.results[] | {path: .path, line: .start.line, message: .extra.message}'

# CI-friendly (fail on findings)
semgrep --config auto --error .
```

---

## Benchmarking

### hyperfine instead of time

**Install:** `cargo install hyperfine` or `apt install hyperfine`

Statistical command benchmarking with warmup, multiple runs, comparison, and export features. Essential for making data-driven performance claims.

```bash
# Basic benchmark (auto-detects run count)
hyperfine 'fd -e py'

# Compare two commands side by side
hyperfine 'find . -name "*.py"' 'fd -e py'

# With warmup runs (important for disk cache)
hyperfine --warmup 3 'rg pattern'

# Minimum runs for statistical significance
hyperfine --min-runs 20 'command'

# Parameterized benchmarks
hyperfine -P threads 1 8 'sort --parallel={threads} data.txt'

# Shell selection (default is sh)
hyperfine -S bash 'echo ${BASH_VERSION}'

# Export results
hyperfine --export-markdown bench.md 'grep -r pattern .' 'rg pattern'
hyperfine --export-json bench.json 'command1' 'command2'
hyperfine --export-csv bench.csv 'command1' 'command2'

# Preparation command (run before each benchmark)
# NOTE: Clearing page cache requires sudo/root privileges
hyperfine --prepare 'sync; echo 3 | sudo tee /proc/sys/vm/drop_caches' 'cat large-file'

# Cleanup command (run after each benchmark)
hyperfine --cleanup 'rm -f output.txt' 'generate output.txt'

# Show intermediate results
hyperfine --show-output 'echo hello'
```

**Interpreting results:**
- **Mean:** Average execution time across all runs
- **Stddev:** Standard deviation - high values indicate inconsistent performance
- **Min/Max:** Fastest and slowest runs
- **Relative:** "X is Y times faster than Z" comparison

---

## Viewing & General

### bat instead of cat

**Install:** `cargo install bat` or `apt install bat`

A cat clone with syntax highlighting, line numbers, git integration, and automatic paging.

```bash
# View file with syntax highlighting
bat script.py

# Show specific lines
bat -r 10:20 main.go

# Plain mode (no decoration, for piping)
bat -pp data.json | jq '.'

# Show non-printable characters
bat -A config.yml

# Use as man pager
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
```

---

## Tool Integration Patterns

These modern tools work well together through pipes and subshells:

```bash
# fd + rg: Find files then search contents
fd -e yaml | xargs rg 'apiVersion: v2'

# fd + bat: Find and view files
fd 'Dockerfile' -x bat {}

# rg + jq: Search JSON files and process matches
rg -l 'error' --glob '*.json' | xargs -I{} jq '.errors' {}

# gh + jq: GitHub API with structured processing
gh api repos/{owner}/{repo}/pulls --jq '.[].title'

# fd + hyperfine: Benchmark file operations
hyperfine 'fd -e py | wc -l' 'find . -name "*.py" | wc -l'

# scc + jq: Process code statistics
scc -f json | jq '.[] | {Name, Code, Lines}'

# qsv + jq: CSV to JSON pipeline
qsv tojsonl data.csv | jq 'select(.status == "active")'
```

---

## Performance Reference

Typical speedup factors (varies by workload and hardware):

| Legacy | Modern | Typical Speedup |
|--------|--------|----------------|
| `grep -r` | `rg` | 5-15x |
| `find` | `fd` | 3-8x |
| `cloc` | `tokei` | 10-50x |
| `cloc` | `scc` | 50-100x |
| `awk` on CSV | `qsv` | 50-200x |
| `diff` | `difft` | Similar speed, much better output |

Verify with hyperfine on your actual workload:
```bash
hyperfine --warmup 3 'grep -r "pattern" .' 'rg "pattern"'
```
