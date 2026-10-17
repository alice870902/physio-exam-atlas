"""Build the single-page Physio Exam Atlas site.

usage: python3 src/build_site.py            -> writes index.html + region redirect pages
Reads src/data/<region>/{categories,group*,zh_*}.json for every region in REGIONS,
embeds everything as JSON into src/site_template.html and writes index.html.
"""
import json, re, pathlib, sys

BASE = pathlib.Path(__file__).parent
ROOT = BASE.parent

REGIONS = [  # learning order on the page
    {"id": "shoulder", "zh": "肩部", "en": "Shoulder"},
    {"id": "hip", "zh": "髖部", "en": "Hip"},
    {"id": "knee", "zh": "膝部", "en": "Knee"},
    {"id": "lumbar", "zh": "腰椎", "en": "Lumbar spine"},
]

# Cross-region themes for chapter 01. Keys are "<region>.<category id>" or "*.<category id>".
THEMES = [
    {"id": "basics", "zh": "基礎評估與活動度", "en": "Basics & Range of Motion",
     "cats": ["*.assess", "lumbar.screen", "lumbar.rom", "lumbar.neuro"]},
    {"id": "structure", "zh": "結構特殊測試（韌帶／肌腱／盂唇／關節）", "en": "Structural Special Tests",
     "cats": ["*.saps", "*.rc", "shoulder.instab", "*.labrum", "*.biceps", "*.ac", "*.fai", "*.glute", "*.posthip",
              "*.effusion", "*.acl", "*.rotatory", "*.pcl", "*.plc", "*.collateral", "*.meniscus", "*.pf", "*.tendon"]},
    {"id": "motor", "zh": "肌力、肌肉長度與動作控制", "en": "Strength, Muscle Length & Motor Control",
     "cats": ["*.scap", "*.length", "lumbar.instab"]},
    {"id": "neuro", "zh": "神經、神經動力學與卡壓", "en": "Nerve, Neurodynamics & Entrapment",
     "cats": ["*.tos", "*.piri", "*.radic", "*.stenosis"]},
    {"id": "sij", "zh": "薦髂關節與骨盆", "en": "Sacroiliac Joint & Pelvis", "cats": ["*.sij"]},
    {"id": "rtp", "zh": "功能與回場測試", "en": "Functional & Return-to-Play Testing", "cats": ["*.rtp"]},
    {"id": "treat", "zh": "治療決策與運動治療", "en": "Treatment Decisions & Exercise",
     "cats": ["*.ex", "lumbar.tx"]},
]

SAMPLE_SLUG = "lachman-test"   # "快速試看" card on the hero

NOT_REPORTED = re.compile(r"^\s*(not reported|n/?a|none|-|—)?\s*$", re.I)
TITLE_SPLIT = re.compile(r"\s*([A-Za-z0-9][A-Za-z0-9 '’()|/\-]*)$")


def has_value(s):
    """True when an accuracy string carries a real value (used for the hero count)."""
    return bool(s) and not NOT_REPORTED.match(s) and not s.lower().startswith("not reported")


def first_number(s):
    """Numeric sort key for Sn/Sp/LR strings: first number in the string, None if none."""
    if not has_value(s):
        return None
    m = re.search(r"\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def theme_of(region, cat):
    for t in THEMES:
        if f"{region}.{cat}" in t["cats"] or f"*.{cat}" in t["cats"]:
            return t["id"]
    raise SystemExit(f"category {region}.{cat} has no theme in THEMES")


def load_region(r):
    d = BASE / "data" / r["id"]
    cats = json.load(open(d / "categories.json", encoding="utf-8"))
    src, zh = {}, {}
    for f in sorted(d.glob("group*.json")):
        for x in json.load(open(f, encoding="utf-8")):
            src[x["slug"]] = x
    for f in sorted(d.glob("zh_*.json")):
        for x in json.load(open(f, encoding="utf-8")):
            zh[x["slug"]] = x
    missing = [s for c in cats for s in c["slugs"] if s not in zh or s not in src]
    if missing:
        raise SystemExit(f"{r['id']} MISSING: {missing}")
    tests = []
    for c in cats:
        for s in c["slugs"]:
            a, z = src[s], zh[s]
            m = TITLE_SPLIT.search(z["title_zh"])
            title_en = m.group(1).strip().replace(" | ", " · ") if m else re.split(r"\s*\|\s*", a["title"])[0].strip()
            name_zh = z["title_zh"][: m.start()].strip() if m else z["title_zh"]
            acc = a.get("accuracy") or {}
            tests.append({
                "slug": s, "region": r["id"], "cat": c["id"], "theme": theme_of(r["id"], c["id"]),
                "title_en": title_en, "name_zh": name_zh, "title_zh": z["title_zh"], "title_src": a["title"],
                "link": a["link"], "youtube_ids": a["youtube_ids"],
                "acc": {k: acc.get(k, "not reported") for k in ("sensitivity", "specificity", "lr_plus", "lr_minus", "source")},
                "num": {k: first_number(acc.get(k, "")) for k in ("sensitivity", "specificity", "lr_plus", "lr_minus")},
                "has_acc": has_value(acc.get("sensitivity", "")),
                "zh": {k: z[k + "_zh"] for k in ("purpose", "structure", "procedure", "positive", "notes")},
                "en": {k: a.get(k, "") for k in ("purpose", "structure", "procedure", "positive", "notes")},
                "tags": z.get("tags", []),
            })
    return [{k: c[k] for k in ("id", "zh", "en")} | {"n": len(c["slugs"])} for c in cats], tests


def main():
    regions, tests = [], []
    for r in REGIONS:
        cats, t = load_region(r)
        regions.append(r | {"cats": cats, "n": len(t)})
        tests.extend(t)
    # a slug may legitimately appear in two regions (myotomes-lower-limb: knee + lumbar); keys stay unique per region
    keys = [f"{t['region']}/{t['slug']}" for t in tests]
    assert len(keys) == len(set(keys)), "duplicate region/slug"
    themes = []
    for th in THEMES:
        n = sum(1 for t in tests if t["theme"] == th["id"])
        themes.append({k: th[k] for k in ("id", "zh", "en")} | {"n": n})
    stats = {
        "tests": len(tests), "regions": len(regions),
        "topics": sum(len(r["cats"]) for r in regions),
        "with_accuracy": sum(1 for t in tests if t["has_acc"]),   # sensitivity present and not "not reported"
    }
    sample = next(t for t in tests if t["slug"] == SAMPLE_SLUG)
    data = {"regions": regions, "themes": themes, "tests": tests, "stats": stats, "sample": sample["region"] + "/" + sample["slug"]}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (BASE / "site_template.html").read_text(encoding="utf-8")
    for k, v in {"__DATA__": payload, "__N_TESTS__": str(stats["tests"]), "__N_REGIONS__": str(stats["regions"]),
                 "__N_TOPICS__": str(stats["topics"]), "__N_ACC__": str(stats["with_accuracy"])}.items():
        assert k in html, k
        html = html.replace(k, v)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("index.html", stats, round(len(html) / 1024), "KB")
    # tiny redirect pages so old /<region>/ and /<region>/#<slug> links keep working
    for r in REGIONS:
        page = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>{r['zh']} {r['en']} · Physio Exam Atlas</title>
<meta http-equiv="refresh" content="0; url=../#region-{r['id']}">
<script>var h=location.hash.replace(/^#/,'');location.replace('../#'+(h?'test-'+h:'region-{r['id']}'));</script>
</head><body><p>轉址中… <a href="../#region-{r['id']}">{r['zh']} {r['en']}</a></p></body></html>
"""
        (ROOT / r["id"]).mkdir(exist_ok=True)
        (ROOT / r["id"] / "index.html").write_text(page, encoding="utf-8")
    print("redirect pages:", ", ".join(r["id"] + "/" for r in REGIONS))


if __name__ == "__main__":
    main()
