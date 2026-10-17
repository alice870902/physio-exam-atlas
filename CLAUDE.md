# Physio Exam Atlas — project guide for Claude Code

Static site that turns Physiotutors' physical-examination videos into a course-style
study page per body region, with Traditional Chinese (台灣用語) notes and English
medical terms kept alongside. Live at https://alice870902.github.io/physio-exam-atlas/
(GitHub Pages, branch `main`, root). Owner: Wulin, rehabilitation medicine R1.

## Status

| Region | State | Notes |
|---|---|---|
| shoulder | **live** (74 videos, 10 categories) | `shoulder/index.html` |
| hip | **live** (42 videos, 7 categories) | `hip/index.html`; source quirks (Pace page duplicates FAIR procedure, compression/sacral-thrust share one YouTube ID) are flagged in `groupC/D.json` notes |
| knee | **live** (61 videos, 12 categories) | `knee/index.html`; 50 'Knee Assessment' wiki pages + screening/RTP/rehab pages; source quirks (duck-walk, decline-step-down, Renne pages duplicate other pages' procedures; varus page titled 'Valgus') flagged in record notes |
| lumbar | planned | placeholder card on home page |

## Repo layout

```
index.html                 home page (region cards; hand-written)
shoulder/index.html        built output — DO NOT edit by hand, rebuild from src/
src/template.html          single-page app template; __DATA__ is replaced with JSON
src/build.py               python3 src/build.py <region> <中文名> <English name> <out.html>
src/data/<region>/
  categories.json          [{id, zh, en, slugs:[...]}]  ← defines order & grouping
  group*.json              English source records fetched from physiotutors (any number of files)
  zh_*.json                Traditional Chinese notes (any number of files)
  slugs.json               (hip only) discovery list of candidate slugs
.nojekyll                  keep; GitHub Pages must not run Jekyll
```

Rebuild shoulder: `python3 src/build.py shoulder 肩部 Shoulder shoulder/index.html`
Build hip once data exists: `python3 src/build.py hip 髖部 Hip hip/index.html`
Then add/replace the region card in `index.html` (remove its 規劃中 placeholder) and commit.

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
   - `title_zh` = `中文名稱 + 空格 + 英文原名` (e.g. `空罐測試 Empty Can Test`). build.py
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

## Page behaviour (template.html)

- Left index: category (`<details>`) → test; search box filters on zh/en title, structure,
  tags, purpose. Prev/next buttons; URL hash = slug; mobile drawer via ☰.
- Right: YouTube `youtube-nocookie.com/embed/<id>` iframe (multiple IDs → 影片 1/2 pills),
  bilingual heading, tags, 已看完 checkbox, then six sections: 目的 / 檢查結構 / 操作步驟 /
  陽性判讀 / 診斷準確度 (Sn, Sp, LR±, source — rows hidden when "not reported") / 臨床重點,
  plus a link back to the physiotutors.com page.
- Progress stored in `localStorage` key `physio-atlas-done-<region>` (per browser).
- Light/dark via `prefers-color-scheme`; Google Fonts Noto Sans TC + Fraunces + IBM Plex Mono.
- No build step beyond build.py; no framework; one self-contained HTML per region.

## Conventions and gotchas

- Videos are only embedded, never downloaded; keep the copyright footer line.
- The build replaces three literal strings in the template (title, `<h1>`, localStorage key)
  — keep those exact strings in template.html if you edit it.
- Region names: zh/en pairs used so far — 肩部 Shoulder, 髖部 Hip, 膝部 Knee, 腰椎 Lumbar spine.
- Home-page card count line is hand-written (`74 支影片 · 10 個主題`); update when rebuilding.
- Commit messages: short imperative English summary; the owner writes in Traditional Chinese
  in conversation.

## Suggested next steps

1. Lumbar, same pipeline. (Hip and knee done 2026-10-17. Slug discovery tip: fetch all wiki
   entries with `?per_page=20&page=N&_fields=id,slug,title,link,acf` and group by the
   `page-header-detail-page` section's `subheading`, e.g. "Lumbar Spine Assessment" (24 pages)
   plus "Spine Assessment"/"Screening"/"Neurological Screening" candidates.)
2. Possible features the owner mentioned: an "其他" bucket for channel videos with no wiki
   page; timestamped segments within a video (needs transcripts); an "all regions" search.
