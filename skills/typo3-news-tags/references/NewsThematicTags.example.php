<?php

declare(strict_types=1);

/**
 * Reference: 65 single-concept German tags for EXT:news in an Austrian internet-fraud
 * watchlist corpus (~1500 news on a single storage PID).
 *
 * Each tag is ONE concept (not "X & Y" combinations) — this is deliberate so that
 * `/<tag-slug>/` URLs read cleanly and so that backend editors can compose multiple
 * tags per news instead of memorising compound names.
 *
 * Catalogue was derived from a frequency analysis of the actual corpus (title + teaser
 * + linked tt_content harvested via tx_news_related_news) — see SKILL.md
 * §"Default workflow" steps 1–2. Tags are ordered roughly by descending corpus
 * frequency. Adjust the catalogue to your domain before adopting.
 *
 * Keyword design notes (see SKILL.md §"Keyword design rules"):
 *   - Short bare prefixes like 'auto' over-match in German (autor, automatisch, …).
 *     Prefer compound forms: autokauf, autoverkauf, autohändler, kfz, gebrauchtwagen.
 *   - 'min_per_news' is aspirational; the command accepts fewer if the corpus does
 *     not legitimately support 5 distinct themes for a given news.
 *
 * Consumed by Vendor\YourExt\Command\AssignNewsTagsCommand.
 */
return [
    'tags' => [
        // ── Communication channels & message types
        ['name' => 'E-Mail',                  'slug' => 'e-mail',                  'keywords' => ['e-mail', 'e-mailadresse', 'mailadresse', 'mailbox', 'posteingang', 'mailanhang', 'newsletter-betrug', 'gefälschte e-mail', 'betrügerische e-mail', 'spam-mail', 'mail-betrug']],
        ['name' => 'SMS',                     'slug' => 'sms',                     'keywords' => ['sms', 'sms-nachricht', 'kurznachricht', 'fake-sms', 'gefälschtes sms', 'betrügerisches sms']],
        ['name' => 'Spam',                    'slug' => 'spam',                    'keywords' => ['spam', 'spam-mail', 'spamfilter', 'unerwünschte werbung', 'spamming']],
        ['name' => 'Messenger',               'slug' => 'messenger',               'keywords' => ['messenger', 'messenger-dienst', 'messenger-nachricht', 'chat-nachricht']],
        ['name' => 'WhatsApp',                'slug' => 'whatsapp',                'keywords' => ['whatsapp', 'whatsapp-nachricht', 'whatsapp-gruppe', 'whatsapp-betrug']],
        ['name' => 'Telegram',                'slug' => 'telegram',                'keywords' => ['telegram', 'telegram-nachricht', 'telegram-gruppe', 'telegram-channel']],
        ['name' => 'Facebook',                'slug' => 'facebook',                'keywords' => ['facebook', 'fb-post', 'facebook-konto', 'facebook-anzeige', 'meta-konzern']],
        ['name' => 'Instagram',               'slug' => 'instagram',               'keywords' => ['instagram', 'insta', 'instagram-account', 'instagram-werbung', 'insta-story']],
        ['name' => 'TikTok',                  'slug' => 'tiktok',                  'keywords' => ['tiktok', 'tiktok-video', 'tiktok-werbung', 'tiktok-account']],
        ['name' => 'YouTube',                 'slug' => 'youtube',                 'keywords' => ['youtube', 'youtube-video', 'youtube-werbung', 'youtube-kanal']],

        // ── Attack types & scams
        ['name' => 'Phishing',                'slug' => 'phishing',                'keywords' => ['phishing', 'phishing-mail', 'phishingmail', 'phishing-falle', 'phishing-nachricht', 'phishing-welle', 'phishing-seite', 'phishing-versuch', 'phishing-link']],
        ['name' => 'Telefonbetrug',           'slug' => 'telefonbetrug',           'keywords' => ['telefonbetrug', 'telefontrick', 'telefonbetrüger', 'fake-anruf', 'betrügerischer anruf', 'vishing', 'cold-call', 'ping-anruf']],
        ['name' => 'Spoofing',                'slug' => 'spoofing',                'keywords' => ['spoofing', 'rufnummer-spoofing', 'caller-id-spoofing', 'gefälschte rufnummer', 'spoof']],
        ['name' => 'Erpressung',              'slug' => 'erpressung',              'keywords' => ['erpressung', 'erpresserisch', 'erpresserische e-mail', 'erpresserische nachricht', 'masturbationsvideo', 'sextortion', 'erpressungsversuch']],
        ['name' => 'Vorschussbetrug',         'slug' => 'vorschussbetrug',         'keywords' => ['vorschussbetrug', 'scam ', 'scamming', 'scammer', 'vorauszahlung', 'vorkasse', 'vorauskasse', 'vorab überweisen']],
        ['name' => 'Investmentbetrug',        'slug' => 'investmentbetrug',        'keywords' => ['investment', 'anlagebetrug', 'trading-plattform', 'rendite', 'investmentplattform', 'investmentfalle', 'investmentbetrug', 'aktien', 'anlage', 'broker', 'trading']],
        ['name' => 'Jobbetrug',               'slug' => 'jobbetrug',               'keywords' => ['jobbetrug', 'jobangebot', 'job-angebot', 'fake-job', 'fake-jobangebot', 'heimarbeit', 'nebenjob', 'minijob', 'task-scam', 'fake-jobinserat']],
        ['name' => 'Wohnungsbetrug',          'slug' => 'wohnungsbetrug',          'keywords' => ['wohnungsbetrug', 'fake-wohnung', 'wohnungsanzeige', 'mietbetrug', 'fake-vermieter']],
        ['name' => 'Ticketbetrug',            'slug' => 'ticketbetrug',            'keywords' => ['ticketbetrug', 'ticket-betrug', 'fake-ticket', 'fake-tickets', 'ticombo', 'hellotickets', 'ticketmasche']],
        ['name' => 'Markenmissbrauch',        'slug' => 'markenmissbrauch',        'keywords' => ['markenmissbrauch', 'gefälschte rechnung', 'fake-rechnung', 'impressumsdiebstahl', 'imitiert', 'imitieren', 'scheinfirma', 'fake-firma', 'unter dem namen', 'geben sich als']],
        ['name' => 'Identitätsdiebstahl',     'slug' => 'identitaetsdiebstahl',    'keywords' => ['identitätsdiebstahl', 'identitätsmissbrauch', 'identitätsbetrug', 'identitätsklau', 'identität gestohlen', 'ausweiskopie', 'ausweisdaten', 'personalausweis']],
        ['name' => 'Datendiebstahl',          'slug' => 'datendiebstahl',          'keywords' => ['datendiebstahl', 'datenklau', 'datenleak', 'datenleck', 'daten gestohlen', 'gestohlene daten']],
        ['name' => 'Login-Daten',             'slug' => 'login-daten',             'keywords' => ['logindaten', 'login-daten', 'zugangsdaten', 'passwort', 'benutzerkonto-zugang', 'login-seite', 'anmeldedaten', 'kontodaten preisgeben']],

        // ── Threats & malicious software
        ['name' => 'Schadsoftware',           'slug' => 'schadsoftware',           'keywords' => ['schadsoftware', 'schadprogramm', 'schadcode', 'schädlicher anhang']],
        ['name' => 'Virus',                   'slug' => 'virus',                   'keywords' => ['virus', 'computervirus', 'viren', 'virusinfektion']],
        ['name' => 'Trojaner',                'slug' => 'trojaner',                'keywords' => ['trojaner', 'trojanische', 'banking-trojaner']],
        ['name' => 'Deepfake',                'slug' => 'deepfake',                'keywords' => ['deepfake', 'deep fake', 'ki-manipulierte', 'manipulierter inhalt', 'gefälschtes video']],

        // ── Tech & AI
        ['name' => 'Künstliche Intelligenz',  'slug' => 'kuenstliche-intelligenz', 'keywords' => ['ki', 'künstliche intelligenz', 'chatgpt', 'gpt', 'ki-werbung', 'ki-anwendung', 'ki-systeme', 'gemini', 'ki-generiert', 'ki-tool', 'ki-modell']],
        ['name' => 'Smartphone',              'slug' => 'smartphone',              'keywords' => ['smartphone', 'handy', 'mobiltelefon', 'mobilgerät', 'tablet']],

        // ── Commerce & shopping
        ['name' => 'Fake-Shop',               'slug' => 'fake-shop',               'keywords' => ['fake-shop', 'fakeshop', 'fake shop', 'fake-shops', 'betrügerischer shop', 'scheinshop', 'fake-website', 'fake-webseite', 'problematischer shop']],
        ['name' => 'Online-Shopping',         'slug' => 'online-shopping',         'keywords' => ['online-shop', 'online-shopping', 'online einkauf', 'webshop', 'online-händler', 'online bestellen', 'online-bestellung', 'online kaufen']],
        ['name' => 'Kleinanzeigen',           'slug' => 'kleinanzeigen',           'keywords' => ['kleinanzeige', 'kleinanzeigen', 'willhaben', 'shpock', 'vinted', 'kleinanzeigenplattform', 'kleinanzeigen-portal']],
        ['name' => 'Marketplace',             'slug' => 'marketplace',             'keywords' => ['marketplace', 'amazon marketplace', 'marketplace-händler', 'marketplace-angebot', 'facebook-marketplace']],
        ['name' => 'Abo-Falle',               'slug' => 'abo-falle',               'keywords' => ['abo', 'abofalle', 'abo-falle', 'abonnement', 'kostenpflichtiges abo', 'jahresabo', 'monatsabo', 'kostenfalle', 'abo-vertrag']],
        ['name' => 'Gewinnspiel',             'slug' => 'gewinnspiel',             'keywords' => ['gewinnspiel', 'gewinn', 'lotto', 'preisausschreiben', 'jackpot', 'glücksspiel', 'gewinnbenachrichtigung', 'verlosung']],

        // ── Brands & global services
        ['name' => 'Amazon',                  'slug' => 'amazon',                  'keywords' => ['amazon', 'amazon-konto', 'amazon-bestellung', 'amazon-shop']],
        ['name' => 'eBay',                    'slug' => 'ebay',                    'keywords' => ['ebay', 'ebay-kleinanzeigen', 'ebay-shop', 'ebay-konto']],
        ['name' => 'PayPal',                  'slug' => 'paypal',                  'keywords' => ['paypal', 'paypal-zahlung', 'paypal-konto', 'paypal-rechnung']],
        ['name' => 'Microsoft',               'slug' => 'microsoft',               'keywords' => ['microsoft', 'windows-defender', 'microsoft-nachricht', 'outlook', 'microsoft-anruf']],
        ['name' => 'Apple',                   'slug' => 'apple',                   'keywords' => ['apple', 'apple-id', 'icloud', 'apple-konto', 'iphone']],
        ['name' => 'Google',                  'slug' => 'google',                  'keywords' => ['google', 'google-konto', 'google-suche', 'gmail', 'google-werbung']],

        // ── Finance & payment
        ['name' => 'Banking',                 'slug' => 'banking',                 'keywords' => ['banking', 'online-banking', 'onlinebanking', 'ebanking', 'banking-app', 'bank-app', 'bank-zugang', 'mobile-banking']],
        ['name' => 'Konto',                   'slug' => 'konto',                   'keywords' => ['konto', 'bankkonto', 'kontostand', 'kontonummer', 'kontodaten', 'kontoinhaber']],
        ['name' => 'Kreditkarte',             'slug' => 'kreditkarte',             'keywords' => ['kreditkarte', 'kreditkartendaten', 'kreditkartennummer', 'mastercard', 'visa', 'master card', 'kreditkartenbetrug']],
        ['name' => 'Kryptowährung',           'slug' => 'kryptowaehrung',          'keywords' => ['krypto', 'kryptowährung', 'kryptowährungen', 'krypto-plattform', 'crypto']],
        ['name' => 'Bitcoin',                 'slug' => 'bitcoin',                 'keywords' => ['bitcoin', 'btc', 'bitcoin-wallet', 'bitcoin-zahlung']],

        // ── Logistics & delivery
        ['name' => 'Paket',                   'slug' => 'paket',                   'keywords' => ['paket', 'paketbenachrichtigung', 'paketankündigung', 'paketzustellung', 'fake-paket', 'paket-mail', 'paket-sms']],
        ['name' => 'Lieferung',               'slug' => 'lieferung',               'keywords' => ['lieferung', 'zustellung', 'sortierzentrum', 'lieferdienst', 'lieferadresse', 'lieferverfolgung']],
        ['name' => 'DHL',                     'slug' => 'dhl',                     'keywords' => ['dhl', 'dhl-paket', 'dhl-zustellung']],

        // ── Travel
        ['name' => 'Reise',                   'slug' => 'reise',                   'keywords' => ['reise', 'urlaub', 'urlaubsbuchung', 'reisebuchung', 'reiseanbieter', 'pauschalreise', 'reisebüro']],
        ['name' => 'Hotel',                   'slug' => 'hotel',                   'keywords' => ['hotel', 'hotelbuchung', 'hotel-zimmer', 'hotelreservierung', 'unterkunft']],

        // ── Austrian authorities & entities
        ['name' => 'Polizei',                 'slug' => 'polizei',                 'keywords' => ['polizei', 'polizeidienststelle', 'polizei melden', 'polizeiliche anzeige', 'kriminalpolizei']],
        ['name' => 'Finanzamt',               'slug' => 'finanzamt',               'keywords' => ['finanzamt', 'finanzonline', 'finanzministerium', 'steuerausgleich', 'finanzpolizei']],
        ['name' => 'WKO',                     'slug' => 'wko',                     'keywords' => ['wko', 'wirtschaftskammer', 'wirtschaftskammern', 'wko-mail']],

        // ── Domains & sectors
        ['name' => 'Auto',                    'slug' => 'auto',                    'keywords' => ['kfz', 'gebrauchtwagen', 'fahrzeug', 'autokauf', 'autoverkauf', 'pkw', 'pkw-kauf', 'autohändler', 'automobil']],
        ['name' => 'Immobilien',              'slug' => 'immobilien',              'keywords' => ['immobilie', 'immobilien', 'haus zu mieten', 'wohnungsanzeige', 'immobilienagentur', 'immobilienmakler']],
        ['name' => 'Unternehmen',             'slug' => 'unternehmen',             'keywords' => ['unternehmer', 'unternehmen', 'firma', 'firmenname', 'gewerbetreibende', 'selbständige', 'betrieb']],
        ['name' => 'Bewerbung',               'slug' => 'bewerbung',               'keywords' => ['bewerbung', 'bewerber', 'bewerbungsverfahren', 'bewerbungsgespräch']],
        ['name' => 'Dating',                  'slug' => 'dating',                  'keywords' => ['dating', 'online-dating', 'datingportal', 'datingplattform', 'partnerbörse', 'liebesbetrug']],

        // ── Topics & themes
        ['name' => 'Werbung',                 'slug' => 'werbung',                 'keywords' => ['werbung', 'werbeanzeige', 'gesponserte werbung', 'banner-werbung', 'popup-werbung', 'werbebanner', 'irreführende werbung', 'fake-werbung']],
        ['name' => 'Datenschutz',             'slug' => 'datenschutz',             'keywords' => ['datenschutz', 'dsgvo', 'datenschutzrecht', 'datenschutzbestimmungen', 'datenschutzeinstellungen']],
        ['name' => 'Promi',                   'slug' => 'promi',                   'keywords' => ['promi', 'prominente', 'prominenter', 'promi-zitat', 'fake-zitat', 'elon musk', 'celebrity']],
        ['name' => 'Kinder',                  'slug' => 'kinder',                  'keywords' => ['kinder', 'jugendliche', 'minderjährige', 'eltern', 'schule', 'kinderbetreuung']],

        // ── Format
        ['name' => 'Webinar',                 'slug' => 'webinar',                 'keywords' => ['webinar', 'kostenloses webinar', 'online-seminar', 'live-webinar']],
        ['name' => 'Tipps',                   'slug' => 'tipps',                   'keywords' => ['tipps', 'so erkennen sie', 'so schützen sie sich', 'wie erkenne ich', 'was tun wenn', 'ratgeber', 'checkliste', 'so vermeiden sie', 'tipps und tricks']],
    ],
    'config' => [
        'min_per_news' => 5,
        'max_per_news' => 10,
        'storage_pid' => 70,
        'news_limit' => 1500,
        'score_threshold' => 1,
    ],
];
