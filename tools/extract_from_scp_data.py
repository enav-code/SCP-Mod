#!/usr/bin/env python3
"""
Builds tools/scp_wiki_data.json (real object class, tags, size, colours) from a local clone of the public
dataset https://github.com/scp-data/scp-api (article text and tags from the SCP wiki, CC BY-SA 3.0).

    git clone --depth 1 https://github.com/scp-data/scp-api /path/to/scp-api
    python3 tools/extract_from_scp_data.py /path/to/scp-api
    python3 tools/generate_resources.py

Output per SCP number:
  cls       Safe/Euclid/Keter/Thaumiel/Apollyon from the wiki's own class tag (or the Object Class line)
  tags      wiki tags (used to decide mob / block / item)
  height    metres, only when the article states one
  height_src  "wiki" (stated height) or "wiki-length" (derived from a stated length)
  colors    colour words from the description
"""
import ast, glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLASS_TAGS = ["safe", "euclid", "keter", "thaumiel", "apollyon"]
CLASS_MAP = {"neutralized": "Safe", "explained": "Safe", "decommissioned": "Safe", "archon": "Keter",
             "uncontained": "Keter", "esoteric": "Euclid", "ticonderoga": "Euclid", "hiemal": "Euclid",
             "cernunnos": "Euclid", "tiamat": "Keter", "levant": "Euclid", "pending": "Euclid"}
COLORS = ["black", "white", "grey", "gray", "red", "green", "blue", "yellow", "orange", "purple", "pink", "brown",
          "gold", "golden", "silver", "pale", "crimson", "violet", "tan", "beige"]

NUM = r"(\d+(?:\.\d+)?)"
UNITS = {"m": 1.0, "meter": 1.0, "meters": 1.0, "metre": 1.0, "metres": 1.0, "cm": 0.01, "centimeter": 0.01,
         "centimeters": 0.01, "centimetre": 0.01, "centimetres": 0.01, "ft": 0.3048, "feet": 0.3048, "foot": 0.3048,
         "in": 0.0254, "inch": 0.0254, "inches": 0.0254}
U = r"(m|meters?|metres?|cm|centimet(?:er|re)s?|ft|feet|foot)"
HEIGHT = [
    re.compile(NUM + r"[\s-]*" + U + r"[\s-]*(?:tall|high)\b", re.I),
    re.compile(NUM + r"[\s-]*" + U + r"\s+in\s+height", re.I),
    re.compile(r"\b(?:height|stands|standing|measures|measuring)\b[^.\n]{0,50}?" + NUM + r"[\s-]*" + U + r"\b", re.I),
    re.compile(r"\b(\d)\s*(?:'|ft\.?|feet|foot)\s*(\d{1,2})?\s*(?:\"|in\.?|inches)?[\s-]*(?:tall|high)\b", re.I),
]
LENGTH = re.compile(NUM + r"[\s-]*" + U + r"[\s-]*(?:long|in\s+length)\b", re.I)


def unit(u):
    u = u.lower()
    return UNITS.get(u) or UNITS.get(u.rstrip("s")) or 1.0


def plain(html):
    t = re.sub(r"<(br|p|li|div)[^>]*>", "\n", html)
    t = re.sub(r"<[^>]+>", " ", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"').replace("&#8217;", "'")
          .replace("&lt;", "<").replace("&gt;", ">"))
    return re.sub(r"[ \t]+", " ", t)


def find_height(text):
    for pat in HEIGHT[:3]:
        for m in pat.finditer(text):
            v = float(m.group(1)) * unit(m.group(2))
            if 0.05 <= v <= 60:
                return round(v, 2), "wiki"
    m = HEIGHT[3].search(text)
    if m:
        v = (int(m.group(1)) * 12 + int(m.group(2) or 0)) * 0.0254
        if 0.05 <= v <= 60:
            return round(v, 2), "wiki"
    m = LENGTH.search(text)
    if m:
        v = float(m.group(1)) * unit(m.group(2)) * 0.5   # a long creature is about half as tall as it is long
        if 0.05 <= v <= 60:
            return round(v, 2), "wiki-length"
    return None, None


def main(repo):
    items = Path(repo) / "docs/data/scp/items"
    recs = {}
    for f in sorted(glob.glob(str(items / "content_*.json"))):
        is_series = "series" in f or "scp-001" in f
        for k, v in json.load(open(f, encoding="utf-8")).items():
            m = re.fullmatch(r"SCP-(\d{3,4})", k)
            if m and int(m.group(1)) <= 2000 and (int(m.group(1)) not in recs or is_series):
                recs[int(m.group(1))] = v
    out = {}
    for n, v in sorted(recs.items()):
        tags = v["tags"] if isinstance(v["tags"], list) else ast.literal_eval(v["tags"])
        text = plain(v["raw_content"])
        cls = next((c.capitalize() for c in CLASS_TAGS if c in tags), None)
        if not cls:
            cls = next((CLASS_MAP[t] for t in tags if t in CLASS_MAP), None)
        if not cls:
            m = re.search(r"Object Class:?\s*([A-Za-z]+)", text)
            if m:
                w = m.group(1).lower()
                cls = w.capitalize() if w in CLASS_TAGS else CLASS_MAP.get(w)
        d = re.search(r"Description:?(.*)", text, re.S | re.I)
        desc = (d.group(1) if d else text)
        desc_cut = re.split(r"Addendum|Reference|Appendix|Incident", desc)[0]
        height, src = find_height(desc_cut)
        colors = [c for c in COLORS if re.search(r"\b" + c + r"\b", desc_cut[:2500], re.I)][:3]
        out[str(n)] = {"cls": cls, "tags": [t for t in tags if not t.startswith("_")], "height": height,
                       "height_src": src, "colors": colors,
                       "desc": re.sub(r"\s+", " ", desc_cut)[:700].strip()}
    (ROOT / "tools/scp_wiki_data.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(out)} SCPs: class {sum(1 for x in out.values() if x['cls'])}, "
          f"height {sum(1 for x in out.values() if x['height'])} "
          f"(stated {sum(1 for x in out.values() if x['height_src']=='wiki')}), "
          f"colours {sum(1 for x in out.values() if x['colors'])}")


if __name__ == "__main__":
    main(sys.argv[1])
