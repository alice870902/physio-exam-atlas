# Physio Exam Atlas — project guide for Claude Code

Static site that turns Physiotutors' physical-examination videos into one course-style
single-page library (all regions, chapters 00–05, sidebar filters, accuracy table), with Traditional Chinese (台灣用語) notes and English
medical terms kept alongside. Live at https://alice870902.github.io/physio-exam-atlas/
(GitHub Pages, branch `main`, root). Owner: Wulin, rehabilitation medicine R1.

## Status

| Region | State | Notes |
|---|---|---|
| shoulder | **live** (92 videos, 10 categories) | redirect page; all 81 'Shoulder Assessment' wiki pages are in (18 backfilled 2026-10-17 as groupE/zh_4) |
| hip | **live** (61 videos, 8 categories) | redirect page; all 43 'Hip Assessment' wiki pages are in (19 backfilled 2026-10-17 as groupE/zh_4); source quirks (Pace page duplicates FAIR procedure, resisted-external-derotation page duplicates Puranen-Orava, compression/sacral-thrust and Kendall/Phelps share YouTube IDs) are flagged in record notes |
| knee | **live** (61 videos, 12 categories) | redirect page; 50 'Knee Assessment' wiki pages + screening/RTP/rehab pages; source quirks (duck-walk, decline-step-down, Renne pages duplicate other pages' procedures; varus page titled 'Valgus') flagged in record notes |
| lumbar | **live** (36 videos, 8 categories) | redirect page; 24 'Lumbar Spine Assessment' pages + referred pain, fracture red flags, Babinski, 4 SIJ pages not in hip, CPRs, direction-specific exercises; `myotomes-lower-limb` is deliberately in both knee and lumbar; SIJ provocation tests stay in hip |

## Repo layout

```
index.html                 built single-page site — DO NOT edit by hand, rebuild from src/
<region>/index.html        built redirect stubs → ../#region-<id> (or ../#test-<slug> if a hash is present)
src/site_template.html     single-page template; build replaces __DATA__, __N_TESTS__, __N_REGIONS__, __N_TOPICS__, __N_ACC__
src/build_site.py          python3 src/build_site.py   (no args) → writes index.html + 4 redirect pages
src/data/<region>/
  categories.json          [{id, zh, en, slugs:[...]}]  ← defines order & grouping
  group*.json              English source records fetched from physiotutors (any number of files)
  zh_*.json                Traditional Chinese notes (any number of files)
  slugs.json               (hip only) discovery list of candidate slugs
.nojekyll                  keep; GitHub Pages must not run Jekyll
```

Rebuild everything: `python3 src/build_site.py` (prints stats; fails loudly if a slug is missing
from zh/group or a category has no theme). Adding a region = add its data folder, append it to
`REGIONS` and map its category ids in `THEMES` inside build_site.py, rebuild, commit, push.
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
- 01 依主題: 7 cross-region themes (`THEMES` in build_site.py) → list → detail.
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
- Region names: zh/en pairs used so far — 肩部 Shoulder, 髖部 Hip, 膝部 Knee, 腰椎 Lumbar spine.
- Counts on the page are all computed by build_site.py; nothing is hand-written.
- Commit messages: short imperative English summary; the owner writes in Traditional Chinese
  in conversation.

## Suggested next steps

All four regions (shoulder, hip, knee, lumbar) are live as of 2026-10-17. Slug discovery tip
for any new region: fetch all wiki entries with `?per_page=20&page=N&_fields=id,slug,title,link,acf`
and group by the `page-header-detail-page` section's `subheading`. Only count `[embed]`
shortcodes (and `youtube.com/embed/` iframes) as videos; plain YouTube links in the text are
related-video or reference links.

1. Possible new regions from the same wiki: Ankle & Foot (31 pages), Elbow (28), Wrist & Hand (27),
   Cervical spine (17), Thoracic spine (13), Dizziness/vestibular (14), fracture-screening rules.
2. Possible features the owner mentioned: an "其他" bucket for channel videos with no wiki
   page; timestamped segments within a video (needs transcripts — deferred 2026-10-17).
