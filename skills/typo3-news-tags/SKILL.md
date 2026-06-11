---
name: "typo3-news-tags"
description: "Bulk-generates thematic tags for georgringer/news (EXT:news) and assigns them to existing news records via keyword matching. Use when tagging large news corpora, defining a generic tag catalogue, building a Symfony console command for tag assignment, working with tx_news_domain_model_tag / tx_news_domain_model_news_tag_mm, or installing b13/tag as a generic site-wide tagging capability alongside news tags."
compatibility: "TYPO3 14.x (EXT:news ^14)"
metadata:
  version: "1.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---

# TYPO3 News Tags — Bulk Generation & Assignment

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** TYPO3 v14.x with `georgringer/news` ^14.
> All code examples target TYPO3 v14 APIs only. Do not use this skill for v12 / v13 sites.

> **Scope.** Designing, generating and assigning **thematic news tags** (`tx_news_domain_model_tag`)
> in georgringer/news at scale (hundreds to tens of thousands of news), and optionally installing
> the orthogonal generic tag system from `b13/tag` (`sys_tag`).
>
> **Not in scope.** Frontend rendering of tags in Fluid templates, tag translations, or tag merging.

## When to use this skill

Trigger this skill when the user asks to:
- "Tag all news / tag the latest N news"
- "Define a tag catalogue / generic tags / thematic tags"
- "Assign categories or tags in bulk to existing news"
- "Install a generic tagging extension" (b13/tag)
- "Build a Symfony command that tags news" / "automate tagging in TYPO3"
- "Why are large UIDs missing from my QueryBuilder result" (DBAL gotcha, §8)

## Mental model

EXT:news ships **two relations** for news classification:

| Relation | Table | Purpose | Routing |
|---|---|---|---|
| Categories | `sys_category` ← `sys_category_record_mm` | Primary hierarchical taxonomy | Optional |
| Tags | `tx_news_domain_model_tag` ← `tx_news_domain_model_news_tag_mm` | Flat, slug-routable thematic crosscuts | `NewsTag` aspect in site config |

**Categories** answer "what bucket is this in?" — typically a few per news, hierarchical, often
locale-aware. **Tags** answer "what themes does this touch?" — typically 5–10 per news, flat,
URL-friendly via `/{tag-slug}/`.

If the site already has narrow business categories ("Betrügerische Shops", "Phishing", …),
tags should be **orthogonal and thematic** (e.g. "Künstliche Intelligenz", "Banking", "Senioren")
— not redundant copies of categories.

`b13/tag` is a **different system**: `sys_tag` + `sys_tag_mm` with a `keywords` int column on
the target table. It is generic across all record types but **not** integrated with EXT:news.
Use it for tagging *other* tables; keep EXT:news's native tags for news.

## Default workflow

### 1. Verify the corpus (always)

```bash
ddev mysql -e "SELECT COUNT(*) FROM tx_news_domain_model_news WHERE pid=<PID> AND deleted=0 AND hidden=0;"
ddev mysql -e "SELECT COUNT(*) FROM tx_news_domain_model_tag WHERE deleted=0;"
ddev mysql -e "SELECT COUNT(*) FROM tx_news_domain_model_news_tag_mm;"
```

Identify where the readable text actually lives. With EXT:news's built-in `contentElementRelation`
extension configuration or `mask` based content, **`tx_news_domain_model_news.bodytext` is often
empty** — the real content sits in `tt_content` rows linked via `tx_news_related_news`. Verify:

```sql
SELECT AVG(LENGTH(bodytext)) FROM tx_news_domain_model_news WHERE pid=<PID> AND deleted=0;
SELECT CType, COUNT(*) FROM tt_content
  WHERE tx_news_related_news > 0 AND deleted=0 AND hidden=0
  GROUP BY CType ORDER BY 2 DESC;
```

If average bodytext is ~0, you **must** harvest `tt_content` to get meaningful scoring.

### 2. Derive tag candidates from corpus frequency

Don't guess the catalogue — let the corpus pick it. Read 50–100 titles + teasers first to
get a feel:

```sql
SELECT uid, title, LEFT(teaser, 200) FROM tx_news_domain_model_news
  WHERE pid=<PID> AND deleted=0 AND hidden=0
  ORDER BY datetime DESC LIMIT 100;
```

Then run a **frequency analysis** on the full target corpus (latest N news + their linked
`tt_content`). Brainstorm ~100 candidate concepts with 1–3 keywords each, count how many
news mention each, and pick the top ~65 (or whatever count you need). This is much more
defensible than a guessed catalogue and surfaces non-obvious recurring themes
(e.g. *Unternehmen* and *Polizei* ranked top-5 in the example corpus — neither was on
the original guess list).

**Single-concept rule.** Each tag should be ONE concept — never a `X & Y` combination.
Compose multiple tags per news instead. So:

| Avoid                          | Prefer                                         |
|--------------------------------|------------------------------------------------|
| `Banking & Konto`              | `Banking` + `Konto` (two tags)                 |
| `Künstliche Intelligenz & Deepfake` | `Künstliche Intelligenz` + `Deepfake`     |
| `Paket & Lieferung`            | `Paket` + `Lieferung` (+ `DHL` if relevant)    |
| `Reise & Urlaub`               | `Reise` + `Hotel` + `Flug`                     |

Hyphenated compounds (`Fake-Shop`, `Online-Shopping`, `Login-Daten`) and standard German
two-word concepts (`Künstliche Intelligenz`) are fine — they are one concept.

Each tag needs a *name*, a *slug* (lowercase, ASCII-only, hyphenated), and a curated list
of *keywords*. See `references/NewsThematicTags.example.php` for a worked German example
covering 65 single-concept fraud-prevention themes derived from a real ~1500-news corpus.

**Keyword design rules:**

- Lowercase. Both singular and plural where common (`fake-shop`, `fake-shops`).
- Both hyphenated and spaced spellings (`fake-shop`, `fake shop`, `fakeshop`).
- Compound nouns over generic single words (`kostenpflichtiges abo` over `kosten`).
- **Beware short prefixes**: `auto` matches `autor`, `automatisch`, `autorin` under the
  left-only word boundary. Use compound forms instead (`autokauf`, `autoverkauf`, `kfz`).
  Same trap with `apple` (`applied`), `bank` (`bankrott`), `post` (`posten`).
- 1–3 char ambiguous tokens are OK with strict both-sides boundaries (`tan`, `ki`, `sms`)
  — the example command auto-applies stricter boundaries for short keywords.
- 5–15 keywords per tag is a good target for single-concept tags; broaden if a tag is
  legitimately under-firing in the dry-run.
- Multi-word keywords are matched verbatim after whitespace collapse — be specific.

### 3. Decide on tag storage

For EXT:news, tags live on a **storage PID**. Use the same PID as the news (most common) — the
route enhancer in `config/sites/<id>/config.yaml` uses the tag's `slug`, not its PID. Verify your
site has the tag route wired:

```yaml
routeEnhancers:
  News:
    type: Extbase
    extension: News
    plugin: Pi1
    routes:
      - routePath: '/{tag-name}'
        _controller: 'News::list'
        _arguments:
          tag-name: overwriteDemand/tags
    aspects:
      tag-name:
        type: NewsTag
```

If not present, add it before publishing tag URLs. The `NewsTag` aspect type ships with
EXT:news and is the documented best practice; a plain `PersistedAliasMapper` with
`tableName: tx_news_domain_model_tag` and `routeFieldName: slug` is a legacy alternative.

### 4. Build a Symfony Console command

Create one command per extension/package in `Classes/Command/AssignNewsTagsCommand.php` and
register it in `Configuration/Services.yaml` with the `console.command` tag. See
`references/AssignNewsTagsCommand.example.php` for a complete, idempotent implementation that:

- loads the tag catalogue from a PHP config file
- upserts tags via **DataHandler** (slug auto-generates, refindex updated)
- harvests content from `tt_content` linked via `tx_news_related_news`
- normalizes HTML → lowercase → collapsed whitespace
- scores each tag by **distinct keyword matches** (not total occurrences — avoids spam from
  one repeated word dominating)
- selects the top N tags per news (5–10 typical, threshold ≥ 1)
- bulk-inserts MM rows via raw SQL multi-row `INSERT` (batch of 500)
- updates `tx_news_domain_model_news.tags` counter for backend list display
- supports `--dry-run`, `--reset`, `--limit`, `--storage-pid`, `--force`, `--debug-uid`

### 5. Iterate with `--dry-run`

```bash
ddev exec vendor/bin/typo3 cache:flush
ddev exec vendor/bin/typo3 <vendor>:news:assign-tags --dry-run --limit=300
```

The dry-run prints the **tags-per-news distribution** and **per-tag popularity**. Healthy
targets for fraud/news corpora:

- median 5+, p25 ≥ 3, p75 ≤ 8
- unmatched (0 tags) < 1% of corpus
- per-tag count: most-popular tag covers ≤ 60% of news; least-popular ≥ 1%

If many news fall to 1–2 tags, **broaden keywords** on common tags (E-Mail-Betrug, Banking,
Werbung — these typically anchor most scam stories). If a tag has 0 matches, either keywords
are wrong or the tag is not actually represented in the corpus — adjust or replace.

### 6. Run for real

```bash
ddev exec vendor/bin/typo3 <vendor>:news:assign-tags --reset --force
ddev exec vendor/bin/typo3 cache:flush
```

`--reset` truncates `tx_news_domain_model_news_tag_mm` and deletes tags on the storage PID
before recreating — safest for re-runs while iterating on keywords. Drop `--reset` for additive
runs once the catalogue is stable.

Expected throughput: **~150 news/sec** on a typical DDEV setup (1500 news ≈ 10 seconds).

### 7. Verify

```sql
-- 1. All tags present
SELECT COUNT(*) FROM tx_news_domain_model_tag WHERE pid=<PID> AND deleted=0;

-- 2. MM rows = sum(tags-per-news)
SELECT COUNT(*) FROM tx_news_domain_model_news_tag_mm;

-- 3. Distribution
SELECT tags_per_news, COUNT(*) AS news FROM (
  SELECT uid_local, COUNT(*) AS tags_per_news
  FROM tx_news_domain_model_news_tag_mm GROUP BY uid_local
) t GROUP BY tags_per_news ORDER BY tags_per_news;

-- 4. Counter consistency (must return 0 rows)
SELECT n.uid, n.tags, COUNT(mm.uid_foreign) AS actual
FROM tx_news_domain_model_news n
LEFT JOIN tx_news_domain_model_news_tag_mm mm ON mm.uid_local = n.uid
WHERE n.pid=<PID> AND n.deleted=0
GROUP BY n.uid, n.tags HAVING n.tags <> actual LIMIT 20;

-- 5. Per-tag popularity
SELECT t.title, COUNT(mm.uid_local) AS n
FROM tx_news_domain_model_tag t
LEFT JOIN tx_news_domain_model_news_tag_mm mm ON mm.uid_foreign = t.uid
WHERE t.pid=<PID> AND t.deleted=0
GROUP BY t.uid, t.title ORDER BY n DESC;

-- 6. Backend spot-check
SELECT n.uid, LEFT(n.title, 60), GROUP_CONCAT(t.title ORDER BY mm.sorting)
FROM tx_news_domain_model_news n
JOIN tx_news_domain_model_news_tag_mm mm ON mm.uid_local = n.uid
JOIN tx_news_domain_model_tag t ON t.uid = mm.uid_foreign
WHERE n.pid=<PID> AND n.deleted=0
GROUP BY n.uid ORDER BY n.datetime DESC LIMIT 10;
```

Backend visual check: open News module → pick a recent news → the "Relations" tab shows the
assigned tags (categories sit in the separate "Categories" tab). Frontend route check: visit
`https://<site>/<tag-slug>/`.

## Adding b13/tag (optional generic capability)

`b13/tag` provides a generic `sys_tag` table that can tag *any* record via an int `keywords`
column. It does **not** integrate with EXT:news tags and should not replace them.

```bash
ddev composer require b13/tag
ddev exec vendor/bin/typo3 extension:setup
ddev mysql -e "SHOW TABLES LIKE 'sys_tag%';"   # sys_tag + sys_tag_mm
```

To use it on a custom table:

1. Add `keywords int(11) unsigned DEFAULT '0' NOT NULL` to the table's SQL.
2. Configure TCA via `B13\Tag\TcaHelper`.
3. Register the field via `ExtensionManagementUtility::addToAllTCAtypes()`.

See the [b13/tag README](https://github.com/b13/tag) for current TCA wiring.

## 8. DBAL `createNamedParameter(PARAM_INT)` gotcha

In some DBAL stacks, `$qb->createNamedParameter($uid, Connection::PARAM_INT)`
**silently drops rows** when the integer is large (observed for UIDs in the tens of millions).
The query returns 0 rows even though the row exists. Reproduce in your environment before
adopting the workaround; on a clean TYPO3 v14 install with current Doctrine DBAL this may no
longer fire.

**Symptom.** `--debug-uid=29386376` returns "not found", but `SELECT … WHERE uid = 29386376`
in MySQL returns the row. The full `fetchNews()` query returns rows but the loop processes
*different* news than expected — the result set is silently truncated.

**Workaround.** Use raw SQL with `?` placeholders for queries that touch large integer columns
(news UIDs, tt_content UIDs, content element relations):

```php
// AVOID for large ints:
$qb->expr()->eq('uid', $qb->createNamedParameter($uid, Connection::PARAM_INT));

// PREFER:
$conn->executeQuery(
    'SELECT … FROM tx_news_domain_model_news WHERE uid = ?',
    [$uid]
)->fetchAssociative();

// For IN clauses with int arrays, inline the cast values:
$ids = implode(',', array_map(static fn($v) => (int)$v, $chunk));
$conn->executeQuery("SELECT … WHERE tx_news_related_news IN ($ids) AND …");
```

Small ints (PID, hidden, deleted) work fine with `createNamedParameter` — only large UIDs
exhibit the issue. The reference command applies this workaround throughout.

## 9. Performance notes

- **Tag upsert via DataHandler** for the 25 tag rows (slug eval, refindex) — negligible cost.
- **MM inserts via direct multi-row SQL** (batch 500). DataHandler MM writes are O(n²) per
  record and unnecessary for MM tables that have no TCA semantics.
- **Sort by `datetime DESC`** with `LIMIT N` to get the latest N news — index it if cold.
- **Chunk tt_content fetches** in groups of 200 news per IN-query to keep `max_allowed_packet`
  and prepared-statement parameter caps safe.
- Disable any caches that observe `tx_news_domain_model_news` during the run, then `cache:flush`
  afterwards. The reference command does **not** call DataHandler per news (only for tag
  upsert), so caches are minimally affected during the bulk pass.

## 10. Keyword matching — Unicode-safe word boundaries

PHP's `\b` is ASCII-only and breaks on `ä/ö/ü/ß`. Use `\p{L}\p{N}` lookarounds and the `/u`
modifier:

```php
private function buildKeywordPattern(string $keyword): string
{
    $quoted = preg_quote($keyword, '/');
    // Short tokens (<=3 chars): require both word boundaries to avoid false positives.
    // Longer tokens: require left boundary only — covers German plural/genitive and compound
    // suffixes (e.g. "phishing" matches "phishing-welle", "phishings", "phishingsoftware").
    if (mb_strlen($keyword, 'UTF-8') <= 3) {
        return '/(?<![\p{L}\p{N}])' . $quoted . '(?![\p{L}\p{N}])/u';
    }
    return '/(?<![\p{L}\p{N}])' . $quoted . '/u';
}
```

Score by **count of distinct matched keywords** — not total occurrences. A single keyword
repeated 50 times should not outweigh four different keywords matching once each.

## Files in this skill

- `references/AssignNewsTagsCommand.example.php` — complete, idempotent Symfony console
  command (~370 LOC) with all options, scoring logic, DataHandler upsert, bulk MM insert,
  DBAL workaround, `--debug-uid` per-news inspector, summary report.
- `references/NewsThematicTags.example.php` — 65 single-concept German fraud-prevention
  tags (no `X & Y` combinations), derived from a ~1500-news corpus frequency analysis,
  with ~5–15 curated keywords each.
- `references/Services.example.yaml` — minimal command registration snippet.

## Common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Median tags-per-news is 1–2 | Keywords too narrow; or `bodytext` empty without harvesting `tt_content` | Broaden top tags' keywords; verify `fetchContentByNews` is wired |
| Newest news (large UID) have 0 tags despite obvious keywords | DBAL `createNamedParameter(PARAM_INT)` truncation | Switch the affected query to raw SQL, see §8 |
| Tags exist but slugs are NULL | Created via direct INSERT instead of DataHandler | Use DataHandler with `process_datamap` so TCA slug eval fires |
| `tx_news_domain_model_news.tags` counter is wrong | Counter not updated after MM writes | Run an `UPDATE news SET tags = (SELECT COUNT(*) FROM mm WHERE mm.uid_local = news.uid)` once, then ensure command writes it |
| Frontend `/<tag-slug>/` 404s | Route enhancer missing in site config | Add the `News` route with the `NewsTag` aspect (§3) and flush caches |
| Identical tag created twice on re-run | Lookup-before-insert missing | `SELECT uid FROM tag WHERE slug = ?` before each DataHandler `NEW_x`; reuse UID if found |

## Acceptance checklist

Before reporting "done":

- [ ] Storage PID confirmed and tags created there
- [ ] `--dry-run` distribution reviewed (median ≥ 4, unmatched < 2%)
- [ ] Counter consistency query returns 0 rows
- [ ] Backend News module shows tags on a recent record
- [ ] `https://<site>/<tag-slug>/` resolves to the filtered news list
- [ ] Command is re-runnable (`--reset` works; second run is idempotent)
- [ ] If `b13/tag` was installed, `sys_tag` + `sys_tag_mm` exist and the extension is active
