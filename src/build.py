"""Build one region page.  usage: build.py <region-dir> <zh-name> <en-name> <out.html>"""
import json, re, sys, pathlib
base = pathlib.Path(__file__).parent
d = base / "data" / sys.argv[1]
zh_name, en_name, out = sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
cats = json.load(open(d / "categories.json"))
src = {}
for f in sorted(d.glob("group*.json")):
    for x in json.load(open(f)):
        src[x["slug"]] = x
zh = {}
for f in sorted(d.glob("zh_*.json")):
    for x in json.load(open(f)):
        zh[x["slug"]] = x
missing = [s for c in cats for s in c["slugs"] if s not in zh or s not in src]
if missing:
    print("MISSING:", missing); sys.exit(1)
tests = []
for c in cats:
    for s in c["slugs"]:
        a, z = src[s], zh[s]
        m = re.search(r"\s*([A-Za-z0-9][A-Za-z0-9 '’()|/\-]*)$", z["title_zh"])
        title_en = m.group(1).strip().replace(" | ", " · ") if m else re.split(r"\s*\|\s*", a["title"])[0].strip()
        name_zh = z["title_zh"][: m.start()].strip() if m else z["title_zh"]
        tests.append({
            "slug": s, "title_en": title_en, "link": a["link"], "youtube_ids": a["youtube_ids"],
            "accuracy": a.get("accuracy") or {},
            "title_zh": z["title_zh"], "name_zh": name_zh, "purpose_zh": z["purpose_zh"], "structure_zh": z["structure_zh"],
            "procedure_zh": z["procedure_zh"], "positive_zh": z["positive_zh"], "notes_zh": z["notes_zh"],
            "tags": z.get("tags", []),
        })
data = {"region": {"zh": zh_name, "en": en_name, "slug": sys.argv[1]},
        "categories": [{k: c[k] for k in ("id", "zh", "en", "slugs")} for c in cats], "tests": tests}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = open(base / "template.html", encoding="utf-8").read()
html = (html.replace("__DATA__", payload)
            .replace("<title>Shoulder · Physio Exam Atlas</title>", f"<title>{en_name} · Physio Exam Atlas</title>")
            .replace("<h1>肩部 Shoulder</h1>", f"<h1>{zh_name} {en_name}</h1>")
            .replace("const LS = 'physio-atlas-done-shoulder';", f"const LS = 'physio-atlas-done-{sys.argv[1]}';"))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")
print(out, len(tests), "tests", round(out.stat().st_size / 1024), "KB")
