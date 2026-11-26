#!/usr/bin/env python3
"""
Generates everything data-driven for the SCP Foundation mod:
  - src/main/resources/scp_registry.json        (SCP-0000..SCP-2000 definitions read by the mod at startup)
  - assets: lang, item definitions, item/block models, blockstates, textures
  - data:   block loot tables
Re-run after editing tools/scp_overrides.psv:   python3 tools/generate_resources.py
Requires Pillow.
"""
import json, random, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import icons

MODID = "scpfoundation"
ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets" / MODID
DATA = RES / "data" / MODID

ENTITY_BEHAVIORS = ["WATCHED_FREEZE", "TELEPORT_STRIKE", "FIRE_AURA", "POISON_TOUCH", "REGEN", "DARKNESS_AURA",
                    "HEAL_AURA", "RAGE_WHEN_LOOKED", "WEAKEN_TOUCH", "WITHER_AURA", "LEVITATE_TOUCH", "FAST", "BLINK",
                    "BLIND_STARE", "SLOW_FIELD", "THORNS", "EXPLODE_ON_DEATH", "SUMMON_MINIONS", "PASSIVE",
                    "PULL_PLAYERS"]
HOSTILE_POOL = [b for b in ENTITY_BEHAVIORS if b not in ("PASSIVE", "HEAL_AURA")]
SAFE_ENTITY_POOL = ["PASSIVE", "HEAL_AURA", "REGEN", "SLOW_FIELD", "BLINK"]
ITEM_BEHAVIORS = ["HEAL", "SPEED_BURST", "NIGHT_VISION", "LEVITATE_SELF", "BLINK", "REGENERATION", "FIRE_PROOF",
                  "STRENGTH", "FEED", "REPEL", "ABSORB_COST", "RESIST"]
BLOCK_BEHAVIORS = ["LAUNCH_PAD", "HARM_ON_STEP", "SLOW_ON_STEP", "USE_EFFECT", "USE_TELEPORT", "USE_LOOT",
                   "HEAL_ON_USE"]
SAFE_BLOCK_POOL = ["LAUNCH_PAD", "USE_EFFECT", "USE_LOOT", "HEAL_ON_USE"]

CLASS_STATS = {  # hp, dmg, number of behaviors
    "Safe": (20, 2, 1), "Euclid": (40, 6, 2), "Keter": (100, 12, 3), "Thaumiel": (80, 4, 2), "Apollyon": (250, 20, 3),
}
CLASS_COLORS = {
    "Safe": (70, 170, 80), "Euclid": (215, 175, 45), "Keter": (190, 55, 55),
    "Thaumiel": (100, 80, 200), "Apollyon": (30, 30, 30),
}

DIGITS = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
}


def write(path: Path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, (dict, list)):
        content = json.dumps(content, indent=2, ensure_ascii=False)
    path.write_text(content, encoding="utf-8")


def sid(n):
    return f"scp_{n:04d}"


def load_overrides():
    out = {}
    for line in (ROOT / "tools/scp_overrides.psv").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        n, name, cls, form, beh, height, color = (line.split("|") + ["", "", ""])[:7]
        out[int(n)] = dict(name=name, cls=cls, form=form, behaviors=[b for b in beh.split(";") if b],
                           height=float(height) if height else None, color=color or None)
    return out


def load_wiki():
    f = ROOT / "tools" / "scp_wiki_data.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


ENTITY_TAGS = {"humanoid", "sapient", "sentient", "animal", "mammal", "reptilian", "avian", "insect", "arachnid", "feline",
               "canine", "hostile", "alive", "biological", "fish", "plant", "cognitohazard", "predatory", "ghost", "spirit",
               "aquatic", "amphibian", "uncontained", "mind-affecting"}
BLOCK_TAGS = {"location", "structure", "building", "room", "portal", "door", "extradimensional", "site-specific", "tree"}
COLOR_RGB = {"black": (25, 25, 28), "white": (225, 225, 225), "grey": (130, 130, 135), "gray": (130, 130, 135),
             "red": (170, 40, 40), "crimson": (150, 20, 40), "green": (70, 130, 60), "blue": (60, 90, 170),
             "yellow": (210, 190, 60), "orange": (225, 130, 40), "purple": (110, 60, 150), "violet": (110, 60, 150),
             "pink": (220, 140, 170), "brown": (110, 80, 50), "gold": (205, 170, 50), "golden": (205, 170, 50),
             "silver": (180, 185, 190), "pale": (210, 200, 190), "tan": (190, 160, 120), "beige": (205, 190, 160),
             "dark": (40, 40, 48)}
TAG_RGB = {"reptilian": (70, 110, 60), "feline": (200, 130, 60), "canine": (110, 90, 70), "avian": (150, 150, 170),
           "insect": (90, 70, 40), "arachnid": (50, 40, 40), "aquatic": (50, 100, 140), "plant": (60, 120, 60),
           "ghost": (170, 190, 200), "spirit": (170, 190, 200), "humanoid": (150, 130, 115)}
CLASS_SKIN = {"Safe": (110, 140, 115), "Euclid": (120, 115, 100), "Keter": (95, 45, 45),
              "Thaumiel": (80, 70, 130), "Apollyon": (28, 28, 30)}
CLASS_EYES = CLASS_COLORS


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def skin_color(d, wiki):
    if d.get("color"):
        return hex_rgb(d["color"])
    for c in (wiki or {}).get("colors", []):
        if c in COLOR_RGB:
            return COLOR_RGB[c]
    for t in (wiki or {}).get("tags", []):
        if t in TAG_RGB:
            return TAG_RGB[t]
    return CLASS_SKIN[d["cls"]]


def entity_skin(n, rgb, eyes, title=""):
    """64x64 humanoid (zombie UV layout) skin: tinted body, per-SCP eyes/mouth/pattern/clothing so every mob differs."""
    r = random.Random(n * 97 + 5)
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    px = img.load()
    pattern = r.choice(["none", "stripes", "spots", "patches", "bands"])
    cloth = tuple(r.randint(20, 120) for _ in range(3))
    has_cloth = r.random() < 0.55
    n_eyes = 1 if "eye" in title.lower() and r.random() < .5 else r.choice([2, 2, 2, 3, 4])
    def body(x0, y0, x1, y1, scale, cl=False):
        for y in range(y0, y1):
            for x in range(x0, x1):
                j = r.randint(-9, 9)
                c = tuple(max(0, min(255, int(v * scale) + j)) for v in (cloth if cl else rgb))
                if not cl:
                    if pattern == "stripes" and (x + y) % 6 < 2: c = tuple(int(v * .7) for v in c)
                    if pattern == "spots" and r.random() < .08: c = tuple(int(v * .6) for v in c)
                    if pattern == "patches" and ((x // 3 + y // 3) % 4 == 0): c = tuple(int(v * .78) for v in c)
                    if pattern == "bands" and y % 5 == 0: c = tuple(min(255, int(v * 1.2)) for v in c)
                px[x, y] = (*c, 255)
    body(0, 0, 32, 16, 1.10)              # head (front face is x 8..16, y 8..16)
    body(16, 16, 40, 32, 0.80, has_cloth) # torso
    body(40, 16, 56, 32, 0.95)            # arm
    body(32, 48, 48, 64, 0.95)            # arm
    body(0, 16, 16, 32, 0.65, has_cloth)  # leg
    body(16, 48, 32, 64, 0.65, has_cloth) # leg
    ex = {1: [11], 2: [10, 13], 3: [9, 11, 14], 4: [9, 10, 13, 14]}[n_eyes]
    for x in ex:
        px[x, 12] = (*eyes, 255)
        if n_eyes == 4: px[x, 11] = (*eyes, 255)
    mouth = r.choice(["flat", "grin", "none", "wide"])
    if mouth == "flat":
        for x in range(10, 14): px[x, 14] = (20, 20, 20, 255)
    elif mouth == "grin":
        for x in range(9, 15): px[x, 14] = (230, 230, 230, 255)
    elif mouth == "wide":
        for x in range(9, 15): px[x, 14] = (30, 10, 10, 255); px[x, 15] = (30, 10, 10, 255)
    return img


def load_names():
    """Real wiki titles for SCP-001..SCP-2000 (names_series1.txt / names_series2.txt)."""
    out = {}
    for fn in ("names_series1.txt", "names_series2.txt"):
        for line in (ROOT / "tools" / fn).read_text(encoding="utf-8").splitlines():
            if "|" in line:
                n, title = line.split("|", 1)
                out[int(n)] = title.strip()
    return out


# Survival crafting: shapeless, one class-tier ingredient + 3 distinct pool items, unique per SCP.
TIER_ITEM = {"Safe": "minecraft:iron_ingot", "Euclid": "minecraft:gold_ingot", "Keter": "minecraft:diamond",
             "Thaumiel": "minecraft:emerald", "Apollyon": "minecraft:nether_star"}
POOL = ["redstone", "lapis_lazuli", "coal", "copper_ingot", "quartz", "amethyst_shard", "glowstone_dust", "gunpowder",
        "bone", "string", "slime_ball", "ender_pearl", "blaze_powder", "prismarine_shard", "spider_eye", "rotten_flesh",
        "leather", "feather", "flint", "sugar", "gold_nugget", "iron_nugget", "paper", "ink_sac", "glow_ink_sac",
        "honeycomb", "phantom_membrane", "magma_cream", "fermented_spider_eye", "clay_ball"]
import itertools
COMBOS = list(itertools.combinations(POOL, 3))


# ---- wiki tag -> in-game form / behaviours ---------------------------------------------------------------
STRONG_ENTITY = {"humanoid", "animal", "bird", "insect", "hostile", "mobile", "predatory", "child", "swarm", "invertebrate",
                 "mammalian", "reptilian", "feline", "canine", "rodent", "fish", "amphibian", "murder-monster"}
SOFT_ENTITY = {"alive", "sapient", "biological", "species", "aquatic", "autonomous", "cadaver", "sentient", "ghost", "spirit"}
NOT_ENTITY = {"plant", "location", "building", "structure", "portal", "city", "document", "artifact", "tool", "toy",
              "appliance", "vehicle", "food", "weapon", "clothing", "electronic", "computer", "tree", "liquid", "game", "media"}
BLOCK_TAG_SET = {"location", "building", "structure", "portal", "city", "subterranean", "geological", "room", "site-specific",
                 "tree", "extradimensional-location"}

ENTITY_TAG_BEH = [("observational", "WATCHED_FREEZE"), ("fire", "FIRE_AURA"), ("toxic", "POISON_TOUCH"), ("venom", "POISON_TOUCH"),
                  ("corrosive", "POISON_TOUCH"), ("contagion", "WEAKEN_TOUCH"), ("biohazard", "WEAKEN_TOUCH"),
                  ("parasitic", "WEAKEN_TOUCH"), ("teleportation", "BLINK"), ("spatial", "TELEPORT_STRIKE"),
                  ("cognitohazard", "BLIND_STARE"), ("visual", "BLIND_STARE"), ("darkness", "DARKNESS_AURA"),
                  ("shadow", "DARKNESS_AURA"), ("telekinetic", "PULL_PLAYERS"), ("reanimation", "SUMMON_MINIONS"),
                  ("swarm", "SUMMON_MINIONS"), ("indestructible", "REGEN"), ("hard-to-destroy", "REGEN"),
                  ("self-repairing", "REGEN"), ("regenerat", "REGEN"), ("temporal", "SLOW_FIELD"), ("cold", "SLOW_FIELD"),
                  ("ice", "SLOW_FIELD"), ("sleep", "SLOW_FIELD"), ("radioactive", "WITHER_AURA"), ("necrotic", "WITHER_AURA"),
                  ("explosive", "EXPLODE_ON_DEATH"), ("electrical", "THORNS"), ("flight", "LEVITATE_TOUCH"),
                  ("mind-affecting", "WEAKEN_TOUCH"), ("murder-monster", "FAST"), ("predatory", "FAST"), ("healing", "HEAL_AURA"),
                  ("medical", "HEAL_AURA")]
ITEM_TAG_BEH = [("medical", "HEAL"), ("healing", "HEAL"), ("regenerat", "REGENERATION"), ("teleportation", "BLINK"),
                ("spatial", "BLINK"), ("food", "FEED"), ("light", "NIGHT_VISION"), ("fire", "FIRE_PROOF"), ("weapon", "STRENGTH"),
                ("temporal", "SPEED_BURST"), ("telekinetic", "REPEL"), ("indestructible", "RESIST"), ("clothing", "RESIST"),
                ("armor", "RESIST"), ("flight", "LEVITATE_SELF"), ("mind-affecting", "ABSORB_COST"),
                ("cognitohazard", "ABSORB_COST"), ("tool", "SPEED_BURST"), ("electronic", "NIGHT_VISION")]
BLOCK_TAG_BEH = [("portal", "USE_TELEPORT"), ("teleportation", "USE_TELEPORT"), ("extradimensional", "USE_TELEPORT"),
                 ("food", "USE_LOOT"), ("appliance", "USE_LOOT"), ("artifact", "USE_EFFECT"), ("medical", "HEAL_ON_USE"),
                 ("toxic", "HARM_ON_STEP"), ("biohazard", "HARM_ON_STEP"), ("hostile", "HARM_ON_STEP"),
                 ("corrosive", "HARM_ON_STEP"), ("temporal", "SLOW_ON_STEP"), ("sleep", "SLOW_ON_STEP"),
                 ("mechanical", "LAUNCH_PAD"), ("vehicle", "LAUNCH_PAD"), ("spatial", "USE_TELEPORT")]


def form_from_tags(tags):
    t = set(tags)
    if t & BLOCK_TAG_SET and not (t & {"humanoid", "animal", "bird", "insect"}):
        return "block"
    if t & STRONG_ENTITY and not (t & NOT_ENTITY - {"clothing"} and not t & {"humanoid", "animal", "bird", "insect"}):
        return "entity"
    if t & SOFT_ENTITY and not t & NOT_ENTITY:
        return "entity"
    return "item"


def behaviours_from_tags(tags, form, cls):
    t = list(tags)
    table = ENTITY_TAG_BEH if form == "entity" else ITEM_TAG_BEH if form == "item" else BLOCK_TAG_BEH
    out = []
    for key, b in table:
        if any(key in x for x in t) and b not in out:
            out.append(b)
    limit = CLASS_STATS[cls][2]
    if form == "entity":
        friendly = cls in ("Safe", "Thaumiel") and not set(t) & {"hostile", "predatory", "murder-monster", "horror"}
        if friendly:
            out = [b for b in out if b in ("HEAL_AURA", "REGEN", "SLOW_FIELD", "BLINK", "PASSIVE", "LEVITATE_TOUCH")] or []
            if "PASSIVE" not in out:
                out.insert(0, "PASSIVE")
    return out[:limit]


def procedural(n, wiki=None, title=""):
    r = random.Random(n * 7919 + 13)
    roll = r.random()
    cls = ("Safe" if roll < .34 else "Euclid" if roll < .74 else "Keter" if roll < .92
           else "Thaumiel" if roll < .96 else "Apollyon" if roll < .98 else "Euclid")
    form = r.choices(["item", "entity", "block"], weights=[40, 35, 25])[0]
    tags = (wiki or {}).get("tags") or []
    if wiki and wiki.get("cls"):
        cls = wiki["cls"]
    if tags:
        form = form_from_tags(tags)
    elif title:
        form = icons.form_hint(title)
    count = CLASS_STATS[cls][2]
    beh = behaviours_from_tags(tags, form, cls) if tags else []
    if not beh:
        if form == "entity":
            pool = SAFE_ENTITY_POOL if cls in ("Safe", "Thaumiel") else HOSTILE_POOL
        elif form == "item":
            pool = ITEM_BEHAVIORS
        else:
            pool = SAFE_BLOCK_POOL if cls in ("Safe", "Thaumiel") else BLOCK_BEHAVIORS
        beh = r.sample(pool, min(max(1, count - (1 if form != "entity" else 0)), len(pool)))
    return dict(name=f"SCP-{n:04d}", cls=cls, form=form, behaviors=beh)


def texture(n, cls, form, rows):
    r = random.Random(n * 31 + 7)
    base = CLASS_COLORS[cls]
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            j = r.randint(-12, 12)
            c = tuple(max(0, min(255, int(v * 0.40) + j)) for v in base)
            px[x, y] = (*c, 255)
    for i in range(16):  # class-coloured border
        for (x, y) in ((i, 0), (i, 15), (0, i), (15, i)):
            px[x, y] = (*base, 255)
    if form == "entity":  # corner marks
        for (x, y) in ((1, 1), (14, 1), (1, 14), (14, 14)):
            px[x, y] = (255, 255, 255, 255)
    if form == "block":  # inner frame
        for i in range(2, 14):
            for (x, y) in ((i, 2), (i, 13), (2, i), (13, i)):
                px[x, y] = (*base, 255)
    light = tuple(min(255, int(v * 0.55 + 140)) for v in base)
    for dy, row in enumerate(rows):  # 8x8 icon, top
        for dx, ch in enumerate(row):
            if ch == "#":
                px[4 + dx, 1 + dy] = (*light, 255)
    s = f"{n:04d}"
    ox = 1
    for ch in s:  # tiny number, bottom
        for dy, row in enumerate(DIGITS[ch]):
            for dx, bit in enumerate(row):
                if bit == "1":
                    px[ox + dx, 10 + dy] = (255, 255, 255, 255) if cls != "Apollyon" else (220, 40, 40, 255)
        ox += 4
    return img


def simple_tex(fn):
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = fn(x, y)
    return img


def facility_textures():
    tex = {}
    tex["containment_wall"] = simple_tex(lambda x, y: (190, 192, 196, 255) if (x % 8 and y % 8) else (120, 122, 128, 255))
    tex["reinforced_floor"] = simple_tex(lambda x, y: (70, 72, 78, 255) if (x + y) % 4 else (95, 98, 105, 255))
    tex["hazard_stripe"] = simple_tex(lambda x, y: (235, 200, 30, 255) if ((x + y) // 4) % 2 == 0 else (25, 25, 25, 255))
    tex["containment_lamp"] = simple_tex(lambda x, y: (255, 245, 200, 255) if 3 <= x <= 12 and 3 <= y <= 12 else (150, 150, 155, 255))
    tex["foundation_logo"] = simple_tex(lambda x, y: (240, 240, 240, 255) if 36 <= (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 49 else (20, 20, 24, 255))
    lvl_cols = [(120, 120, 120), (80, 160, 255), (90, 200, 90), (230, 200, 60), (230, 130, 40), (200, 50, 50)]
    for lvl, col in enumerate(lvl_cols):
        tex[f"keycard_door_{lvl}"] = simple_tex(
            lambda x, y, col=col: (*col, 255) if 5 <= x <= 10 and 2 <= y <= 4 else
            (55, 58, 64, 255) if x in (0, 15) or y in (0, 15) else (100, 104, 112, 255))
    return tex, lvl_cols


def item_tex_keycard(col):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y in range(4, 12):
        for x in range(2, 14):
            px[x, y] = (235, 235, 235, 255)
    for x in range(2, 14):
        for y in (4, 5):
            px[x, y] = (*col, 255)
    for x in range(3, 7):
        px[x, 9] = (60, 60, 60, 255)
    return img


def item_tex_gun():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for x in range(3, 13):
        for y in (6, 7):
            px[x, y] = (60, 70, 85, 255)
    for y in range(8, 12):
        px[5, y] = (40, 40, 45, 255)
        px[6, y] = (40, 40, 45, 255)
    px[13, 6] = px[14, 6] = (230, 60, 60, 255)
    return img


def main():
    over = load_overrides()
    names = load_names()
    wiki = load_wiki()
    n_titles = len(names)
    entries, lang = [], {}
    n_item = n_entity = n_block = 0
    n_scaled = 0
    class_fixed = []
    class_counter = {}
    import shutil
    for old in (ASSETS, DATA):  # everything under these is generated; clear stale files from earlier runs
        shutil.rmtree(old, ignore_errors=True)
    (ASSETS / "textures/entity/scp").mkdir(parents=True, exist_ok=True)
    custom = ROOT / "tools" / "custom_art"   # drop-in: scp_0173.png (16x16 tile) / scp_0173_skin.png (64x64 mob skin)
    for n in range(0, 2001):
        w = wiki.get(str(n)) or {}
        title = names.get(n) or (over.get(n) or {}).get("name") or f"SCP-{n:04d}"
        d = dict(over.get(n) or procedural(n, w, title))
        if w.get("cls"):
            if over.get(n) and d["cls"] != w["cls"]:
                class_fixed.append((n, d["cls"], w["cls"]))
            d["cls"] = w["cls"]           # the wiki's own object class always wins
        cls, form, beh = d["cls"], d["form"], d["behaviors"]
        height = d.get("height") or w.get("height")
        size_src = (w.get("height_src") or "wiki") if height else "default"
        if form == "entity" and height:
            scale = round(max(0.25, min(4.0, height / 1.95)), 2)
        elif form == "entity":
            scale, size_src = icons.scale_hint(title, w.get("tags"))
        else:
            scale = 1.0
        n_scaled += scale != 1.0
        hp, dmg, _ = CLASS_STATS[cls]
        i = sid(n)
        icon_name, icon_rows = icons.pixels(n, title, w.get("tags"), w.get("desc", ""))
        k = class_counter.get(cls, 0)
        class_counter[cls] = k + 1
        recipe = [TIER_ITEM[cls]] + [f"minecraft:{x}" for x in COMBOS[k]]
        write(DATA / f"recipe/{i}.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                          "ingredients": recipe, "result": {"id": f"{MODID}:{i}", "count": 1}})
        entries.append(dict(n=n, id=i, name=title, cls=cls, form=form, canon=(n in over) or bool(w.get('cls')),
                            behaviors=beh, hp=hp, dmg=dmg, recipe=recipe, scale=scale, height=height or 0, size_src=size_src,
                            icon=icon_name))
        if form == "entity":
            skin_file = custom / f"scp_{n:04d}_skin.png"
            if skin_file.exists():
                shutil.copy(skin_file, ASSETS / f"textures/entity/scp/{i}.png")
            else:
                entity_skin(n, skin_color(d, w), CLASS_EYES[cls], title).save(ASSETS / f"textures/entity/scp/{i}.png")
        label = f"SCP-{n:04d}: {title}"
        kind = "block" if form == "block" else "item"
        lang[f"{kind}.{MODID}.{i}"] = label
        img = texture(n, cls, form, icon_rows)
        tile_file = custom / f"scp_{n:04d}.png"
        if tile_file.exists():
            img = Image.open(tile_file).convert("RGBA")
        (ASSETS / "textures/item").mkdir(parents=True, exist_ok=True)
        (ASSETS / "textures/block").mkdir(parents=True, exist_ok=True)
        if form == "block":
            n_block += 1
            img.save(ASSETS / f"textures/block/{i}.png")
            write(ASSETS / f"models/block/{i}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MODID}:block/{i}"}})
            write(ASSETS / f"blockstates/{i}.json", {"variants": {"": {"model": f"{MODID}:block/{i}"}}})
            write(ASSETS / f"items/{i}.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:block/{i}"}})
            write(DATA / f"loot_table/blocks/{i}.json", {
                "type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MODID}:{i}"}],
                                                      "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
        else:
            n_entity += form == "entity"
            n_item += form == "item"
            img.save(ASSETS / f"textures/item/{i}.png")
            write(ASSETS / f"models/item/{i}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{i}"}})
            write(ASSETS / f"items/{i}.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:item/{i}"}})

    # facility blocks
    tex, lvl_cols = facility_textures()
    fac_blocks = ["containment_wall", "reinforced_floor", "hazard_stripe", "containment_lamp", "foundation_logo"] + \
                 [f"keycard_door_{l}" for l in range(6)]
    names = {"containment_wall": "Containment Wall", "reinforced_floor": "Reinforced Floor", "hazard_stripe": "Hazard Stripe Block",
             "containment_lamp": "Containment Lamp", "foundation_logo": "Foundation Logo Block"}
    for l in range(6):
        names[f"keycard_door_{l}"] = f"Level {l} Keycard Door"
    for b in fac_blocks:
        tex[b].save(ASSETS / f"textures/block/{b}.png")
        lang[f"block.{MODID}.{b}"] = names[b]
        if b.startswith("keycard_door_"):
            for state in ("open", "closed"):
                write(ASSETS / f"models/block/{b}_{state}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MODID}:block/{b}"}})
            write(ASSETS / f"blockstates/{b}.json", {"variants": {
                "open=false": {"model": f"{MODID}:block/{b}_closed"}, "open=true": {"model": f"{MODID}:block/{b}_open"}}})
        else:
            write(ASSETS / f"models/block/{b}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MODID}:block/{b}"}})
            write(ASSETS / f"blockstates/{b}.json", {"variants": {"": {"model": f"{MODID}:block/{b}"}}})
        write(ASSETS / f"items/{b}.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:block/{b if not b.startswith('keycard_door_') else b + '_closed'}"}})
        write(DATA / f"loot_table/blocks/{b}.json", {
            "type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MODID}:{b}"}],
                                                  "conditions": [{"condition": "minecraft:survives_explosion"}]}]})

    # facility recipes (survival)
    def shapeless(rid, ings, out, count=1):
        write(DATA / f"recipe/{rid}.json", {"type": "minecraft:crafting_shapeless", "category": "building",
                                            "ingredients": ings, "result": {"id": f"{MODID}:{out}", "count": count}})
    write(DATA / "recipe/containment_wall.json", {
        "type": "minecraft:crafting_shaped", "category": "building", "pattern": ["SIS", "ISI", "SIS"],
        "key": {"S": "minecraft:smooth_stone", "I": "minecraft:iron_ingot"},
        "result": {"id": f"{MODID}:containment_wall", "count": 8}})
    shapeless("reinforced_floor", [f"{MODID}:containment_wall", "minecraft:iron_ingot"], "reinforced_floor", 2)
    shapeless("hazard_stripe", [f"{MODID}:containment_wall", "minecraft:yellow_dye", "minecraft:black_dye"], "hazard_stripe", 2)
    shapeless("containment_lamp", [f"{MODID}:containment_wall", "minecraft:glowstone"], "containment_lamp")
    shapeless("foundation_logo", [f"{MODID}:containment_wall", "minecraft:black_dye", "minecraft:white_dye"], "foundation_logo", 2)
    shapeless("keycard_0", ["minecraft:paper", "minecraft:iron_ingot"], "keycard_0")
    upgrades = ["minecraft:copper_ingot", "minecraft:gold_ingot", "minecraft:diamond", "minecraft:netherite_ingot", "minecraft:nether_star"]
    for l in range(1, 6):
        shapeless(f"keycard_{l}", [f"{MODID}:keycard_{l-1}", upgrades[l - 1]], f"keycard_{l}")
    for l in range(6):
        shapeless(f"keycard_door_{l}", [f"{MODID}:containment_wall", "minecraft:redstone", f"{MODID}:keycard_{l}"], f"keycard_door_{l}")
    write(DATA / "recipe/tranquilizer_gun.json", {
        "type": "minecraft:crafting_shaped", "category": "equipment", "pattern": ["III", " SR"],
        "key": {"I": "minecraft:iron_ingot", "S": "minecraft:stick", "R": "minecraft:redstone"},
        "result": {"id": f"{MODID}:tranquilizer_gun", "count": 1}})

    # facility items
    for l, col in enumerate(lvl_cols):
        item_tex_keycard(col).save(ASSETS / f"textures/item/keycard_{l}.png")
        write(ASSETS / f"models/item/keycard_{l}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/keycard_{l}"}})
        write(ASSETS / f"items/keycard_{l}.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:item/keycard_{l}"}})
        lang[f"item.{MODID}.keycard_{l}"] = f"Level {l} Keycard"
    item_tex_gun().save(ASSETS / "textures/item/tranquilizer_gun.png")
    write(ASSETS / "models/item/tranquilizer_gun.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/tranquilizer_gun"}})
    write(ASSETS / "items/tranquilizer_gun.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:item/tranquilizer_gun"}})
    lang[f"item.{MODID}.tranquilizer_gun"] = "Tranquilizer Gun"

    # entity texture (zombie UV layout, flat dark placeholder with lighter head/limb panels)
    ent = Image.new("RGBA", (64, 64), (45, 48, 55, 255))
    epx = ent.load()
    for y in range(64):
        for x in range(64):
            if (x // 4 + y // 4) % 2:
                epx[x, y] = (52, 55, 63, 255)
    (ASSETS / "textures/entity").mkdir(parents=True, exist_ok=True)
    ent.save(ASSETS / "textures/entity/scp_entity.png")
    lang[f"entity.{MODID}.scp_entity"] = "SCP Entity"

    for tab, label in (("foundation", "SCP: Foundation Gear"), ("safe", "SCP: Safe"), ("euclid", "SCP: Euclid"),
                       ("keter", "SCP: Keter"), ("other", "SCP: Thaumiel / Apollyon")):
        lang[f"itemGroup.{MODID}.{tab}"] = label

    write(RES / "scp_registry.json", {"version": 1, "entries": entries})
    write(ASSETS / "lang/en_us.json", lang)
    if class_fixed:
        print("Classes corrected from wiki:", ", ".join(f"{a}:{b}->{c}" for a, b, c in class_fixed))
    uniq = {tuple(sorted(e["recipe"])) for e in entries}
    assert len(uniq) == len(entries), "recipe collision"
    print(f"Generated {len(entries)} SCPs: {n_item} items, {n_entity} entities, {n_block} blocks, "
          f"{sum(1 for e in entries if e['canon'])} with authored class/behaviors, {n_titles} real wiki titles, "
          f"{len(uniq)} unique recipes, {n_scaled} entities with a custom size, "
          f"{len(wiki)} entries of wiki data loaded")


if __name__ == "__main__":
    sys.exit(main())
