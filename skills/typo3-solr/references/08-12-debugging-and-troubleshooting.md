# 12. Debugging & Troubleshooting

Continues `typo3-solr` from [full guide](full-guide.md).

## 12. Debugging & Troubleshooting

This section is the core reference for diagnosing and fixing EXT:solr issues. If you are new to EXT:solr, start with the step-by-step guide below before jumping to the reference sections.

### Step-by-Step Troubleshooting Guide (Beginner)

If search is not working and you have **no idea where to start**, follow these steps in order. Each step explains **what** you are checking, **where** to find it, and **what the result means**.

---

#### Step 1: Understand the Architecture

Before debugging, know how EXT:solr works. There are **four parts** that must all work:

```
┌─────────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1. Connection   │───▶│  2. Indexing  │───▶│  3. Solr Core │───▶│  4. Frontend  │
│  TYPO3 ↔ Solr    │    │  Queue+Worker │    │  Documents   │    │  Search+Fluid │
└─────────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

- **Connection**: TYPO3 must know where Solr is running (host, port, core name)
- **Indexing**: TYPO3 must send your content (pages, news, etc.) to Solr via the Index Queue and a Scheduler task
- **Solr Core**: The Solr server stores documents and makes them searchable
- **Frontend**: The search plugin sends queries to Solr and renders results via Fluid templates

A problem at **any** of these four parts breaks search. The steps below check each part from left to right.

---

#### Step 2: Is Solr Reachable? (Connection Check)

**Where:** TYPO3 Backend → Admin Tools → Reports → Status Report

**What you see:** A list of status checks. Look for entries about "Solr":
- **All green** ✅ = Solr is reachable, connection works → go to Step 3
- **Red/yellow** ⚠️ = Solr is not reachable → fix connection first

**If red -- things to check:**

Open your site configuration file `config/sites/<your-site>/config.yaml` and verify these settings:

```yaml
solr_enabled_read: true
solr_host_read: solr              # hostname where Solr runs
solr_port_read: '8983'            # port (8983 for standalone, 8984 for DDEV)
solr_scheme_read: http            # http or https (DDEV uses https)
solr_path_read: /                 # usually just /
solr_core_read: core_en           # must match the actual core name in Solr
```

**For DDEV users:**

```yaml
solr_host_read: <your-project>.ddev.site
solr_port_read: '8984'
solr_scheme_read: https
```

**Quick test from the terminal:**

```bash
# DDEV: test if Solr responds
ddev exec curl -s http://typo3-solr:8983/solr/core_en/admin/ping

# Expected: {"status":"OK"}
# If "Connection refused": Solr container is not running → ddev restart
```

**After fixing:** Always click "Initialize connection" in the EXT:solr backend module (Web → Search → Overview tab).

---

#### Step 3: Is Content in the Index Queue? (Indexing Check)

**Where:** TYPO3 Backend → Web → Search → "Index Queue" tab

**What you see:** A table showing record types (pages, news, etc.) with counts.

| What you see | What it means | What to do |
|-------------|---------------|------------|
| **Table is empty** | No content has been queued for Solr | You need to initialize the queue (see below) |
| **Items with count > 0, errors = 0** | Content is queued and indexed | Go to Step 4 |
| **Items with errors > 0** | Indexing failed for some records | Read the error messages (see below) |

**If the queue is empty:**

1. Check that EXT:solr TypoScript templates are included on the root page:
   - Backend → Web → Template module → root page → "Includes" tab
   - You must see "Search - Base Configuration" in the list
   - If it's missing, add it: click "Include static (from extensions)" and select "Search - Base Configuration (solr)"

2. Initialize the queue:
   - Go to Web → Search → "Index Queue" tab
   - Select the checkboxes for the record types you want to index (e.g., "pages")
   - Click "Queue selected content"
   - The table should now show a count

**If items have errors:**

The `errors` column tells you what went wrong. Common errors:

| Error message | What it means | Fix |
|---------------|---------------|-----|
| "Could not resolve host" | Solr server unreachable | Go back to Step 2 |
| "Document is missing mandatory uniqueKey field: id" | The document has no ID | Check your TypoScript field mapping |
| "OutOfMemoryError" | PHP or Solr ran out of memory | Increase `memory_limit` for the scheduler |
| "HTTP 404" | The Solr core doesn't exist | Check core name, run `ddev solrctl apply` |

---

#### Step 4: Have Documents Arrived in Solr? (Solr Check)

Even if the queue shows no errors, documents might not have been sent to Solr yet. The queue only fills the to-do list -- a **Scheduler task** actually sends them.

**Check if the Scheduler task exists:**
- Backend → System → Scheduler
- Look for a task called "Index Queue Worker" (class: `ApacheSolrForTypo3\Solr\Task\IndexQueueWorkerTask`)
- If it doesn't exist: create it (Add task → select "Index Queue Worker" → save)
- If it exists: check "Last execution" -- has it run recently?

**Run it manually now:**
- Click the "play" button next to the Index Queue Worker task

**Verify documents are in Solr:**

Open the Solr Admin UI:
- DDEV: run `ddev launch :8984` (opens in browser)
- Production: navigate to `http://your-solr-host:8983/solr/`

In Solr Admin UI:
1. Select your core from the dropdown (e.g., `core_en`)
2. Click "Query" in the left menu
3. Leave `q` as `*:*` (means "all documents")
4. Click "Execute Query"
5. Check `numFound` in the response:

| numFound | What it means | What to do |
|----------|---------------|------------|
| **0** | No documents at all | Scheduler task didn't run, or indexing failed silently → enable logging (see 12.0 Layer 2 below) |
| **> 0** | Documents exist in Solr | Go to Step 5 |

**Useful queries to run in Solr Admin:**

```
# How many documents per type?
q=*:*&rows=0&facet=true&facet.field=type

# Show 5 page documents with their key fields
q=*:*&fq=type:pages&rows=5&fl=uid,title,url,siteHash

# Search for a specific term
q=your search term&fl=uid,title,score
```

---

#### Step 5: Does the Frontend Show Results? (Frontend Check)

**Where:** Open the page with the search plugin in the frontend, type a search term you know exists in Solr.

| What you see | What it means | What to do |
|-------------|---------------|------------|
| **"Search is currently not available"** | Plugin can't connect to Solr | Go back to Step 2 -- connection issue from the frontend |
| **Search works, but 0 results** | Query runs but finds nothing | Check site hash, access field (see below) |
| **Results appear but wrong** | Documents found but wrong content/order | Check field mapping, boosting (see below) |
| **Results appear correctly** ✅ | Everything works! | Done |

**If 0 results even though Solr has documents:**

The most common cause is a **site hash mismatch**. EXT:solr adds a `siteHash` to every document to prevent cross-site contamination. If the hash during indexing differs from the hash during searching, no results appear.

Check in Solr Admin:
```
# What siteHash values exist in the index?
q=*:*&rows=0&facet=true&facet.field=siteHash
```

Compare Solr cores and TYPO3 site / **language** endpoints against the EXT:solr version you run — use Extension Settings + Site Configuration as documented for that major (names moved between releases).

If the hashes don't match: **re-index** (Backend → Web → Search → Index Queue → clear and re-queue all).

**Other causes of 0 results:**

- `plugin.tx_solr.search.targetPage` points to wrong page → set it to the page UID containing the search plugin
- `plugin.tx_solr.enabled` is `0` somewhere in TypoScript → check for override
- Access restrictions: the `access` field on documents doesn't match the frontend user → test in Solr Admin with `q=*:*&fl=uid,title,access`

---

#### Step 6: Something Else is Wrong -- Enable Logging

If the steps above didn't solve it, **enable logging** to see exactly what EXT:solr does:

**1. Add TypoScript logging** (on the root page, dev/staging only):

```typoscript
plugin.tx_solr.logging {
    debugOutput = 1
    exceptions = 1
    indexing = 1
    query.rawGet = 1
    query.queryString = 1
    query.searchWords = 1
}
```

**2. Write logs to a file** (in `config/system/additional.php`):

```php
$GLOBALS['TYPO3_CONF_VARS']['LOG']['ApacheSolrForTypo3']['Solr']['writerConfiguration'] = [
    \Psr\Log\LogLevel::DEBUG => [
        \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
            'logFile' => \TYPO3\CMS\Core\Core\Environment::getVarPath() . '/log/solr.log',
        ],
    ],
];
```

**3. Watch the log file:**

```bash
# DDEV
ddev exec tail -f var/log/solr.log

# Then trigger the action: run the scheduler, or do a search in the frontend
```

**What to look for in the log:**

- `[ERROR]` lines → these tell you exactly what failed
- `Solr raw GET: http://...` → the exact URL sent to Solr (paste it in a browser to test)
- `Response: 0 results` → Solr answered but found nothing (site hash? access? wrong field?)

**4. Also check:** Admin Tools → Log module (filter by component "ApacheSolrForTypo3")

---

#### Step 7: Still Stuck? Escalation Path

If all six steps above didn't solve it:

1. **Ask in Slack:** [TYPO3 Slack #ext-solr](https://typo3.slack.com/messages/ext-solr/) -- the maintainers (dkd) are active here
2. **Search GitHub Issues:** [TYPO3-Solr/ext-solr/issues](https://github.com/TYPO3-Solr/ext-solr/issues) -- your problem might already be reported
3. **dkd support:** [Professional support](https://www.dkd.de/en/products/solr-enterprise-search/) -- paid support from the extension maintainers
4. **Collect info for a bug report:** Solr version, EXT:solr version, PHP version, TYPO3 version, error messages from the log, Solr Admin query results

---
