<?php

declare(strict_types=1);

namespace Vendor\YourExt\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Core\Bootstrap;
use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;
use TYPO3\CMS\Core\Utility\GeneralUtility;

/**
 * Reference: assigns thematic tags to EXT:news records via keyword matching.
 *
 * Loads the tag catalogue from
 * EXT:<your_ext>/Resources/Private/Data/NewsThematicTags.php,
 * upserts each tag into tx_news_domain_model_tag (DataHandler-driven
 * so slugs auto-generate), then scans the latest N news on the given
 * storage PID, scores each tag by distinct keyword matches in
 * title + teaser + linked tt_content, and assigns the top 5..10 tags.
 *
 * IMPORTANT: This is a reference example. Before adopting it:
 *   - replace `Vendor\YourExt` with your namespace
 *   - update `loadConfig()` to point at your extension key
 *   - tune `self::CONTENT_TYPES` to match your tt_content harvest set
 *     (mask CTypes vary by project; verify with:
 *       SELECT CType, COUNT(*) FROM tt_content
 *         WHERE tx_news_related_news>0 AND deleted=0 AND hidden=0
 *         GROUP BY CType ORDER BY 2 DESC)
 *   - register in your Configuration/Services.yaml — see Services.example.yaml
 *
 * See SKILL.md §8 for the DBAL `createNamedParameter(PARAM_INT)` workaround
 * used in fetchNews(), fetchContentByNews() and the news.tags counter UPDATE.
 */
final class AssignNewsTagsCommand extends Command
{
    private const TAG_TABLE = 'tx_news_domain_model_tag';
    private const NEWS_TABLE = 'tx_news_domain_model_news';
    private const MM_TABLE = 'tx_news_domain_model_news_tag_mm';
    private const TT_CONTENT = 'tt_content';
    private const CONTENT_TYPES = [
        'text',
        'mask_text_icon',
        'mask_aufzaehlungbox',
        'mask_box_lamp',
        'mask_box_achtung',
    ];

    protected function configure(): void
    {
        $this
            ->setDescription('Assign generic German thematic tags to EXT:news records via keyword matching')
            ->addOption('dry-run', null, InputOption::VALUE_NONE, 'Compute assignments and print summary without writing anything')
            ->addOption('reset', null, InputOption::VALUE_NONE, 'Truncate MM and delete existing tags on the storage PID before processing')
            ->addOption('limit', null, InputOption::VALUE_OPTIONAL, 'Max news to process (default from config)')
            ->addOption('storage-pid', null, InputOption::VALUE_OPTIONAL, 'Storage PID (default from config)')
            ->addOption('force', null, InputOption::VALUE_NONE, 'Skip interactive confirmation for --reset')
            ->addOption('debug-uid', null, InputOption::VALUE_OPTIONAL, 'Print score breakdown and selected tags for one specific news UID, then exit');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $io->title('EXT:news thematic tag assignment');

        $config = $this->loadConfig();
        $dryRun = (bool)$input->getOption('dry-run');
        $reset = (bool)$input->getOption('reset');
        $force = (bool)$input->getOption('force');
        $storagePid = (int)($input->getOption('storage-pid') ?? $config['config']['storage_pid']);
        $limit = (int)($input->getOption('limit') ?? $config['config']['news_limit']);
        $minPer = (int)$config['config']['min_per_news'];
        $maxPer = (int)$config['config']['max_per_news'];
        $threshold = (int)$config['config']['score_threshold'];

        $io->writeln(sprintf(
            '<info>Storage PID:</info> %d   <info>Limit:</info> %d   <info>Tags catalogue:</info> %d   <info>Per-news:</info> %d..%d   <info>Mode:</info> %s',
            $storagePid,
            $limit,
            count($config['tags']),
            $minPer,
            $maxPer,
            $dryRun ? 'DRY-RUN' : 'WRITE'
        ));

        Bootstrap::initializeBackendAuthentication();

        $debugUid = $input->getOption('debug-uid') !== null ? (int)$input->getOption('debug-uid') : null;
        if ($debugUid !== null) {
            $this->debugSingleNews($debugUid, $storagePid, $config, $minPer, $maxPer, $threshold, $io);
            return Command::SUCCESS;
        }

        if ($reset) {
            if (!$dryRun && !$force && !$io->confirm(sprintf(
                'This deletes existing tags on PID %d and truncates %s. Continue?',
                $storagePid,
                self::MM_TABLE
            ), false)) {
                $io->warning('Aborted.');
                return Command::SUCCESS;
            }
            $this->resetTagsAndMm($storagePid, $dryRun, $io);
        }

        // Phase 1: upsert tags, build slug -> uid map
        $tagUidBySlug = $this->upsertTags($config['tags'], $storagePid, $dryRun, $io);

        // Phase 2: load news
        $newsRows = $this->fetchNews($storagePid, $limit);
        $io->writeln(sprintf('<info>Loaded %d news rows.</info>', count($newsRows)));
        if ($newsRows === []) {
            $io->warning('No news to process.');
            return Command::SUCCESS;
        }

        // Phase 3: load tt_content for all news (in chunks)
        $contentByNews = $this->fetchContentByNews(array_column($newsRows, 'uid'));
        $io->writeln(sprintf(
            '<info>Harvested tt_content for %d news (%d distinct content rows).</info>',
            count($contentByNews),
            array_sum(array_map('count', $contentByNews))
        ));

        // Phase 4: score + select + write
        $distribution = [];
        $perTagCount = array_fill_keys(array_keys($tagUidBySlug), 0);
        $unmatched = 0;
        $mmInsertCount = 0;
        $progress = $io->createProgressBar(count($newsRows));
        $progress->setFormat(' %current%/%max% [%bar%] %percent:3s%%  %elapsed:6s%/%estimated:-6s%  %message%');
        $progress->setMessage('');
        $progress->start();

        $connection = $this->getMmConnection();
        $newsConnection = $this->getNewsConnection();
        $batch = [];
        $batchLimit = 500;

        foreach ($newsRows as $news) {
            $text = $this->buildSearchText($news, $contentByNews[$news['uid']] ?? []);
            $scores = $this->scoreTags($text, $config['tags']);
            $selected = $this->selectTags($scores, $maxPer, $threshold);
            $count = count($selected);
            $distribution[] = $count;
            if ($count === 0) {
                $unmatched++;
            }
            foreach ($selected as $sortIndex => $tagSlug) {
                $perTagCount[$tagSlug]++;
                if (!$dryRun) {
                    $batch[] = [
                        'uid_local' => (int)$news['uid'],
                        'uid_foreign' => $tagUidBySlug[$tagSlug],
                        'sorting' => $sortIndex + 1,
                        'sorting_foreign' => $perTagCount[$tagSlug],
                    ];
                    $mmInsertCount++;
                    if (count($batch) >= $batchLimit) {
                        $this->flushMmBatch($connection, $batch);
                        $batch = [];
                    }
                }
            }
            if (!$dryRun) {
                // Use raw SQL: see fetchNews() comment about DBAL PARAM_INT misbinding.
                $newsConnection->executeStatement(
                    'UPDATE ' . self::NEWS_TABLE . ' SET tags = ?, tstamp = ? WHERE uid = ' . (int)$news['uid'],
                    [$count, time()]
                );
            }
            $progress->setMessage(sprintf('news=%d tags=%d', (int)$news['uid'], $count));
            $progress->advance();
        }
        if (!$dryRun && $batch !== []) {
            $this->flushMmBatch($connection, $batch);
        }
        $progress->finish();
        $io->newLine(2);

        $this->renderSummary($io, $distribution, $perTagCount, $tagUidBySlug, $config['tags'], $unmatched, $mmInsertCount, $dryRun);

        return Command::SUCCESS;
    }

    /**
     * @return array{tags: list<array{name:string,slug:string,keywords:list<string>}>, config: array<string,int>}
     */
    private function loadConfig(): array
    {
        // Replace 'your_ext' with your extension key.
        $path = ExtensionManagementUtility::extPath('your_ext') . 'Resources/Private/Data/NewsThematicTags.php';
        if (!is_file($path)) {
            // Fallback: composer-mode packages live in packages/<key>/ at repo root.
            $path = dirname(__DIR__, 2) . '/Resources/Private/Data/NewsThematicTags.php';
        }
        if (!is_file($path)) {
            throw new \RuntimeException('NewsThematicTags.php not found at expected path: ' . $path);
        }
        /** @var array $config */
        $config = require $path;
        return $config;
    }

    private function resetTagsAndMm(int $storagePid, bool $dryRun, SymfonyStyle $io): void
    {
        if ($dryRun) {
            $io->writeln('<comment>[dry-run] would TRUNCATE ' . self::MM_TABLE . ' and DELETE ' . self::TAG_TABLE . ' WHERE pid=' . $storagePid . '</comment>');
            return;
        }
        $mm = $this->getMmConnection();
        $mm->truncate(self::MM_TABLE);
        $tagConn = $this->getTagConnection();
        $tagConn->delete(self::TAG_TABLE, ['pid' => $storagePid]);
        $newsConn = $this->getNewsConnection();
        $newsConn->executeStatement(
            'UPDATE ' . self::NEWS_TABLE . ' SET tags = 0 WHERE pid = :pid',
            ['pid' => $storagePid]
        );
        $io->writeln('<info>Reset done.</info>');
    }

    /**
     * @param list<array{name:string,slug:string,keywords:list<string>}> $tags
     * @return array<string,int> map slug -> uid
     */
    private function upsertTags(array $tags, int $storagePid, bool $dryRun, SymfonyStyle $io): array
    {
        $conn = $this->getTagConnection();

        $existing = [];
        foreach ($conn->select(['uid', 'slug', 'title'], self::TAG_TABLE, ['pid' => $storagePid, 'deleted' => 0])->fetchAllAssociative() as $row) {
            $existing[$row['slug']] = (int)$row['uid'];
        }

        $toCreate = [];
        foreach ($tags as $tag) {
            if (!isset($existing[$tag['slug']])) {
                $toCreate[] = $tag;
            }
        }

        if ($toCreate === []) {
            $io->writeln(sprintf('<info>All %d tags already present.</info>', count($tags)));
            return $existing;
        }

        if ($dryRun) {
            $io->writeln('<comment>[dry-run] would create ' . count($toCreate) . ' tag(s).</comment>');
            // Provide placeholder UIDs so scoring/selection runs and summary is meaningful.
            $next = 1000000;
            $map = $existing;
            foreach ($toCreate as $tag) {
                $map[$tag['slug']] = $next++;
            }
            return $map;
        }

        $data = [];
        $placeholders = [];
        foreach ($toCreate as $idx => $tag) {
            $key = 'NEW_tag_' . $idx;
            $placeholders[$key] = $tag;
            $data[self::TAG_TABLE][$key] = [
                'pid' => $storagePid,
                'title' => $tag['name'],
                'slug' => $tag['slug'],
                'hidden' => 0,
                'sys_language_uid' => 0,
            ];
        }

        $dh = GeneralUtility::makeInstance(DataHandler::class);
        $dh->start($data, []);
        $dh->process_datamap();
        if ($dh->errorLog !== []) {
            foreach ($dh->errorLog as $err) {
                $io->warning('DataHandler: ' . $err);
            }
        }

        // Resolve assigned UIDs
        $map = $existing;
        foreach ($placeholders as $key => $tag) {
            $resolved = $dh->substNEWwithIDs[$key] ?? null;
            if ($resolved) {
                $map[$tag['slug']] = (int)$resolved;
            }
        }

        // Final reconciliation in case substitution map missed anything
        foreach ($conn->select(['uid', 'slug'], self::TAG_TABLE, ['pid' => $storagePid, 'deleted' => 0])->fetchAllAssociative() as $row) {
            if (!isset($map[$row['slug']])) {
                $map[$row['slug']] = (int)$row['uid'];
            }
        }

        $io->writeln(sprintf('<info>Created %d new tag(s) via DataHandler.</info>', count($toCreate)));
        return $map;
    }

    /**
     * @return list<array{uid:int,title:string,teaser:string,bodytext:string}>
     */
    private function fetchNews(int $storagePid, int $limit): array
    {
        $conn = $this->getNewsConnection();
        // Use raw SQL: DBAL's createNamedParameter(PARAM_INT) silently misbinds
        // large integers in this stack (loses rows for large uids during IN/EQ).
        $rows = $conn->executeQuery(
            'SELECT uid, title, teaser, bodytext FROM ' . self::NEWS_TABLE
            . ' WHERE pid = ? AND deleted = 0 AND hidden = 0'
            . ' ORDER BY datetime DESC LIMIT ' . (int)$limit,
            [$storagePid]
        )->fetchAllAssociative();

        return array_map(static fn(array $r): array => [
            'uid' => (int)$r['uid'],
            'title' => (string)($r['title'] ?? ''),
            'teaser' => (string)($r['teaser'] ?? ''),
            'bodytext' => (string)($r['bodytext'] ?? ''),
        ], $rows);
    }

    /**
     * @param list<int> $newsUids
     * @return array<int, list<string>>  newsUid -> list of text snippets
     */
    private function fetchContentByNews(array $newsUids): array
    {
        $result = [];
        $chunks = array_chunk($newsUids, 200);
        $conn = $this->getNewsConnection();
        $cTypeList = "'" . implode("','", array_map(static fn(string $s): string => addslashes($s), self::CONTENT_TYPES)) . "'";
        foreach ($chunks as $chunk) {
            // Build an inline IN list of integers (already cast). Raw SQL avoids
            // the DBAL PARAM_INT_ARRAY large-int misbinding seen elsewhere.
            $intIds = implode(',', array_map(static fn($v) => (int)$v, $chunk));
            if ($intIds === '') {
                continue;
            }
            $sql = 'SELECT tx_news_related_news AS news, bodytext, tx_mask_text, header'
                . ' FROM ' . self::TT_CONTENT
                . ' WHERE tx_news_related_news IN (' . $intIds . ')'
                . ' AND deleted = 0 AND hidden = 0'
                . ' AND CType IN (' . $cTypeList . ')';
            foreach ($conn->executeQuery($sql)->fetchAllAssociative() as $row) {
                $uid = (int)$row['news'];
                $parts = array_filter([
                    (string)($row['header'] ?? ''),
                    (string)($row['bodytext'] ?? ''),
                    (string)($row['tx_mask_text'] ?? ''),
                ], static fn($s) => $s !== '');
                if ($parts !== []) {
                    $result[$uid][] = implode(' ', $parts);
                }
            }
        }
        return $result;
    }

    /**
     * @param array{uid:int,title:string,teaser:string,bodytext:string} $news
     * @param list<string> $contentSnippets
     */
    private function buildSearchText(array $news, array $contentSnippets): string
    {
        $raw = $news['title'] . ' ' . $news['teaser'] . ' ' . $news['bodytext'] . ' ' . implode(' ', $contentSnippets);
        $stripped = strip_tags($raw);
        $decoded = html_entity_decode($stripped, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $lower = mb_strtolower($decoded, 'UTF-8');
        // Collapse whitespace (incl. NBSP) to single spaces.
        return trim((string)preg_replace('/[\s\xC2\xA0]+/u', ' ', $lower));
    }

    /**
     * @param list<array{name:string,slug:string,keywords:list<string>}> $tags
     * @return array<string,int>  tagSlug -> score (distinct keyword matches)
     */
    private function scoreTags(string $text, array $tags): array
    {
        $scores = [];
        foreach ($tags as $tag) {
            $score = 0;
            foreach ($tag['keywords'] as $kw) {
                $kwLower = mb_strtolower($kw, 'UTF-8');
                $pattern = $this->buildKeywordPattern($kwLower);
                if (@preg_match($pattern, $text) === 1) {
                    $score++;
                }
            }
            $scores[$tag['slug']] = $score;
        }
        return $scores;
    }

    private function buildKeywordPattern(string $keyword): string
    {
        $quoted = preg_quote($keyword, '/');
        // Short tokens (<=3 chars): require both word boundaries to avoid false positives.
        // Longer tokens: require left boundary only — covers German plural/genitive
        // and compound suffixes (e.g. "phishing" matches "phishing-welle", "phishings").
        if (mb_strlen($keyword, 'UTF-8') <= 3) {
            return '/(?<![\p{L}\p{N}])' . $quoted . '(?![\p{L}\p{N}])/u';
        }
        return '/(?<![\p{L}\p{N}])' . $quoted . '/u';
    }

    /**
     * @param array<string,int> $scores
     * @return list<string>  ordered list of tag slugs (highest score first), capped at $max
     */
    private function selectTags(array $scores, int $max, int $threshold): array
    {
        $filtered = array_filter($scores, static fn(int $s) => $s >= $threshold);
        // Sort by score DESC, then slug ASC for deterministic ordering.
        uksort($filtered, static function ($a, $b) use ($filtered) {
            $cmp = $filtered[$b] <=> $filtered[$a];
            return $cmp !== 0 ? $cmp : strcmp($a, $b);
        });
        return array_slice(array_keys($filtered), 0, $max);
    }

    /**
     * @param list<array{uid_local:int,uid_foreign:int,sorting:int,sorting_foreign:int}> $batch
     */
    private function flushMmBatch(Connection $connection, array $batch): void
    {
        if ($batch === []) {
            return;
        }
        // Build a single multi-row INSERT for speed; parameter count well under MariaDB limits.
        $columns = ['uid_local', 'uid_foreign', 'sorting', 'sorting_foreign'];
        $placeholders = [];
        $params = [];
        $i = 0;
        foreach ($batch as $row) {
            $placeholders[] = sprintf('(:l%1$d, :f%1$d, :s%1$d, :sf%1$d)', $i);
            $params['l' . $i] = $row['uid_local'];
            $params['f' . $i] = $row['uid_foreign'];
            $params['s' . $i] = $row['sorting'];
            $params['sf' . $i] = $row['sorting_foreign'];
            $i++;
        }
        $sql = 'INSERT INTO ' . self::MM_TABLE . ' (' . implode(', ', $columns) . ') VALUES ' . implode(', ', $placeholders);
        $connection->executeStatement($sql, $params);
    }

    /**
     * @param list<int> $distribution
     * @param array<string,int> $perTagCount
     * @param array<string,int> $tagUidBySlug
     * @param list<array{name:string,slug:string,keywords:list<string>}> $tags
     */
    private function renderSummary(
        SymfonyStyle $io,
        array $distribution,
        array $perTagCount,
        array $tagUidBySlug,
        array $tags,
        int $unmatched,
        int $mmInsertCount,
        bool $dryRun
    ): void {
        $total = count($distribution);
        sort($distribution);
        $min = $distribution[0] ?? 0;
        $max = $distribution[$total - 1] ?? 0;
        $median = $total > 0 ? $distribution[(int)floor($total / 2)] : 0;
        $p25 = $total > 0 ? $distribution[(int)floor($total * 0.25)] : 0;
        $p75 = $total > 0 ? $distribution[(int)floor($total * 0.75)] : 0;
        $avg = $total > 0 ? round(array_sum($distribution) / $total, 2) : 0.0;

        $io->section('Distribution (tags per news)');
        $io->definitionList(
            ['total news' => (string)$total],
            ['min' => (string)$min],
            ['p25' => (string)$p25],
            ['median' => (string)$median],
            ['p75' => (string)$p75],
            ['max' => (string)$max],
            ['avg' => (string)$avg],
            ['unmatched (0 tags)' => (string)$unmatched],
            ['MM rows ' . ($dryRun ? 'would insert' : 'inserted') => (string)$mmInsertCount],
        );

        $buckets = [];
        foreach ($distribution as $d) {
            $buckets[$d] = ($buckets[$d] ?? 0) + 1;
        }
        ksort($buckets);
        $rows = [];
        foreach ($buckets as $count => $newsCount) {
            $rows[] = [$count, $newsCount];
        }
        $io->table(['tags per news', 'news'], $rows);

        $io->section('Per-tag popularity');
        $tagsByName = [];
        foreach ($tags as $t) {
            $tagsByName[$t['slug']] = $t['name'];
        }
        $rows = [];
        arsort($perTagCount);
        foreach ($perTagCount as $slug => $n) {
            $rows[] = [
                $tagsByName[$slug] ?? $slug,
                $slug,
                $tagUidBySlug[$slug] ?? 0,
                $n,
            ];
        }
        $io->table(['Tag', 'Slug', 'UID', 'News'], $rows);
        if ($dryRun) {
            $io->note('Dry-run only — no rows written.');
        } else {
            $io->success(sprintf('Tagged %d news with %d MM rows.', $total, $mmInsertCount));
        }
    }

    private function debugSingleNews(int $uid, int $storagePid, array $config, int $minPer, int $maxPer, int $threshold, SymfonyStyle $io): void
    {
        $conn = $this->getNewsConnection();
        $row = $conn->executeQuery(
            'SELECT uid, pid, hidden, deleted, title, teaser, bodytext FROM ' . self::NEWS_TABLE . ' WHERE uid = ?',
            [$uid]
        )->fetchAssociative();
        if (!$row) {
            $io->error('news uid not found via raw SQL');
            return;
        }
        $io->writeln(sprintf('uid=%d pid=%d hidden=%d deleted=%d', (int)$row['uid'], (int)$row['pid'], (int)$row['hidden'], (int)$row['deleted']));
        $io->writeln('title: ' . $row['title']);
        $io->writeln('teaser: ' . mb_substr((string)$row['teaser'], 0, 200) . '…');

        $content = $this->fetchContentByNews([(int)$row['uid']]);
        $news = [
            'uid' => (int)$row['uid'],
            'title' => (string)($row['title'] ?? ''),
            'teaser' => (string)($row['teaser'] ?? ''),
            'bodytext' => (string)($row['bodytext'] ?? ''),
        ];
        $text = $this->buildSearchText($news, $content[(int)$row['uid']] ?? []);
        $io->writeln('normalized text (first 400 chars): ' . mb_substr($text, 0, 400));
        $io->newLine();

        $scores = $this->scoreTags($text, $config['tags']);
        $rows = [];
        foreach ($config['tags'] as $tag) {
            $rows[] = [$tag['name'], $tag['slug'], $scores[$tag['slug']] ?? 0];
        }
        usort($rows, static fn($a, $b) => $b[2] <=> $a[2]);
        $io->table(['Tag', 'Slug', 'Score'], $rows);

        $selected = $this->selectTags($scores, $maxPer, $threshold);
        $io->writeln('Selected tags (top ' . $maxPer . ', threshold ' . $threshold . '): ' . implode(', ', $selected));
    }

    private function getMmConnection(): Connection
    {
        return GeneralUtility::makeInstance(ConnectionPool::class)->getConnectionForTable(self::MM_TABLE);
    }

    private function getTagConnection(): Connection
    {
        return GeneralUtility::makeInstance(ConnectionPool::class)->getConnectionForTable(self::TAG_TABLE);
    }

    private function getNewsConnection(): Connection
    {
        return GeneralUtility::makeInstance(ConnectionPool::class)->getConnectionForTable(self::NEWS_TABLE);
    }
}
