"""產生 src/data/<region>/anatomy.json：Atlas 測試 slug → 解剖資料庫構造編號 的對照表。

來源（都在私人 repo anatomy-atlas，只讀這兩個不含版權內容的檔案）：
  /Users/yitzu_wu/dev/anatomy-atlas/data/coverage_<region>.tsv
      三欄：slug ／ 構造編號（逗號分隔）／ Atlas 目標構造欄位（備查用，不輸出）
  /Users/yitzu_wu/dev/anatomy-atlas/data/structures.json
      {"region": ..., "structures": [{id, type, zh, en, ...}]}  → 只取 id／zh／en
建立：2026-10-19（肩部試點：100 個 slug、268 組配對）

用法：
  python3 src/make_anatomy_json.py shoulder
  python3 src/make_anatomy_json.py <region> [--coverage 路徑.tsv] [--structures 路徑.json]
      加新部位時，等 anatomy-atlas 那邊的 coverage_<region>.tsv 做好，跑一次即可；
      之後 `python3 src/build_site.py` 會自己讀 anatomy.json 並檢查 slug／構造編號都對得上。

輸出格式（src/data/<region>/anatomy.json）：
  {"base_url": "https://anatomy-atlas.alice870902.workers.dev/#s-",
   "structures": {"supraspinatus": {"zh": "棘上肌", "en": "Supraspinatus"}, ...},   # 只收這個部位用到的
   "tests": {"neer-test": ["coracoacromial-ligament", "infraspinatus", ...], ...}}

⛔ anatomy-atlas 的 data/excerpts、data/entries、data/figures、dist 含教科書逐字文字與裁圖，
   一個字、一張圖都不可以進這個公開 repo；本腳本只輸出「編號＋中英文名」。
"""
import argparse, csv, json, pathlib, sys

BASE = pathlib.Path(__file__).parent
ANATOMY_REPO = pathlib.Path("/Users/yitzu_wu/dev/anatomy-atlas/data")
BASE_URL = "https://anatomy-atlas.alice870902.workers.dev/#s-"


def main():
    ap = argparse.ArgumentParser(description="產生 Atlas 測試 → 解剖資料庫構造 的對照表 anatomy.json")
    ap.add_argument("region", help="Atlas 部位 id，例如 shoulder（對應 src/data/<region>/）")
    ap.add_argument("--coverage", type=pathlib.Path, help="覆蓋率對照表 TSV（預設 anatomy-atlas/data/coverage_<region>.tsv）")
    ap.add_argument("--structures", type=pathlib.Path, default=ANATOMY_REPO / "structures.json",
                    help="構造總表 JSON（預設 anatomy-atlas/data/structures.json）")
    args = ap.parse_args()

    region_dir = BASE / "data" / args.region
    if not region_dir.is_dir():
        sys.exit(f"找不到部位資料夾：{region_dir}")
    coverage = args.coverage or ANATOMY_REPO / f"coverage_{args.region}.tsv"
    for p in (coverage, args.structures):
        if not p.exists():
            sys.exit(f"找不到來源檔：{p}")

    # 構造總表：接受 {"structures": [...]} 或直接是陣列；只取 id／zh／en
    raw = json.load(open(args.structures, encoding="utf-8"))
    items = raw["structures"] if isinstance(raw, dict) else raw
    all_structs = {}
    for x in items:
        if x["id"] in all_structs:
            sys.exit(f"structures.json 裡 id 重複：{x['id']}")
        all_structs[x["id"]] = {"zh": x["zh"], "en": x["en"]}

    # 這個部位的 Atlas slug 清單（categories.json 是分類的事實來源）
    cats = json.load(open(region_dir / "categories.json", encoding="utf-8"))
    cat_slugs = {s for c in cats for s in c["slugs"]}

    tests, used, problems = {}, set(), []
    with open(coverage, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for col in ("slug", "構造編號"):
        if rows and col not in rows[0]:
            sys.exit(f"{coverage} 缺少欄位「{col}」，現有欄位：{list(rows[0].keys())}")
    for r in rows:
        slug = r["slug"].strip()
        ids = [s.strip() for s in r["構造編號"].split(",") if s.strip()]
        if slug in tests:
            problems.append(f"slug 重複：{slug}")
        if slug not in cat_slugs:
            problems.append(f"slug 不在 {args.region}/categories.json 裡：{slug}")
        if not ids:
            problems.append(f"{slug} 沒有任何構造編號")
        for sid in ids:
            if sid not in all_structs:
                problems.append(f"{slug} 的構造編號不在 structures.json 裡：{sid}")
        tests[slug] = ids
        used |= set(ids)
    if problems:
        sys.exit("anatomy.json 沒有產生，來源有問題：\n  " + "\n  ".join(problems))

    out = {
        "base_url": BASE_URL,
        "structures": {sid: all_structs[sid] for sid in sorted(used)},
        "tests": tests,
    }
    dst = region_dir / "anatomy.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_pairs = sum(len(v) for v in tests.values())
    print(f"寫入 {dst.relative_to(BASE.parent)}：{len(tests)} 個 slug、{len(out['structures'])} 個構造、{n_pairs} 組 (slug, 構造) 配對")
    missing = sorted(cat_slugs - set(tests))
    if missing:
        print(f"提醒：{args.region} 有 {len(missing)} 個 slug 沒有對照（這些卡片不會顯示解剖列）：{missing}")
    unused = sorted(set(all_structs) - used)
    if unused:
        print(f"提醒：structures.json 有 {len(unused)} 個構造沒被任何測試引用（未寫入）：{unused}")


if __name__ == "__main__":
    main()
