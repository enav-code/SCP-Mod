#!/usr/bin/env python3
"""
Crawls the SCP wiki (text only, CC BY-SA 3.0) for SCP-001..SCP-2000 and writes tools/scp_wiki_data.json:
    { "173": {"cls": "Euclid", "height": 2.0, "tags": ["humanoid", ...], "colors": ["grey"]}, ... }
generate_resources.py then uses it for: real object class, entity size (scale), entity skin color, and
whether an SCP is a mob / block / item.

Run on a machine with internet access (the Claude sandbox has none):
    python3 tools/fetch_wiki_data.py            # ~2000 pages, ~35 min at the polite 1 s delay; resumable
    python3 tools/generate_resources.py

Only text is read. No images are downloaded (wiki images carry individual licenses).
Please keep the delay; this is a volunteer-run site.
"""
import json, re, sys, time, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "tools" / "cache"
OUT = ROOT / "tools" / "scp_wiki_data.json"
DELAY = 1.0
UA = "scp-minecraft-mod-datagen/1.0 (personal mod build; text only)"

COLOR_WORDS = ["black", "white", "grey", "gray", "red", "green", "blue", "yellow", "orange", "purple", "pink",
               "brown", "gold", "golden", "silver", "pale", "dark", "crimson", "violet", "tan", "beige"]
CLASSES = {"safe": "Safe", "euclid": "Euclid", "keter": "Keter", "thaumiel": "Thaumiel", "apollyon": "Apollyon"}
# non-standard classes mapped to the closest in-game tier
CLASS_FALLBACK = {"neutralized": "Safe", "explained": "Safe", "esoteric": "Euclid", "archon": "Keter", "ticonderoga": "Euclid",
                  "hiemal": "Euclid", "uncontained": "Keter", "pending": "Euclid", "decommissioned": "Safe",
                  "levant": "Euclid", "cernunnos": "Euclid", "tiamat": "Keter"}


class TextAndTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_content = 0
        self.depth = 0
        self.text = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and a.get("id") == "page-content":
            self.in_content = 1
            self.depth = 1
            return
        if self.in_content:
            if tag == "div":
                self.depth += 1
            if tag in ("br", "p", "li"):
                self.text.append("\n")
        if tag == "a" and "/system:page-tags/tag/" in (a.get("href") or ""):
            self.tags.append(a["href"].rsplit("/", 1)[-1])

    def handle_endtag(self, tag):
        if self.in_content and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.in_content = 0

    def handle_data(self, data):
        if self.in_content:
            self.text.append(data)


def fetch(n):
    f = CACHE / f"{n:04d}.html"
    if f.exists():
        return f.read_text(encoding="utf-8", errors="replace")
    url = f"https://scp-wiki.wikidot.com/scp-{n:03d}" if n < 1000 else f"https://scp-wiki.wikidot.com/scp-{n}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        html = ""
        if e.code not in (404, 410):
            print("HTTP", e.code, url, file=sys.stderr)
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")
    time.sleep(DELAY)
    return html


NUM = r"(\d+(?:\.\d+)?)"
HEIGHT_PATTERNS = [
    (re.compile(NUM + r"\s*(?:m|meters?|metres?)\s*(?:tall|high|in height)", re.I), 1.0),
    (re.compile(NUM + r"\s*(?:cm|centimet(?:er|re)s?)\s*(?:tall|high|in height)", re.I), 0.01),
    (re.compile(NUM + r"\s*(?:ft|feet|foot)\s*(?:tall|high|in height)", re.I), 0.3048),
    (re.compile(r"(\d+)\s*'\s*(\d+)?\s*(?:\"|in\.?)?\s*(?:tall|high)", re.I), None),  # 6'2" tall
    (re.compile(r"(?:height|stands|standing|measures)[^.\n]{0,40}?" + NUM + r"\s*(?:m|meters?|metres?)\b", re.I), 1.0),
    (re.compile(r"(?:height|stands|standing|measures)[^.\n]{0,40}?" + NUM + r"\s*(?:cm|centimet(?:er|re)s?)\b", re.I), 0.01),
    (re.compile(r"(?:height|stands|standing|measures)[^.\n]{0,40}?" + NUM + r"\s*(?:ft|feet|foot)\b", re.I), 0.3048),
    (re.compile(NUM + r"\s*(?:m|meters?|metres?)\s*(?:long|in length)", re.I), 0.7),   # length: use 70 % as body height
]


def find_height(text):
    best = None
    for pat, mult in HEIGHT_PATTERNS:
        m = pat.search(text)
        if not m:
            continue
        if mult is None:
            val = (int(m.group(1)) * 12 + int(m.group(2) or 0)) * 0.0254
        else:
            val = float(m.group(1)) * mult
        if 0.05 <= val <= 60:
            best = val
            break
    return round(best, 2) if best else None


def parse(n, html):
    if not html:
        return None
    p = TextAndTags()
    p.feed(html)
    text = re.sub(r"[ \t]+", " ", "".join(p.text))
    cls = None
    m = re.search(r"Object Class:?\s*\**\s*([A-Za-z]+)", text)
    if m:
        w = m.group(1).lower()
        cls = CLASSES.get(w) or CLASS_FALLBACK.get(w)
    # description section, falling back to whole text
    d = re.search(r"Description:?(.*?)(?:Addendum|Reference|$)", text, re.S | re.I)
    desc = d.group(1) if d else text
    colors = []
    for w in COLOR_WORDS:
        if re.search(r"\b" + w + r"\b", desc[:2500], re.I):
            colors.append(w)
    tags = [t for t in p.tags if t not in ("scp", "safe", "euclid", "keter", "thaumiel", "apollyon", "explained", "neutralized")]
    return {"cls": cls, "height": find_height(desc), "tags": tags[:12], "colors": colors[:3]}


def main():
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    for n in range(1, 2001):
        if str(n) in data:
            continue
        r = parse(n, fetch(n))
        data[str(n)] = r or {}
        if n % 25 == 0:
            OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
            print(f"{n}/2000", flush=True)
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    got_cls = sum(1 for v in data.values() if v.get("cls"))
    got_h = sum(1 for v in data.values() if v.get("height"))
    print(f"Done. class for {got_cls}, height for {got_h} of {len(data)} entries -> {OUT}")


if __name__ == "__main__":
    main()
