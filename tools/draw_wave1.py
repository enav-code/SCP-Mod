"""Hand-drawn art, wave 1. Original pixel art based on the public SCP wiki descriptions (CC BY-SA 3.0,
scp-wiki.wikidot.com). Writes tools/custom_art/scp_NNNN.png (16x16 tile) and scp_NNNN_skin.png (64x64 mob skin)."""
import random
from pathlib import Path
from PIL import Image

OUT = Path(__file__).parent / "custom_art"
OUT.mkdir(exist_ok=True)

def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)

def tile(rows, legend, bg=None):
    im = Image.new("RGBA", (16, 16), hexc(bg) if bg else (0, 0, 0, 0))
    for y, r in enumerate(rows[:16]):
        for x, ch in enumerate(r.ljust(16, r[-1] if bg and r else '.')[:16]):
            if ch in legend: im.putpixel((x, y), hexc(legend[ch]))
    return im

# ---------------------------------------------------------------- tiles
T = {}
T[173] = (["................",
".....dccccd.....",
"....dccccccd....",
"....cckccckc....",
"....cccccccc....",
"....ccrccrcc....",
".....ccrrcc.....",
"..dcccccccccd...",
".dcccnccccrccd..",
".dccccnccccccd..",
".cc.cccnccc.cc..",
".cc.ccccccc.cc..",
".gc..ccccc..cg..",
".....ccdcc......",
"....ccd.dcc.....",
"....ccc.ccc....."],
 dict(c="b9ab8c", d="8a7e66", k="2b2620", r="c0392b", n="2e9e4f", g="777777"), None)

T[96] = (["................",
"....kkkkkkkk....",
"...kppppppppk...",
"..kppppppppppk..",
"..kpkkppppkkpk..",
"..kpkkppppkkpk..",
"..kppppppppppk..",
"..kpkkkkkkkkpk..",
"..kpkwkwkwkwpk..",
"..kpkkkkkkkkpk..",
"...kppppppppk...",
"....kkppppkk....",
".....kpppk......",
"......kkk.......",
"................",
"................"],
 dict(k="2a2a2a", p="d9d2c8", w="e8e8e8"), None)

T[49] = (["................",
".....kkkkkk.....",
"....kkkkkkkk....",
"...kkkkkkkkkk...",
"...kwwkkkkwwk...",
"...kwBkkkkBwk...",
"...kwwkkkkwwk...",
"....kkkttkkk....",
".....kktttk.....",
"......ktttk.....",
".....kkktkk.....",
"....kkkkkkkk....",
"...kkgkkkkgkk...",
"...kkkkkkkkkk...",
"..kkkkkkkkkkkk..",
"..kk.kkkkkk.kk.."],
 dict(k="1c1a1a", w="cfcfcf", B="111111", t="5a4f45", g="3a3535"), None)

T[106] = (["................",
"....kkkkkkk.....",
"...kggggggkk....",
"..kgGggggGggk...",
"..kgwwggwwggk...",
"..kgwkggwkggk...",
"..kggggGgggk....",
"..kgkkkkkkgk....",
"...kgwkwkwgk....",
"...kggkkkggk....",
"....kgGggGk.....",
".....kggGk......",
"....kkgGggkk....",
"...kgggggggk....",
"..kggGkkkGggk...",
"..kk.k...k.kk..."],
 dict(k="0d1210", g="2f3b2c", G="1a2418", w="d8d8c0"), None)

T[682] = (["................",
"...............k",
"..k.kk.....kk.kk",
".kkkgggkkkkgggk.",
".kgGgggggggggGk.",
".kgrrgggggggrrk.",
".kgrkgggggggkrk.",
".kgggggggggggk..",
"..kwgwgwgwgwgk..",
"..kkwkwkwkwkk...",
"...kgggggggk....",
"..kgGgggggGgk...",
".kggkgGgGgkggk..",
".kgk.kgggk.kgk..",
".kk..kk.kk..kk..",
"................"],
 dict(k="1a2a17", g="3e6b34", G="2a4a24", r="ff2a1a", w="e8e4d0"), None)

T[939] = (["................",
"................",
"....kkkkkkkk....",
"...krrrrrrrrk...",
"..krRrrrrrrRrk..",
"..krrrrrrrrrrk..",
"..krrrrrrrrrrk..",
"..kRrrrrrrrrRk..",
"..kmmmmmmmmmmk..",
"..kmwmwmwmwmmk..",
"..kmmmmmmmmmmk..",
"...kmwmwmwmmk...",
"....kmmmmmmk....",
".....kkkkkk.....",
"................",
"................"],
 dict(k="5a0f14", r="c4414a", R="a8303a", m="e8808a", w="f4ead8"), None)

T[999] = (["................",
"................",
"......oooo......",
"....ooOOOOoo....",
"...oOOOOOOOOo...",
"..oOOwOOOOwOOo..",
"..oOOkOOOOkOOo..",
"..oOOOOOOOOOOo..",
"..oOkOOOOOOkOo..",
"...oOkkkkkkOo...",
"...ooOOOOOOoo...",
"....ooooooooo...",
"................",
"................",
"................",
"................"],
 dict(o="e8731a", O="ffa040", w="ffffff", k="7a3a0a"), None)

T[17] = (["................",
"....s.ss.s......",
"...ssSSSSss.....",
"..sSSSSSSSSs....",
"..sSrSSSSrSs....",
"..sSSSSSSSSs....",
"...sSSSSSSs.....",
"..ssSSSSSSss....",
".sSSSSSSSSSSs...",
".sSS.SSSS.SSs...",
"..s..SSSS..s....",
"....sSSSSs......",
"....sSS.SSs.....",
"...sSS...SSs....",
"..ss.......ss...",
"................"],
 dict(s="15101c", S="2b2236", r="b02030"), None)

T[23] = (["................",
"..kk........kk..",
".kkkk......kkkk.",
".kkkkkkkkkkkkkk.",
".kkokkkkkkkkokk.",
".kkookkkkkkookk.",
".kkkkkkkkkkkkkk.",
"..kkkkwkkwkkkk..",
"..kkkkkwwkkkk...",
"...kkkkkkkkkk...",
"..kkkkkkkkkkkk..",
".kkgkkkkkkkkgkk.",
".kk.kkkkkkkk.kk.",
".kk..kk..kk..kk.",
".k...k....k...k.",
"................"],
 dict(k="141414", g="2a2a2a", o="ff5a1a", w="eeeeee"), None)

T[131] = (["................",
"................",
".......oo.......",
"......oOOo......",
".....oOOOOo.....",
"....oOOwwOOo....",
"....oOwBBwOo....",
"....oOwBBwOo....",
"....oOOwwOOo....",
".....oOOOOo.....",
".....oOOOOo.....",
"......oOOo......",
"....kkkkkkkk....",
"....kgkggkgk....",
".....kkkkkk.....",
"................"],
 dict(o="a8501a", O="e08a2a", w="ffffff", B="1e6cf0", k="222222", g="555555"), None)

T[1048] = (["................",
"..bb........bb..",
".bBBb......bBBb.",
".bBpb.bbbb.bpBb.",
"..bb.bBBBBb.bb..",
"....bBkBBkBb....",
"....bBBnnBBb....",
"....bBBkkBBb....",
".....bbBBbb.....",
"...bbBBBBBBbb...",
"..bBBBBrBBBBBb..",
"..bBBBBBBBBBBb..",
"...bbBBbbBBbb...",
"...bBBb..bBBb...",
"...bBBb..bBBb...",
"....bb....bb...."],
 dict(b="6b4423", B="9a6a3a", p="d9a0a0", k="111111", n="3a2210", r="a0302a"), None)

T[1013] = (["................",
"......rr........",
".....rRRr.......",
"....rRrRr.......",
"....oooooo......",
"...ookwoooo.....",
"....ooooa.......",
"...sgGsgGs......",
"..sgGGGGGGs.....",
".sgGgGGgGGgs....",
".sgGGGGGGGGgsss.",
"..sgGgGGGgGggGgs",
"...kk.kk....sssg",
"...k..k.......ss",
"................",
"................"],
 dict(r="c0302a", R="ee4a3a", o="e0a020", k="111111", w="ffffff", a="c88a10", s="5a5a2a", g="6e7a34", G="8a9a44"), None)

# ---- items
T[35] = (["................",
"................",
"...kwwwwwwwwk...",
"..kwwwwwwwwwwk..",
".kwwwwwwwwwwwwk.",
".kwwkkwwwwkkwwk.",
".kwkkkkwwkkkkwk.",
".kwwkkwwwwkkwwk.",
".kwwwwwwwwwwwwk.",
".kwwwwkkkkwwwwk.",
"..kwwkgggkkwwk..",
"..kwwwkgkkwwk...",
"...kwwwkkwwk....",
"....kkgkkgkk....",
".....g.gg.g.....",
".....g....g....."],
 dict(k="1a1a1a", w="f2efe6", g="62d03a"), None)

T[500] = (["................",
"......kkkk......",
".....kwwwwk.....",
".....kWWWWk.....",
"......kkkk......",
".....kooooook...",
"....kooooooook..",
"....koowwwwook..",
"....koowrrwook..",
"....koowwwwook..",
"....kooooooook..",
"....koorrrrook..",
"....koorrrrook..",
".....kooooook...",
"......kkkkkk....",
"................"],
 dict(k="3a1f08", w="f0ece0", W="c8c4b8", o="d9831a", r="d02a2a"), None)

T[5] = (["................",
"................",
"...kkkkk........",
"..kggggkk.......",
"..kg..gggk......",
"..kg..gggk......",
"..kggggkk.......",
"...kkgkk........",
"....kgk.........",
"....kgk.........",
"....kggkk.......",
"....kgk.........",
"....kggggk......",
"....kgk.k.......",
".....kk.........",
"................"],
 dict(k="2a2118", g="a89060"), None)

T[268] = (["................",
"................",
"....kkkkkkk.....",
"...kBBBBBBBk....",
"..kBBBBBBBBBk...",
"..kBBBwwBBBBk...",
"..kBBBBBBBBBk...",
"..kBBBBBBBBBk...",
".kkkkkkkkkkkkk..",
".kddddddddddddk.",
"..kkkkkkkkkkkk..",
"................",
"................",
"................",
"................",
"................"],
 dict(k="1a2630", B="4a6a8a", d="34506a", w="c8d8e8"), None)

T[513] = (["................",
".......kk.......",
"......kggk......",
"......kggk......",
".....kkggkk.....",
"....kbBBBBbk....",
"...kbBBBBBBbk...",
"...kbBBwBBBbk...",
"..kbBBBwBBBBbk..",
"..kbBBBBBBBBbk..",
"..kbBBBBBBBBbk..",
".kbbbbbbbbbbbbk.",
".kkkkkkkkkkkkkk.",
".....kdddk......",
"......kdk.......",
"................"],
 dict(k="3a2a10", g="5a4a2a", b="9a6a1a", B="d4a030", w="f8e090", d="4a3a1a"), None)

T[714] = (["................",
"................",
".....kkkkkk.....",
"...kkGGGGGGkk...",
"..kGGgggggGGGk..",
"..kGgkkkkkkgGk..",
".kGgkk....kkgGk.",
".kGgk......kgGk.",
".kGgk......kgGk.",
".kGgkk....kkgGk.",
"..kGgkkkkkkgGk..",
"..kGGgggggGGGk..",
"...kkGGGGGGkk...",
".....kkkkkk.....",
"................",
"................"],
 dict(k="12301a", G="2f7a46", g="58b878"), None)

# ---- blocks (full tiles)
T[914] = (["kkkkkkkkkkkkkkkk",
"kbbbbbbbbbbbbbbk",
"kbkkkgbbbbbkgkbk",
"kbkGGgkbbbkGGgbk",
"kbkGkGgkbkGkGgbk",
"kbkGGGgkkkGGGgbk",
"kbbkkgkbbbkkgkbk",
"kbbbbbbooobbbbbk",
"kbbbbbboOObbbbbk",
"kbbkgkbbbbbkkkbk",
"kbkGGgkbbbkGGgbk",
"kbkGkGgkbkGkGgbk",
"kbkGGGgkbkGGGgbk",
"kbbkkgkbbbbkgkbk",
"kbbbbbbbbbbbbbbk",
"kkkkkkkkkkkkkkkk"],
 dict(k="2a1c0c", b="6a4a22", g="c08a3a", G="e0b050", o="a0a0a0", O="d0d0d0"), "6a4a22")

T[294] = (["kkkkkkkkkkkkkkkk",
"kgggggggggggggk",
"kgBBBBBBBgwwwgk",
"kgBBBBBBBgwwwgk",
"kgBBBBBBBgwwwgk",
"kgBBBBBBBgwwwgk",
"kgBBBBBBBgggggk",
"kggggggggggkkkk",
"kgkkkkkkkkgkgkk",
"kgkwkwkwkwgkkkk",
"kgkwkwkwkwgggkk",
"kgkkkkkkkkgcccg",
"kgggggggggggccg",
"kggkkkkkkkkgcgk",
"kggkrrrrrrkgggk",
"kkkkkkkkkkkkkkk"],
 dict(k="1c1c20", g="8a8e94", B="d8c08a", w="d8d8d8", c="e8e0d0", r="aa2a2a"), "8a8e94")

T[330] = (["6a7078888888886a"[:0] + "8a8e94" * 0 + "ddddddddddddddd" + "d",
"dddddddddddddddd",
"ddddkkkkkkkkdddd",
"dddkaaggaaggkddd",
"dddkgrrggbbakddd",
"ddkaabbaarrgakdd",
"ddkrrgaabbggakdd",
"ddkgbbrraaggrkdd",
"ddkkkkkkkkkkkkdd",
"dddkssssssssskdd",
"ddddkssssssskddd",
"ddddddkkkkkkdddd",
"dddddddddddddddd",
"ddwwwwwwwwwwwwdd",
"ddwkkkkkkkkkkwdd",
"dddddddddddddddd"],
 dict(d="5a5e66", k="20232a", s="b8bcc4", a="e0c030", g="40b040", r="d02a2a", b="3070d0", w="e8e8d0"), "5a5e66")

T[79] = (["kkkkkkkkkkkkkkkk",
"kgggggggggggggk",
"kgkkkkkkkkkkkgk",
"kgkGGGGGGGGGkgk",
"kgkGkGGGGGGGkgk",
"kgkGGGGGGGGGkgk",
"kgkGkkkGGGGGkgk",
"kgkGGGGGGGGGkgk",
"kgkGGGGGGkGGkgk",
"kgkkkkkkkkkkkgk",
"kggggggggggggk",
"kgkkkkkkkkkkkgk",
"kgkggkggkggkgk",
"kgkkkkkkkkkkkgk",
"kggggggggggggk",
"kkkkkkkkkkkkkkk"],
 dict(k="1a1a14", g="b8b098", G="1a3a1a"), "b8b098")
# make the screen glow text lines a brighter green
T[79][1]["G"] = "28502a"; T[79][1]["t"] = "58f060"

T[216] = (["kkkkkkkkkkkkkkkk",
"kgggggggggggggk",
"kgddddddddddddgk"[:15],
"kgdkkkkkkkkkkdgk"[:15],
"kgdkwwwwwwwwkdgk"[:15],
"kgdkwkkwkkwwkdgk"[:15],
"kgdkwwwwwwwwkdgk"[:15],
"kgdkkkkkkkkkkdgk"[:15],
"kgdddddddddddgk"[:15],
"kgdddddkkkdddgk"[:15],
"kgdddddkgkdddgk"[:15],
"kgdddddkkkdddgk"[:15],
"kgdddddddddddgk"[:15],
"kgggggggggggggk",
"kkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkk"],
 dict(k="1c1c20", g="5a5e66", d="7a7e86", w="d0d0d0"), "5a5e66")

T[87] = (["kkkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkkk",
"kggggggkkkkkkkkk",
"kgGGGGGgkkkkkkkk",
"kkkkkkkkgkkkkkkk",
"kkkkkkkkgggkkkkk",
"kkkkgggggGGgkkkk",
"kkkgGGGGgkkkkkkk",
"kkkkkkkkgkkkkkkk",
"kggggkkkkgggkkkk",
"kgGGGggggGGGgkkk",
"kkkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkkk",
"kkkkkkkkkkkkkkkk"],
 dict(k="08080a", g="3a3a40", G="55555e"), "08080a")

T[2] = (["ffffffffffffffff",
"fFfffFffffffFfff",
"ffFFfffFFfffffFf",
"fffffFFffFfffFFf",
"fFffkkkkkkkkffff",
"fffkggggggggkfFf",
"fFfkgkkkkkkgkfff",
"fffkgkgGGGkgkFff",
"ffFkgkgGoGkgkfff",
"fffkgkgGGGkgkfFf",
"fFfkgkkkkkkgkfff",
"fffkggggggggkffF",
"ffFfkkkkkkkkfFff",
"fffFffFfffFfffff",
"fFfffFFffffFFfff",
"ffffffffffffffff"],
 dict(f="b86a5a", F="8e4a42", k="2a2a2e", g="6a6e76", G="8a8e96", o="3a3a3e"), "b86a5a")

T[3] = (["mmmmmmmmmmmmmmmm",
"mkkkkkkkkkkkkkkm",
"mkcccccccccccckm",
"mkcpcccpcccpcckm",
"mkcpcccpcccpcckm",
"mkcpppppcccpcckm",
"mkcccccpppppcckm",
"mkcpcccccccpcckm",
"mkcpcccpcccpcckm",
"mkcpppcpcccpcckm",
"mkcccccpcccpcckm",
"mkccpcccpcccckm",
"mkccpcccpcccckm",
"mkcccccccccccckm",
"mkkkkkkkkkkkkkkm",
"mmmmmmmmmmmmmmmm"],
 dict(m="3a2a1a", k="1c140a", c="7a5a3a", p="e8e4b0"), "7a5a3a")

for n, (rows, leg, bg) in T.items():
    tile(rows, leg, bg).save(OUT / f"scp_{n:04d}.png")

# ---------------------------------------------------------------- mob skins (64x64 zombie UV)
def box(im, ox, oy, w, h, d, col, rnd=None, jit=0):
    r = rnd or random.Random(1)
    regions = [(ox+d, oy, w, d), (ox+d+w, oy, w, d), (ox, oy+d, d, h), (ox+d, oy+d, w, h),
               (ox+d+w, oy+d, d, h), (ox+2*d+w, oy+d, w, h)]
    for rx, ry, rw, rh in regions:
        for x in range(rx, rx+rw):
            for y in range(ry, ry+rh):
                j = r.randint(-jit, jit)
                im.putpixel((x, y), tuple(max(0, min(255, c+j)) for c in col[:3]) + (255,))

PARTS = dict(head=(0, 0, 8, 8, 8), body=(16, 16, 8, 12, 4), rarm=(40, 16, 4, 12, 4),
             larm=(32, 48, 4, 12, 4), rleg=(0, 16, 4, 12, 4), lleg=(16, 48, 4, 12, 4))

def skin(name, n, head, body, limbs=None, legs=None, jit=6, face=None, extra=None):
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    r = random.Random(n)
    limbs = limbs or head; legs = legs or body
    box(im, *PARTS["head"], hexc(head), r, jit)
    box(im, *PARTS["body"], hexc(body), r, jit)
    for p in ("rarm", "larm"): box(im, *PARTS[p], hexc(limbs), r, jit)
    for p in ("rleg", "lleg"): box(im, *PARTS[p], hexc(legs), r, jit)
    P = lambda x, y, c: im.putpixel((x, y), hexc(c))
    if face: face(P)          # face drawn on head front: origin (8,8), 8x8
    if extra: extra(P, r)
    im.save(OUT / f"scp_{n:04d}_skin.png")

def F(P, spec, legend, ox=8, oy=8):
    for y, row in enumerate(spec):
        for x, ch in enumerate(row):
            if ch in legend: P(ox+x, oy+y, legend[ch])

def speckle(cols, count, regions=("body", "rarm", "larm", "rleg", "lleg", "head")):
    def e(P, r):
        for _ in range(count):
            reg = PARTS[r.choice(regions)]
            ox, oy, w, h, d = reg
            x = r.randint(ox, ox+2*d+2*w-1); y = r.randint(oy+d, oy+d+h-1)
            if (x, y) and 0 <= x < 64 and 0 <= y < 64: P(x, y, r.choice(cols))
    return e

# 173: concrete + spray paint streaks
skin("173", 173, "b0a284", "a89a7c", jit=12,
     face=lambda P: F(P, ["........", "........", ".kk..kk.", ".kk..kk.", "........", "..rrrr..", "........", "........"], dict(k="2b2620", r="c0392b")),
     extra=speckle(["c0392b", "2e9e4f", "6a6050"], 70))
# 096: pale, gaunt, black sockets, gaping mouth
skin("096", 96, "d6cfc4", "cdc6ba", jit=5,
     face=lambda P: F(P, ["........", ".kk..kk.", ".kk..kk.", "........", ".kkkkkk.", ".kwkwkk.", ".kkkkkk.", "........"], dict(k="1a1a1a", w="e8e8e8")),
     extra=speckle(["b8b0a4", "e8e2d8"], 40))
# 049: plague doctor
skin("049", 49, "1c1a1a", "1c1a1a", limbs="171515", legs="141212", jit=4,
     face=lambda P: F(P, ["........", ".ww..ww.", ".wB..Bw.", "........", "...tt...", "..tttt..", "...tt...", "........"], dict(w="cfcfcf", B="111111", t="5a4f45")),
     extra=speckle(["2e2a2a", "0e0c0c"], 40))
# 106: rotting old man, black ooze
skin("106", 106, "2f3b2c", "1c2619", jit=9,
     face=lambda P: F(P, ["........", ".ww..ww.", ".wk..wk.", "........", "........", ".kkkkkk.", ".kwkwk..", "........"], dict(k="0d1210", w="d8d8c0")),
     extra=speckle(["0d1210", "4a5a38", "20301c"], 90))
# 682: scaly green with red eyes, teeth
skin("682", 682, "3e6b34", "34602c", limbs="2e5a28", jit=10,
     face=lambda P: F(P, ["........", "kk....kk", "krk..krk", "........", "........", "kkkkkkkk", "kwkwkwkw", "........"], dict(k="1a2a17", r="ff2a1a", w="e8e4d0")),
     extra=speckle(["2a4a24", "4e7e44"], 90))
# 939: translucent red, no eyes, toothy maw
skin("939", 939, "c4414a", "b8383f", limbs="a8303a", legs="a8303a", jit=8,
     face=lambda P: F(P, ["........", "........", "........", "........", ".kkkkkk.", ".mwmwmk.", ".kmmmmk.", "........"], dict(k="5a0f14", m="e8808a", w="f4ead8")),
     extra=speckle(["e8808a", "8a2028"], 50))
# 999: orange gel with a smile
skin("999", 999, "f08a2a", "e8731a", jit=10,
     face=lambda P: F(P, ["........", ".ww..ww.", ".kk..kk.", "........", ".k....k.", "..kkkk..", "........", "........"], dict(k="7a3a0a", w="ffffff")),
     extra=speckle(["ffb060", "d05a10"], 60))
# 017: shadow smoke
skin("017", 17, "1a1424", "15101c", jit=8,
     face=lambda P: F(P, ["........", "........", ".r....r.", "........", "........", "........", "........", "........"], dict(r="b02030")),
     extra=speckle(["2b2236", "0a0710", "3a2e4a"], 90))
# 023: black dog, orange eyes
skin("023", 23, "141414", "101010", jit=7,
     face=lambda P: F(P, ["........", "........", ".oo..oo.", ".oo..oo.", "........", "..kkkk..", ".wk..kw.", "........"], dict(o="ff5a1a", k="050505", w="eeeeee")),
     extra=speckle(["2a2a2a", "050505"], 80))
# 131: eye pod, orange w/ single blue eye (on head front & body front)
def f131(P):
    F(P, ["........", "........", "..wwww..", ".wBBBBw.", ".wBkkBw.", "..wBBw..", "........", "........"], dict(w="ffffff", B="1e6cf0", k="0a1a50"))
skin("131", 131, "e08a2a", "c8721e", jit=7, face=f131, extra=speckle(["a8501a", "f0a040"], 40))
# 1048: teddy bear
skin("1048", 1048, "9a6a3a", "8e5e32", limbs="8e5e32", legs="84562c", jit=8,
     face=lambda P: F(P, ["........", ".kk..kk.", ".kk..kk.", "........", "..dddd..", "..dnnd..", "...kk...", "........"], dict(k="111111", d="d9b890", n="3a2210")),
     extra=speckle(["a87a48", "6b4423", "d9a0a0"], 50))
# 1013: reptile with rooster head
skin("1013", 1013, "e0a020", "6e7a34", limbs="5a6a2a", legs="5a6a2a", jit=9,
     face=lambda P: F(P, ["..rrrr..", ".rRRRRr.", "........", ".kw..wk.", "...aa...", "..aaaa..", "..rRRr..", "........"], dict(r="c0302a", R="ee4a3a", k="111111", w="ffffff", a="c88a10")),
     extra=speckle(["8a9a44", "4a5a22"], 90, ("body", "rarm", "larm", "rleg", "lleg")))
print("wrote", len(T), "tiles")
