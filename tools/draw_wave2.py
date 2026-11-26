"""Art wave 2: every remaining item- and block-form SCP gets a 16x16 sprite drawn from a hand-made
shape library (54 shapes), chosen by what the SCP actually is (title/tags/wiki text) and coloured from the
colours named in its wiki description. Wave-1 hand-drawn art is never overwritten. Original art; text data CC BY-SA 3.0."""
import json, random, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import icons

ROOT = Path(__file__).parent
OUT = ROOT / "custom_art"
W = json.load(open(ROOT / "scp_wiki_data.json"))
REG = json.load(open(ROOT.parent / "src/main/resources/scp_registry.json"))["entries"]

def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

COL = dict(white="ece8e0", black="26262a", grey="8a8e94", gray="8a8e94", silver="b8bcc4", red="c0302a", crimson="a01c2a",
  orange="e0802a", yellow="e0c030", gold="d4a030", golden="d4a030", green="3e9a4a", blue="3a6ac8", purple="8a4ab0",
  violet="8a4ab0", pink="e08aa8", brown="7a5230", tan="c0a880", bronze="a8742a", copper="b8683a", iron="6a6e76",
  steel="8a929c", wooden="8a5a2c", wood="8a5a2c", leather="6a4228", ivory="e8e0c0", teal="2a9a9a", cyan="40c0d0", glass="a8d8e8")
CLS = dict(Safe="4a9a5a", Euclid="c8902a", Keter="b02a2a", Thaumiel="3a6ad0")

def shade(c, f): return tuple(max(0, min(255, int(v*f))) for v in c)

# 16x16 shape templates. k outline, m main, d shadow, l light, a accent, '.' empty
S = {}
S['key'] = ["................","....kkkk........","...kllmmk.......","..klk..kmk......","..kmk..kdk......","...kmmmdk.......","....kkkdk.......",".......mk.......",".......mk.......",".......mkk......",".......mmk......",".......mk.......",".......mmmk.....",".......mk.k.....",".......kkk......","................"]
S['mask'] = ["................","...kkkkkkkkkk...","..kllmmmmmmmdk..","..kmmmmmmmmmdk..",".kmmkkkmmkkkmdk.",".kmmkkkmmkkkmdk.",".kmmmkmmmmkmmdk.",".kmmmmmmmmmmmdk.",".kmmmmaaaammmdk.",".kmmmkkkkkkmmdk.","..kmmmaaaammdk..","..kdmmmmmmmddk..","...kddmmmmddk...","....kkddddkk....","......kkkk......","................"]
S['book'] = ["................","..kkkkkkkkkkk...",".kmmmmmmmmmmdk..",".kmllllllllmdk..",".kmmmmmmmmmmdk..",".kmmaaaaaammdk..",".kmmmmmmmmmmdk..",".kmmaaaaaaammdk.".replace("mm","m",1)[:16],".kmmmmmmmmmmdk..",".kmmmmmmmmmmdk..",".kmmmmmmmmmmdk..",".kdddddddddddk..",".kwwwwwwwwwwwk..",".kwwwwwwwwwwwk..","..kkkkkkkkkkk...","................"]
S['eye'] = ["................","................","................","....kkkkkkkk....","..kkwwwwwwwwkk..",".kwwwwmmmmwwwwk.","kwwwwmmkkmmwwwwk","kwwwmmkkkkmmwwwk","kwwwwmmkkmmwwwwk",".kwwwwmmmmwwwwk.","..kkwwwwwwwwkk..","....kkkkkkkk....","................","................","................","................"]
S['tree'] = ["................",".....kkkkkk.....","...kkmmmmmmkk...","..kmmlmmmmmmmk..","..kmmmmmlmmmmk..",".kmmmmmmmmmmmdk.",".kmlmmmmmmmmmdk.",".kmmmmmmlmmmddk.","..kdmmmmmmmdddk.","...kkddmmdddkk..",".....kkbbkk.....",".......bb.......",".......bb.......",".......bb.......","......kbbk......",".....kkkkkk....."]
S['skull'] = ["................","....kkkkkkkk....","..kkwwwwwwwwkk..",".kwwwwwwwwwwwwk.",".kwwwwwwwwwwwdk.",".kwkkkwwwwkkkwk.",".kwkkkwwwwkkkwk.",".kwkkkwwwwkkkdk.","..kwwwwkkwwwwk..","...kwwwkkwwwk...","...kwwwwwwwdk...","....kwkwkwkk....","....kwkwkwk.....","....kkkkkkk.....","................","................"]
S['door'] = ["................","...kkkkkkkkkk...","..kmmmmmmmmmdk..","..kmlllmmlllmk..","..kmlllmmlllmk..","..kmlllmmlllmk..","..kmmmmmmmmmdk..","..kmlllmmlllmk..","..kmlllmmlllmk..","..kmlllmmlllmk..","..kmmmmmmaadmk..","..kmmmmmmaadmk..","..kmmmmmmmmmdk..","..kmmmmmmmmmdk..","..kkkkkkkkkkkk..","................"]
S['box'] = ["................","................","..kkkkkkkkkkkk..",".kllllllllllmmk.",".kmmmmmmmmmmmdk.",".kmmmmmmmmmmmdk.",".kkkkkkaakkkkkk.",".kmmmmmaammmmdk.",".kmmmmmmmmmmmdk.",".kmmmmmmmmmmmdk.",".kmmmmmmmmmmmdk.",".kdddddddddddd..".replace("d.","dk")[:16],"..kkkkkkkkkkkk..","................","................","................"]
S['clock'] = ["................","....kkkkkkkk....","..kkllllllllkk..",".kllmmmmmmmmllk.",".klmmmmkmmmmmlk.",".kmmmmmkmmmmmdk.",".kmmmmmkmmmmmdk.",".kmmmmmkkkkmmdk.",".kmmmmmmmmmmmdk.",".kmmmmmmmmmmmdk.",".kdmmmmmmmmmddk.","..kkddddddddkk..","....kkkkkkkk....","................","................","................"]
S['mirror'] = ["................","....kkkkkkkk....","..kkaaaaaaaakk..",".kaaccccccccaak.",".kacccllcccccak.",".kaccllccccccak.",".kaclcccccccdak.",".kacccccccccdak.",".kaccccccccddak.",".kaaccccccddaak.","..kkaaaaaaaakk..","....kkkaakkk....",".....kaaaak.....",".....kkkkkk.....","................","................"]
S['doll'] = ["................","....kkkkkkkk....","...kmmmmmmmmk...","...kmkkmmkkmk...","...kmmmmmmmmk...","...kmmakkammk...","....kmmmmmmk....","..kkmmmmmmmmkk..",".kmmkaaaaaakmmk.",".kmmkmmmmmmkmmk.","..kkkmmmmmmkkk..","....kmmkkmmk....","....kmmkkmmk....","....kddkkddk....","....kkk..kkk....","................"]
S['bottle'] = ["................","......kkkk......",".....kaaaak.....",".....kkkkkk.....","......kmmk......","......kmmk......",".....kmmmmk.....","....kmmmmmmk....","...kmlmmmmmdk...","...kmlmmmmmdk...","...kmmmmmmmdk...","...kmmmmmmmdk...","...kmmmmmmmdk...","....kddddddk....",".....kkkkkk.....","................"]
S['bug'] = ["................","..k..........k..","...k...kk...k...","....k.kmmk.k....",".....kmmmmk.....","..kkkkmllmkkkk..","....kmmmmmmk....","..kkkmmmmmmkkk..","....kmmmmmmk....","..kkkmmmmmmkkk..","....kdmmmmdk....",".....kddddk.....","....k.kkkk.k....","...k........k...","................","................"]
S['fish'] = ["................","................","................","......kkkk..kk..","....kkmmmmkkmk..","..kkmmmmmmmmmmk.",".kmmkkmmmmmmmmk.",".kmmkkmmmmmmmmk.",".kmmmmmmmmmmmmk.","..kkdddddddddkk.","....kkddddkkdk..","......kkkk..kk..","................","................","................","................"]
S['bird'] = ["................","................","......kkkk......",".....kmmmmk.....","....kmkkmmkaa...","....kmmmmmkaak..","....kmmmmmmk.k..","..kkkmmmmmmmk...",".kmmmmmmmmmdk...",".kmmmmmmmmdk....","..kkddddddkk....","....kkkaakk.....",".....k..a.k.....","................","................","................"]
S['cat'] = ["................","..k........k....","..kk......kk....","..kmk....kmk....","..kmmkkkkmmk....","..kmmmmmmmmk....","..kmwkmmkwmk....","..kmmmmmmmmk....","...kmmaammk.....","....kmmmmk......","...kmmmmmmkkk...","..kmmmmmmmmmmk..","..kmmmmmmmmmmmk.","..kdmk..kmkkmk..","..kkk...kkk.kk..","................"]
S['dog'] = ["................","................","..kk............","..kmkkkkkk......","..kmmmmmmmkk....","..kmwkmmmmmmk...","..kmmmmmmmmmmk..","..kkaakmmmmmmmk.","....kkkmmmmmmmk.","......kmmmmmmmk.","......kmkkkkmkk.","......kmk..kmk..","......kmk..kmk..","......kkk..kkk..","................","................"]
S['hand'] = ["................","......k.........","....k.mk.k......","...kmkmkkmk.....","...kmkmkmmk.kk..","...kmkmkmmkkmk..","...kmmmmmmmkmk..","..kkmmmmmmmmmk..",".kmkmmmmmmmmmk..",".kmmmmmmmmmmdk..","..kmmmmmmmmmk...","...kmmmmmmmdk...","....kmmmmmdk....","....kddddddk....",".....kkkkkk.....","................"]
S['heart'] = ["................","................","..kkkk....kkkk..",".kmllmk..kmmmmk.","kmlllmmkkmmmmmdk","kmllmmmmmmmmmmdk","kmmmmmmmmmmmmddk",".kmmmmmmmmmmddk.","..kmmmmmmmmddk..","...kmmmmmmddk...","....kmmmmddk....",".....kmmddk.....","......kmdk......",".......kk.......","................","................"]
S['house'] = ["................","......kk........",".....kmmk.......","....kmmmmk......","...kmmmmmmk.....","..kmmmmmmmmk....",".kmmmmmmmmmmk...","kkkkkkkkkkkkkk..",".kwwwwwwwwwwk...",".kwwkkwwkkwwk...",".kwwkkwwkkwwk...",".kwwwwwwaawwk...",".kwwwwwwaawwk...",".kkkkkkkkkkkk...","................","................"]
S['tower'] = ["................","......kk........",".....kmmk.......","....kmmmmk......","....kmmmmk......","....kwwwwk......","....kwkkwk......","....kwwwwk......","....kwwwwk......","...kwwwwwwk.....","...kwwkkwwk.....","...kwwwwwwk.....","..kwwwwwwwwk....","..kkkkkkkkkk....","................","................"]
S['bone'] = ["................","................","..kk......kk....",".kwwk....kwwk...",".kwwwk..kwwwk...","..kwwwkkwwwk....","...kwwwwwwk.....","....kwwwwk......",".....kwwwwk.....","....kwwwwwwk....","...kwwwkkwwwk...","..kwwwk..kwwwk..",".kwwk......kwwk.",".kk..........kk.","................","................"]
S['flame'] = ["................","........k.......",".......kak......","......kaak......",".....kaaak......","....kkaaamk.....","...kaaamamk.....","...kaamlmak.....","..kaamllmmak....","..kamlllllmak...","..kamllllllmk...","..kamllllllmk...","...kammlllmak...","....kkammakk....",".....kkkkkk.....","................"]
S['drop'] = ["................","........k.......",".......kmk......","......kmmk......",".....kmlmmk.....","....kmllmmmk....","...kmllmmmmmk...","...kmlmmmmmdk...","..kmmmmmmmmmdk..","..kmmmmmmmmddk..","..kmmmmmmmmddk..","...kmmmmmmddk...","....kdmmmddk....",".....kkddkk.....","......kkkk......","................"]
S['star'] = ["................",".......kk.......","......kmmk......","......kmmk......",".....kmllmk.....","kkkkkkmllmkkkkkk","kmmmmmmllmmmmmdk",".kmmmmmmmmmmmdk.","..kkmmmmmmmdkk..","....kmmmmmdk....","...kmmmmmmmdk...","...kmmmkkmmmk...","..kmmkk..kkmmk..","..kkk......kkk..","................","................"]
S['gear'] = ["................","......kkkk......","....k.kmmk.k....","...kmkkmmkkmk...","...kmmmllmmmk...",".kkkmmkkkkmmkkk.",".kmmmkk..kkmmmk.",".kmllk....kmlmk.",".kmmmkk..kkmmmk.",".kkkmmkkkkmmkkk.","...kmmmmmmmmdk..","...kmkkmmkkmk...","....k.kmmk.k....","......kkkk......","................","................"]
S['phone'] = ["................","..kkkkkkkkkkkk..",".kmmmmmmmmmmmk..",".kmkkkkkkkkkmk..",".kmkcccccccdmk..",".kmkcccccccdmk..",".kmkkkkkkkkkmk..",".kmmmmmmmmmmmk..",".kmkkmkkmkkmmk..",".kmkkmkkmkkmmk..",".kmmmmmmmmmmmk..",".kmkkmkkmkkmmk..",".kmkkmkkmkkmmk..",".kmmmmmmmmmmmk..","..kkkkkkkkkkkk..","................"]
S['tv'] = ["................","..k........k....","...k......k.....","....k....k......",".kkkkkkkkkkkkkk.",".kmmmmmmmmmmmdk.",".kmkcccccccckmk.".replace("mk.","mdk"),".kmkcllcccccdmk.",".kmkccccccccdmk.",".kmkcccccccddmk.",".kmkkkkkkkkkkmk.",".kmmmmmmmmaammk.",".kkkkkkkkkkkkkk.","....kk....kk....","................","................"]
S['ring'] = ["................","................","......kkkk......","....kkllllkk....","...kllmmmmllk...","..klmkkkkkkmlk..","..kmkk....kkmk..","..kmk......kmk..","..kmk......kmk..","..kmkk....kkdk..","..kdmkkkkkkmdk..","...kddmmmmddk...","....kkddddkk....","......kkkk......","................","................"]
S['sword'] = ["................","..............kk","............kkwk","...........kwwk.","..........kwwk..",".........kwwk...","........kwwk....",".k.....kwwk.....",".kk...kwwk......","..kkkkwwk.......","...kaakk........","....kaak........","...kmkkak.......","..kmk..kk.......",".kkk............","................"]
S['crown'] = ["................","................","................","..k....k....k...","..kk..kmk..kk...","..kmk.kmk.kmk...","..kmmkkmmkkmmk..","..kmmmmmmmmmmk..","..kmlmmmmmmmdk..","..kmaaamaaamdk..","..kmmmmmmmmmdk..","..kddddddddddk..","..kkkkkkkkkkkk..","................","................","................"]
S['flower'] = ["................","................",".....kkkk.......","....kmmmmk......","..kkmmllmmkk....",".kmmmmaammmmk...",".kmmmmaammmmk...","..kkmmmmmmkk....","....kmmmmk......",".....kkgk.......","......gg........","....kggg.k......","...kgggk.gk.....","....kk.kggk.....","................","................"]
S['snake'] = ["................","................","....kkkk........","...kmmmmk.......","...kmkmmmkkkk...","...kaamkmmmmmk..","....kkkk.kllmk..","........kmmmk...","....kkkkmmmk....","...kmmmmmmk.....","...kmlmmkk......","....kmmmmkkkk...",".....kkkkmmmmk..","..........kkkk..","................","................"]
S['spider'] = ["................","................","..k....kk....k..","...k..kmmk..k...","....kkmmmmkk....","..kkkmmllmmkkk..","....kmmmmmmk....","..kkmmmmmmmmkk..","..k.kmmmmmmk.k..","..k..kddddk..k..","..k...kkkk...k..","................","................","................","................","................"]
S['ghost'] = ["................","....kkkkkkk.....","...kwwwwwwwk....","..kwwwwwwwwwk...","..kwwkkwwkkwk...","..kwwkkwwkkwk...","..kwwwwkkwwwk...","..kwwwwkkwwwk...","..kwwwwwwwwwk...","..kwwwwwwwwwk...","..kwwwwwwwwwk...","..kwkwwkwwkwk...","..kk.kwk.kwkk...","................","................","................"]
S['planet'] = ["................","................","....kkkkkk......","..kkllmmmmkk....",".kllmmmmmmmmk...","kkkkkkkkkkkkkkk.",".kllmmmmmmmmdk..",".kmmmmmmmmmddk..",".kmmmmmmmmddk...","..kkddmmddkk....","....kkkkkk......","................","................","................","................","................"]
S['tooth'] = ["................","...kkkk..kkkk...","..kwwwwkkwwwwk..","..kwwwwwwwwwwk..","..kwwwwwwwwwdk..","..kwwwwwwwwwdk..","...kwwwwwwwdk...","...kwwkwwkwdk...","...kwwkwwkwdk...","...kwk.kk.kwk...","...kwk.kk.kwk...","....kk....kk....","................","................","................","................"]
S['camera'] = ["................","................","....kkkkk.......","..kkkmmmkkkkkk..",".kmmmmmmmmmmmmk.",".kmkkkkkmmmmaak.",".kmkcccckmmmmmk.",".kmkclccdkmmmmk.",".kmkccccdkmmmmk.",".kmkkkkkkmmmmmk.",".kmmmmmmmmmmmdk.",".kddddddddddddk.","..kkkkkkkkkkkk..","................","................","................"]
S['note'] = ["................","................","......kkkkkk....","......kmmmmmk...","......kmkkkmk...","......kmk.kmk...","......kmk.kmk...","......kmk.kmk...","......kmk.kmk...","..kkk.kmk.kmk...",".kmmmkkmk.kmk...",".kmmmmkmk.kmk...","..kmmmkk..kmmk..","...kkk...kmmmk..","..........kkk...","................"]
S['lock'] = ["................","................","....kkkkkkk.....","...kaaaaaaak....","..kak.....kak...","..kak.....kak...","..kak.....kak...",".kkkkkkkkkkkkk..",".kmmmmmmmmmmmdk.",".kmmmmkkkmmmmdk.",".kmmmmkkkmmmmdk.",".kmmmmmkmmmmmdk.",".kmmmmmkmmmmmdk.",".kddddddddddddk.","..kkkkkkkkkkkk..","................"]
S['pill'] = ["................","................","................","........kkk.....",".......kmmmk....","......kmlmmmk...",".....kmlmmmdk...","....kmmmmmddk...","...kwwmmmddk....","..kwwwwmddk.....","..kwwwwddk......","..kwwwwdk.......","...kkkkk........","................","................","................"]
S['cloud'] = ["................","................","......kkkk......","....kkllllkk....","..kkllmmmmllkk..",".kllmmmmmmmmllk.",".klmmmmmmmmmmdk.",".kmmmmmmmmmmmdk.",".kdmmmmmmmmmddk.","..kkddddddddkk..","....kkkkkkkk....","................","................","................","................","................"]
S['mushroom'] = ["................","................","....kkkkkkkk....","..kkmmmmmmmmkk..",".kmmwwmmmmwwmmk.",".kmwwwmmmmmwwmk.",".kmmmmmmwwmmmdk.",".kddddddddddddk.","..kkkkwwwwkkkk..","......kwwk......","......kwwk......","......kwdk......",".....kwwwdk.....",".....kkkkkk.....","................","................"]
S['human'] = ["................","....kkkkkk......","...kmmmmmmk.....","...kmkmmkmk.....","...kmmmmmmk.....","....kkmmkk......","..kkaaaaaakk....",".kmkaaaaaakmk...",".kmkaaaaaakmk...",".kmkaaaaaakmk...","..kkkddddkkk....","....kmkkmk......","....kmkkmk......","....kdkkdk......","...kkkk.kkkk....","................"]
S['water'] = ["................","................","................","..kkkk..........","kkllmmkkkkk.....","kllmmmmmmmmkkk..","kmmmmmmmmmmmmmk.","kddmmmmmmmmmmdk.",".kkddmmmmmmmdkk.","...kkkddddddkk..",".....kkkkkkk....","................","................","................","................","................"]
S['vehicle'] = ["................","................","................","....kkkkkkk.....","...kmmmmmmmk....","..kmmcccmccmk...",".kmmmcccmccmmk..",".kmmmmmmmmmmmmkk","kmmmmmmmmmmmmmmk","kmmmmmmmmmmmmmdk","kkkkkkkkkkkkkkkk","..kkkk....kkkk..",".kkwwkk..kkwwkk.",".kkwkkk..kkwkkk.","..kkkk....kkkk..","................"]
S['computer'] = ["................","..kkkkkkkkkkkk..",".kmmmmmmmmmmmdk.",".kmkkkkkkkkkmdk.",".kmkccccccckmdk.",".kmkcttcctckmdk.",".kmkccccccckmdk.",".kmkcttttcckmdk.",".kmkkkkkkkkkmdk.",".kmmmmmmmmmmmdk.","..kkkkmmkkkkk...","....kmmmmmmk....",".kkkkkkkkkkkkkk.",".kmkmkmkmkmkmmk.",".kkkkkkkkkkkkkk.","................"]
S['egg'] = ["................","................","......kkkk......","....kkllmmkk....","...kllmmmmmmk...","..kllmmmmmmmmk..","..klmmmmmmmmdk..","..kmmmmmmmmmdk..","..kmmmmmmmmddk..","..kmmmmmmmmddk..","...kmmmmmmddk...","....kkddddkk....","......kkkk......","................","................","................"]
S['cube'] = ["................","......kkkk......","....kkllllkk....","..kkllllllllkk..",".kllllllllllllk.",".kkkllllllllkkk.",".kmmkkllllkkddk.",".kmmmmkkkkdddmk.",".kmmmmmkkmmdddk.",".kmmmmmkkmmmddk.",".kmmmmmkkmmmddk.","..kkmmmkkmmddk..","....kkmkkmdkk...","......kkkk......","................","................"]
S['shell'] = ["................","................","................","......kkkk......","....kkmmllkk....","...kmmmmmllmk...","..kmmkmmmmmmmk..","..kmkmmmmkmmdk..","..kmmmmkmmmmdk..","...kmmmmmmmdk...","....kkdddddk....","......kkkkk.....","................","................","................","................"]
S['feather'] = ["................","..............kk","............kkmk","..........kkmmmk","........kkmmmmk.","......kkmmmmmmk.","....kkmmmmmmmk..","...kmmmmmmmmk...","..kmmmmmmmkk....",".kmmmmmmkk......",".kmmmkkk........","kkk.kk..........","kk..............","................","................","................"]
S['wing'] = ["................","................","................","k...............","kk.........kkkk.","kmk.....kkkmmmk.","kmmkkkkkmmmmmk..","kmmmmmmmmmmmk...",".kmmmmmmmmmk....",".kmmmmmmmmk.....","..kmmmmmkk......","...kmmkk........","....kk..........","................","................","................"]
S['coin'] = ["................","................","....kkkkkkkk....","..kkllllllmmkk..",".kllmmmmmmmmmdk.",".klmmkkmmkkmmdk.",".kmmmkmmmmkmmdk.",".kmmmmkkkkmmmdk.",".kmmmmmmmmmmmdk.",".kmmmmmmmmmmddk.","..kkddmmmmddkk..","....kkkkkkkk....","................","................","................","................"]

def palette(n, e):
    w = W.get(str(n), {})
    cols = [COL[c] for c in w.get("colors", []) if c in COL]
    r = random.Random(n * 7919)
    base = hexc(cols[0]) if cols else shade(hexc(CLS.get(e["cls"], "888888")), r.uniform(0.7, 1.1))
    if not cols:  # nudge hue per SCP so un-coloured ones differ
        base = tuple(max(0, min(255, v + r.randint(-18, 18))) for v in base)
    acc = hexc(cols[1]) if len(cols) > 1 else hexc(CLS.get(e["cls"], "888888"))
    return dict(k=shade(base, 0.22), m=base, d=shade(base, 0.68), l=shade(base, 1.3), a=acc,
                w=(236, 232, 222), c=(30, 60, 70), t=(90, 240, 110), b=(106, 74, 40), g=(60, 140, 60))

def render(shape, pal, flip, bg=None):
    im = Image.new("RGBA", (16, 16), bg + (255,) if bg else (0, 0, 0, 0))
    tpl = S[shape]
    for y, row in enumerate(tpl[:16]):
        row = row.ljust(16, '.')[:16]
        for x, ch in enumerate(row):
            if ch in pal:
                im.putpixel((15 - x if flip else x, y), pal[ch] + (255,))
    return im

def block_tile(shape, pal, e, n):
    r = random.Random(n)
    bgc = shade(pal["m"], 0.42)
    im = Image.new("RGBA", (16, 16), bgc + (255,))
    for _ in range(40):
        im.putpixel((r.randrange(16), r.randrange(16)), shade(bgc, r.uniform(0.8, 1.25)) + (255,))
    cls = hexc(CLS.get(e["cls"], "888888"))
    for i in range(16):
        for xy in ((i, 0), (i, 15), (0, i), (15, i)):
            im.putpixel(xy, cls + (255,))
    spr = render(shape, pal, False)
    small = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); small.alpha_composite(spr.resize((12, 12), Image.NEAREST), (2, 2))
    im.alpha_composite(small)
    return im

done = {int(p.stem.split("_")[1]) for p in OUT.glob("scp_????.png")}
made = {"item": 0, "block": 0}
usage = {}
for e in REG:
    n = e["n"]; form = e["form"]
    if form not in ("item", "block") or n in done: continue
    w = W.get(str(n), {})
    name = e.get("icon")
    if name not in S:
        name = random.Random(n).choice(list(S))   # abstract fallback: a varied shape
    pal = palette(n, e)
    flip = (n % 2 == 1) and form == "item"
    im = render(name, pal, flip) if form == "item" else block_tile(name, pal, e, n)
    im.save(OUT / f"scp_{n:04d}.png")
    made[form] += 1; usage[name] = usage.get(name, 0) + 1
print("drew", made, "shapes used:", len(usage), sorted(usage.items(), key=lambda kv: -kv[1])[:8])
