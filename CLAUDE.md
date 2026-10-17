# Physio Exam Atlas — project guide for Claude Code

Static site that turns Physiotutors' physical-examination videos into one course-style
single-page library (all regions, chapters 00–05, sidebar filters, accuracy table), with Traditional Chinese (台灣用語) notes and English
medical terms kept alongside. Live at https://alice870902.github.io/physio-exam-atlas/
(GitHub Pages, branch `main`, root). Owner: Wulin, rehabilitation medicine R1.

## Status

| Region | State | Notes |
|---|---|---|
| cervical | **live** (25 entries, 6 categories) | first region on the page; 16 'Cervical Spine Assessment' + 1 'Cervical Spine' (referred pain) + 6 'Spine Assessment' upper-cervical ligament/VBI pages + 1 'Neurological Assessment' (Lhermitte) = 24 new pages, plus a deliberate parallel copy of `upper-limb-tension-test-1` (lives in wrist/ultt; groupC/zh_3). Added 2026-10-17 as groupA/groupB/groupC + zh_1/zh_2/zh_3. Headache (7) and Dizziness (14) pages are NOT here: owner decided 2026-10-17 they become their own regions later. Source quirks (upper-cervical-flexion page header reads 'Valgus Stress Test for MCL Injuries'; lateral-shear page cites only the BPPV guideline and mixes alar/transverse ligament; Spurling A specificity 83% vs 86% on two pages; neck tornado 2019 vs 2017; Domenech 2015 vs 2011; shoulder-abduction cites Rubinstein 2006 but lists Wainner) are flagged in record notes |
| headache | **live** (7 videos, 3 categories) | after cervical; all 7 'Headache' wiki pages (ICHD-3 criteria pages for tension-type, migraine, cluster, cervicogenic, medication overuse; cervicogenic mechanism; Watson headache test). Owner decided 2026-10-17: own region, not merged into cervical. Only the Watson test is a physical test; the others are criteria/explanation pages (accuracy n/a). Source quirks (TTH page lists medication overuse among primary headaches; CGH-explained body heading copied from the referred-pain post; subtype table is an image) are flagged in notes |
| dizziness | **live** (14 videos, 5 categories) | after headache; 9 'Dizziness Assessment' + 2 'Dizziness & Vertigo' (Dix-Hallpike, supine head roll) + 3 'Dizziness & Vertigo Treatment' (Epley, Semont, BBQ roll; treatment pages, accuracy n/a). Owner decided 2026-10-17: own region. Source quirks (Semont page says 'Epley can lead to nausea'; BBQ page's background says posterior canal 85-95%; Treleaven 2019 vs 2020; head impulse page gives no positive criterion) are flagged in notes |
| shoulder | **live** (92 videos, 10 categories) | redirect page; all 81 'Shoulder Assessment' wiki pages are in (18 backfilled 2026-10-17 as groupE/zh_4) |
| elbow | **live** (28 videos, 6 categories) | redirect page; all 28 'Elbow Assessment' wiki pages are in (added 2026-10-17 as groupA/zh_1). `biceps-squeeze-test` and `biceps-crease-interval` are deliberately in both shoulder (biceps) and elbow (biceps); `shoulder-internal-rotation-test` (cubital tunnel) lives in elbow only. Source quirks (PL rotatory drawer and tabletop relocation share a YouTube ID; varus test cites a BPPV guideline; PEPPER/SALT report PPV/NPV only; Ludington is a proximal test filed under elbow) are flagged in record notes |
| wrist | **live** (32 videos, 8 categories) | redirect page; 20 'Wrist & Hand Assessment' + 7 'Hand/Wrist Assessment' + 1 'Wrist & Hand' (ULTT4) + 3 'Basic Assessment' wrist/hand ROM-strength pages + `upper-limb-tension-test-1` (source files it under Cervical Spine Assessment; owner decided 2026-10-17 to keep all four ULTTs together here and parallel them into cervical later). Added 2026-10-17 as groupA/groupB + zh_1/zh_2. Source quirks (all four ULTT pages share YouTube ID rir6x6Iiqc4; ULTT3 page quotes Wainner figures under the name ULTT1; DRUJ page's accuracy sentence names the LT ballottement test; Eichhoff page repeats Finkelstein staging text; Sela cited as 2017 but listed as 2019; Allen test comma decimals) are flagged in record notes |
| hip | **live** (61 videos, 8 categories) | redirect page; all 43 'Hip Assessment' wiki pages are in (19 backfilled 2026-10-17 as groupE/zh_4); source quirks (Pace page duplicates FAIR procedure, resisted-external-derotation page duplicates Puranen-Orava, compression/sacral-thrust and Kendall/Phelps share YouTube IDs) are flagged in record notes |
| knee | **live** (61 videos, 12 categories) | redirect page; 50 'Knee Assessment' wiki pages + screening/RTP/rehab pages; source quirks (duck-walk, decline-step-down, Renne pages duplicate other pages' procedures; varus page titled 'Valgus') flagged in record notes |
| ankle | **live** (34 videos, 8 categories) | redirect page; all 25 'Ankle & Foot Assessment' + 6 'Ankle/Foot Assessment' + 2 'Ankle & Foot Treatment' + 1 'Ankle & Foot Exercises' wiki pages are in (added 2026-10-17 as groupA/groupB + zh_1/zh_2). Source quirks (heel thrust and forced dorsiflexion share YouTube ID IbRCCIDa5-8; fibular translation cites Beumer 2011 in text but lists 2002; syndesmosis incidence quoted as 1% / ~25% / 1-24% on different pages; cuboid syndrome page is a treatment technique filed under assessment; hop test states no positive criterion; Tinel ankle describes only one of two sites; heel thrust reference list empty) are flagged in record notes |
| lumbar | **live** (36 videos, 8 categories) | redirect page; 24 'Lumbar Spine Assessment' pages + referred pain, fracture red flags, Babinski, 4 SIJ pages not in hip, CPRs, direction-specific exercises; `myotomes-lower-limb` is deliberately in both knee and lumbar; SIJ provocation tests stay in hip |
| screen | **live** (31 entries, 8 categories) | cross-region 'Screening' region placed after lumbar; 26 new wiki pages (12 cranial nerves, Hoffmann + inverted supinator, Canadian C-spine, NEXUS, elbow extension, Caradeniz wrist, patellar-pubic percussion, fulcrum, 5 ankle/foot fracture rules, tuning fork) + 5 deliberate parallel copies of pages that also live in knee (`ottawa-knee-rules`, `pittsburgh-decision-rule`) and lumbar (`closed-fist-percussion-test`, `supine-sign`, `babinski-sign`). Added 2026-10-17 as groupA (new) / groupB (copies) + zh_1 / zh_2. Source quirks (CN III/IV/VI share one video, CN IX/X share one video, Ottawa ankle page joins tenderness AND inability to walk with 'and', 'low sensitivity' wording on Ottawa ankle/midfoot pages, Caradeniz vs Karadeniz spelling, Kerr 2010 not in optic references) are flagged in record notes |

## Repo layout

```
index.html                 built single-page site — DO NOT edit by hand, rebuild from src/
<region>/index.html        built redirect stubs → ../#region-<id> (or ../#test-<slug> if a hash is present)
src/site_template.html     single-page template; build replaces __DATA__, __N_TESTS__, __N_REGIONS__, __N_TOPICS__, __N_ACC__
src/build_site.py          python3 src/build_site.py   (no args) → writes index.html + 11 redirect pages
src/data/<region>/
  categories.json          [{id, zh, en, slugs:[...]}]  ← defines order & grouping
  group*.json              English source records fetched from physiotutors (any number of files)
  zh_*.json                Traditional Chinese notes (any number of files)
  slugs.json               (hip only) discovery list of candidate slugs
.nojekyll                  keep; GitHub Pages must not run Jekyll
```

Rebuild everything: `python3 src/build_site.py` (prints stats; fails loudly if a slug is missing
from zh/group or a category has no theme). Adding a region = add its data folder, append it to
`REGIONS` and map its category ids in `THEMES` inside build_site.py, update the hard-coded region
lists in site_template.html (hero lead, chapter cards, 02 intro, 目錄 drawer), rebuild, commit, push.
The old per-region `build.py` / `template.html` were removed in the 2026-10-17 redesign.

## Data pipeline (what was done for shoulder; repeat per region)

1. **Discover slugs.** Physiotutors has a WordPress REST API that is the reliable source:
   `https://www.physiotutors.com/wp-json/wp/v2/wiki?search=<term>&per_page=20`
   Response bodies are large (Yoast + ACF); fetch tools truncate after ~5 items, so page
   with `&per_page=5&page=N` (out-of-range page returns HTTP 400 = end).
   `https://www.physiotutors.com/wiki-sitemap.xml` is also useful for a full slug sweep.
   Do not scrape the YouTube channel directly: it was blocked from this environment and
   the wiki is better structured (one page = one test = one video).
2. **Fetch each record.** `…/wp-json/wp/v2/wiki?slug=<slug>` → take `id`, `title`, `link`,
   every YouTube ID in the `acf` embeds, and write an English summary in your own words:
   `{slug,id,title,link,youtube_ids:[],purpose,structure,procedure,positive,
     accuracy:{sensitivity,specificity,lr_plus,lr_minus,source},notes,status}`
   Put "not reported"/"n/a" where the page has nothing. If LR is derived from Sn/Sp rather
   than stated, mark it "(derived)". Flag source typos (e.g. shoulder Neer specificity "6%").
3. **Categorize.** Write `categories.json`. Order = learning order (overview/ROM first,
   then pathology groups, exercises last). Every slug must appear exactly once.
4. **Translate.** Produce `zh_*.json` records:
   `{slug,title_zh,purpose_zh,structure_zh,procedure_zh,positive_zh,notes_zh,tags}`
   Rules the owner asked for:
   - `title_zh` = `中文名稱 + 空格 + 英文原名` (e.g. `空罐測試 Empty Can Test`). build_site.py
     splits on the trailing Latin run to get `name_zh` and `title_en`, so the English part
     must come last and contain only `[A-Za-z0-9 '’()|/-]`.
   - Every medical term bilingual on first mention: 棘上肌 (supraspinatus), 盂唇 (labrum),
     肩峰下疼痛症候群 (subacromial pain syndrome, SAPS). Test names referenced in notes too.
   - Eponyms with no established Chinese name: keep as `Hawkins-Kennedy 測試`, `O'Brien 測試`.
   - procedure_zh 2–4 concrete sentences; notes_zh = clinical pearls, cluster use,
     reliability caveats. Faithful to source, no invented findings.
   - tags: 2–4 short bilingual tags, e.g. `"棘上肌 supraspinatus"`, `"SAPS"`, `"cluster"`.
5. **Build, check, commit, push.** `git push origin main` deploys automatically.

Shoulder was done with ~4 parallel fetch workers (≈20 slugs each) and 3 translate
workers (≈25 slugs each); each worker writes its own groupX.json / zh_N.json.

## Page behaviour (site_template.html)

Layout mirrors a course-library site: sticky header (chapter links, Aa font-size 100/120/135%
stored in localStorage `pa-font`), hero with region buttons + a sample card (`SAMPLE_SLUG`),
stats row, chapter cards, 使用須知, then chapters:
- 01 依主題: 8 cross-region themes (`THEMES` in build_site.py; the 8th, 頭痛、眩暈與前庭, holds every headache/dizziness category) → list → detail.
- 02 依部位: regions → categories → list → detail. Hash routing: `#region-<id>`,
  `#test-<slug>` or `#test-<region>/<slug>` (slug alone picks the first region that has it).
- 03 全部影片庫: full-text search (zh/en titles, purpose, structure, notes, tags) + region/theme selects.
- 04 診斷準確度總表: sortable table (numeric sort on first number in the Sn/Sp/LR string,
  "not reported" always last), region filter, "只看有數字的", search; names link to `#test-…`.
- 05 專業來源; floating 目錄 drawer (Esc closes).
Detail = chips, 中文名 / English name, 原始來源 link, YouTube `youtube-nocookie.com/embed/<id>`
iframes (lazy), four 逐段筆記 cards (目的與檢測結構 / 操作步驟 / 陽性判讀 / 診斷準確度) + 臨床重點與備註;
sentences containing ⚠ render as orange warning boxes; 中文/EN toggle swaps the body text.
No progress tracking (owner decided 2026-10-17). Light/dark via `prefers-color-scheme`;
Google Fonts Noto Serif TC + Noto Sans TC; no framework; one self-contained HTML.

## Conventions and gotchas

- Videos are only embedded, never downloaded; keep the copyright footer line.
- The build asserts every placeholder (`__DATA__`, `__N_*__`) exists in site_template.html.
- Region names: zh/en pairs used so far — 頸椎 Cervical spine, 頭痛 Headache, 眩暈 Dizziness & Vertigo, 肩部 Shoulder, 肘部 Elbow, 腕手 Wrist & Hand, 髖部 Hip, 膝部 Knee, 踝足 Ankle & Foot, 腰椎 Lumbar spine, 篩檢 Screening (cross-region).
- Counts on the page are all computed by build_site.py; nothing is hand-written.
- Commit messages: short imperative English summary; the owner writes in Traditional Chinese
  in conversation.

## Suggested next steps

All eight body regions, headache, dizziness and the cross-region screening section (cervical, headache, dizziness, shoulder, elbow, wrist, hip, knee, ankle, lumbar, screen) are live as of 2026-10-17. Slug discovery tip
for any new region: fetch all wiki entries with `?per_page=20&page=N&_fields=id,slug,title,link,acf`
and group by the `page-header-detail-page` section's `subheading`. Only count `[embed]`
shortcodes (and `youtube.com/embed/` iframes) as videos; plain YouTube links in the text are
related-video or reference links.

1. Possible new regions from the same wiki (owner order): Thoracic spine (13), Basic Assessment leftovers (Beighton, MRC, gait, posture, planes), Stats & Methodology (11), Clinimetrics (6).
2. Possible features the owner mentioned: an "其他" bucket for channel videos with no wiki
   page; timestamped segments within a video (needs transcripts — deferred 2026-10-17).
