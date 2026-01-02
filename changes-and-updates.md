# Changes and Updates

- 2026-01-02 — DataHandler cmd examples now use the correct `move`/`copy` syntax and clarified transaction guidance because DataHandler already wraps its own writes; only outer transactions are needed when bundling adjacent operations on the same connection.
- 2026-01-02 — DDEV snapshot deletion now uses `ddev snapshot delete` and the “nuclear option” note warns it drops the database volume, to avoid steering users toward unsupported flags or accidental data loss.
- 2026-01-02 — Robots.txt sitemap example now uses `{getEnv:TYPO3_SITE_URL}sitemap.xml` so generated URLs stay accurate to the site base instead of the current request host.
- 2026-01-02 — Install Tool password guidance no longer shows an empty placeholder and instructs setting the hashed password per environment to prevent unsafe defaults being committed.

