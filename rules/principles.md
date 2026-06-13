# Principles for Writing & Maintaining TYPO3 Agent Rules

These principles govern how rules in this layer are authored and kept correct. They
apply to anyone (human or agent) adding or editing a rule file.

1. **Atomic.** One rule = one constraint. If a file needs the word "and" to describe
   what it forbids, split it. A rule body stays ≤ ~45 lines including the example.

2. **Verifiable.** Every technical claim (class name, namespace, method signature,
   removed/added API, version fact) must be checked against the installed core source
   before it is asserted. Grep `vendor/`; never assert from memory. If a claim cannot
   be verified, soften it ("prefer", "generally") or omit it.

3. **v14-accurate.** Rules target the current LTS line (14.3.x, PHP 8.2–8.5). Code
   examples must reflect the *installed* v14 API — not v11/v12/v13 habits and not
   anticipated v15 changes. Flag APIs already deprecated for v15 removal.

4. **File-targeted.** Every rule declares precise `appliesTo` globs so agents load it
   only for relevant changes. Prefer the narrowest glob that still covers the rule
   (e.g. `**/Configuration/TCA/**` over `**/*.php`).

5. **Severity-graded.** Choose `error` only for things that are genuinely wrong or
   break on v14 (removed APIs, injection risks). Use `warning` for strongly
   discouraged patterns and `info` for conventions. Don't inflate severity.

6. **Cite sources.** End each rule with a `> Why:` line naming the concrete reason and,
   where one exists, the TYPO3 changelog issue (`#NNNNNN`) that documents the change.
   Citations make the rule auditable and let agents explain their reasoning.

7. **Show, don't lecture.** Lead with a minimal, copy-pasteable Do/Don't pair and one
   correct example in the right language fence (php / yaml / typoscript / html). The
   example carries more weight than prose for a coding agent.
