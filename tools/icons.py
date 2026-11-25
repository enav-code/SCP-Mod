"""
Original 8x8 pixel icons + keyword rules, so every SCP's item/block tile and mob skin looks like its title.
Icons are drawn here (original, no third-party art). Unmatched titles get a unique symmetric glyph seeded by SCP number.
"""
import random

ICONS = {
"key": ["..####..", ".#....#.", ".#....#.", "..####..", "...##...", "...###..", "...##...", "...###.."],
"mask": ["..####..", ".######.", "##.##.##", "########", "########", ".##..##.", "..####..", "...##..."],
"book": [".######.", "##....##", "##.##.##", "##....##", "##.##.##", "##....##", "########", ".######."],
"eye": ["........", "..####..", ".#.##.#.", "##.##.##", ".#.##.#.", "..####..", "........", "........"],
"tree": ["...##...", "..####..", ".######.", "..####..", ".######.", "...##...", "...##...", "..####.."],
"skull": [".######.", "########", "##.##.##", "########", ".######.", "..####..", "..#..#..", "........"],
"door": [".######.", ".#....#.", ".#....#.", ".#....#.", ".#...##.", ".#....#.", ".#....#.", ".######."],
"box": ["........", ".######.", "########", "#......#", "#......#", "#......#", "########", "........"],
"clock": ["..####..", ".#....#.", "#..#...#", "#..#...#", "#..###.#", "#......#", ".#....#.", "..####.."],
"mirror": ["..####..", ".#....#.", "#.#....#", "#..#...#", "#......#", ".#....#.", "..####..", "...##..."],
"doll": ["..####..", "..#..#..", "..####..", "...##...", ".######.", "...##...", "..#..#..", "..#..#.."],
"bottle": ["...##...", "...##...", "..####..", ".######.", ".######.", ".######.", ".######.", "..####.."],
"bug": ["#..##..#", ".#.##.#.", "..####..", "########", "..####..", ".######.", "#..##..#", "........"],
"fish": ["........", "..####.#", ".#######", "##.#####", ".#######", "..####.#", "........", "........"],
"bird": ["........", "...##...", "..####.#", ".#######", "########", "..####..", "...#.#..", "........"],
"cat": ["#.#..#.#", "########", "#.####.#", "########", ".######.", "..####..", "..#..#..", "........"],
"dog": ["##....##", "########", "#.####.#", ".######.", "..####..", ".######.", ".#.##.#.", "........"],
"hand": ["..#.#...", ".######.", ".######.", "########", "########", ".######.", "..####..", "..####.."],
"heart": [".##..##.", "########", "########", "########", ".######.", "..####..", "...##...", "........"],
"house": ["...##...", "..####..", ".######.", "########", ".#....#.", ".#.##.#.", ".#.##.#.", ".######."],
"tower": ["#.#..#.#", "########", ".######.", "..####..", "..####..", "..####..", ".######.", "########"],
"bone": ["##....##", "##....##", ".######.", "..####..", "..####..", ".######.", "##....##", "##....##"],
"flame": ["....#...", "...##...", "..###.#.", "..#####.", ".######.", ".######.", "..####..", "........"],
"drop": ["...##...", "...##...", "..####..", ".######.", "########", "########", ".######.", "..####.."],
"star": ["...##...", "...##...", "########", ".######.", "..####..", ".##..##.", ".#....#.", "........"],
"gear": ["..#..#..", ".######.", "###..###", "#......#", "###..###", ".######.", "..#..#..", "........"],
"phone": [".######.", ".#....#.", ".#....#.", ".######.", ".######.", ".#.#.#..", ".######.", ".######."],
"tv": [".#....#.", "..#..#..", "########", "#......#", "#......#", "#......#", "########", "..#..#.."],
"ring": ["..####..", ".#....#.", "#......#", "#......#", ".#....#.", "..####..", "...##...", "........"],
"sword": ["......##", ".....##.", "....##..", "...##...", "#.##....", ".##.....", "##.#....", "#..#...."],
"crown": ["#..##..#", "########", "########", "########", ".######.", "........", "........", "........"],
"flower": ["..#..#..", ".#.##.#.", "..####..", ".######.", "..####..", "...##...", "...##...", "..####.."],
"snake": [".####...", "#....#..", "#.......", ".####...", "....#...", "#...#...", ".###....", "........"],
"spider": ["#..##..#", ".#.##.#.", "..####..", "########", "..####..", ".#.##.#.", "#..##..#", "........"],
"ghost": ["..####..", ".######.", "##.##.##", "########", "########", "########", "#.#..#.#", "........"],
"planet": ["..####..", ".######.", "########", "########", "########", ".######.", "..####..", "........"],
"tooth": [".######.", "########", "########", ".######.", ".##..##.", ".##..##.", ".#....#.", "........"],
"camera": ["..####..", "########", "#..##..#", "#.####.#", "#..##..#", "########", "........", "........"],
"note": ["...####.", "...#..#.", "...#..#.", "...#....", ".###....", "####....", ".##.....", "........"],
"lock": ["..####..", ".#....#.", ".#....#.", "########", "###..###", "###..###", "########", "########"],
"pill": ["..####..", ".######.", "########", "########", "########", "########", ".######.", "..####.."],
"cloud": ["........", "..###...", ".#####.#", "########", "########", ".######.", "........", "........"],
"mushroom": ["..####..", ".######.", "########", "########", "...##...", "...##...", "..####..", "........"],
"human": ["..####..", "..####..", "...##...", ".######.", "#.####.#", "#..##..#", "..#..#..", "..#..#.."],
"water": ["........", "#..##..#", ".##..##.", "........", "#..##..#", ".##..##.", "........", "........"],
"vehicle": ["........", "..####..", ".######.", "########", "########", ".#.##.#.", "........", "........"],
"computer": [".######.", "#......#", "#......#", "#......#", ".######.", "...##...", "..####..", "........"],
"egg": ["..####..", ".######.", "########", "########", "########", "########", ".######.", "..####.."],
"cube": ["..####..", ".#....##", "########", "#....#.#", "#....#.#", "#....##.", "########", "........"],
"shell": ["...##...", "..####..", ".##..##.", "###..###", "###..###", ".######.", "..####..", "........"],
"feather": ["......##", ".....###", "....###.", "...###..", "..###...", ".###....", "##......", "#......."],
"wing": ["#.......", "##......", "###.....", "####....", "#####...", "######..", "#######.", "########"],
"coin": ["..####..", ".#.##.#.", "#.####.#", "#.#..#.#", "#.####.#", ".#.##.#.", "..####..", "........"],
}

# first match wins; order = specificity
RULES = [
 (["key"], "key"), (["mask", "face"], "mask"), (["book", "journal", "diary", "lexicon", "text", "words", "story", "stories",
   "encyclop", "codex", "notebook", "letter", "poem", "comic", "chronicle", "records", "documents", "manual", "paper"], "book"),
 (["eye", "camera", "vision", "sight", "watch", "photograph", "photo", "optic", "stare", "glasses", "specs", "spectacles",
   "goggles"], "eye"),
 (["tree", "forest", "ivy", "plant", "wood", "vine", "bush", "grove", "kudzu", "weed", "fern", "garden", "moss", "seed",
   "root", "cactus", "cacti", "fruit", "tomato", "pomegranate"], "tree"),
 (["skull", "death", "dead", "corpse", "grave", "tomb", "mortal", "murder", "kill", "reaper", "bones", "bone", "skeleton"], "skull"),
 (["door", "gate", "portal", "hallway", "stair", "elevator", "entrance", "exit", "doorway", "closet", "hatch"], "door"),
 (["box", "chest", "crate", "case", "briefcase", "container", "bag", "kit", "package", "wardrobe", "cabinet", "safe"], "box"),
 (["clock", "time", "watch", "hour", "timer", "temporal", "schedule", "calendar", "snooze", "alarm", "loop"], "clock"),
 (["mirror", "reflection", "glass", "double", "doppelg", "twin", "copy", "clone"], "mirror"),
 (["doll", "toy", "puppet", "mannequin", "dummy", "teddy", "figure", "statue", "sculpture", "action figure"], "doll"),
 (["bottle", "potion", "jar", "can ", "flask", "vial", "syringe", "cup", "canteen", "beaker", "soda", "whiskey", "drink",
   "wine", "tea", "coffee", "milk", "pitcher", "tumbler", "water"], "bottle"),
 (["ant", "bug", "insect", "fly", "flies", "bee", "beetle", "cicada", "worm", "larva", "maggot", "mosquito", "moth", "wasp",
   "roach", "cockroach", "centipede", "tick", "grub", "locust", "bedbug", "caterpillar", "mite"], "bug"),
 (["spider", "arachnid", "web", "tarantula"], "spider"),
 (["fish", "shark", "whale", "carp", "eel", "squid", "octopus", "crab", "shrimp", "lobster", "marine", "aquatic", "ocean",
   "sea", "sub", "ship", "boat", "submarine", "mermaid", "tuna", "dolphin", "turtle", "fishing"], "fish"),
 (["bird", "avian", "owl", "crow", "dove", "hawk", "parrot", "eagle", "raven", "canary", "chicken", "seagull", "duck",
   "goose", "swan", "flamingo", "phoenix", "pigeon"], "bird"),
 (["cat", "feline", "kitten", "lion", "tiger", "panther", "lynx", "fox", "leopard"], "cat"),
 (["dog", "canine", "wolf", "hound", "puppy", "beast", "bear", "ursa", "horse", "pony", "deer", "cow", "pig", "sheep",
   "goat", "rabbit", "hare", "rat", "mouse", "raccoon", "monkey", "ape", "bigfoot", "sloth", "llama", "giraffe", "elephant",
   "hippo", "hog", "boar", "bat", "rodent", "squirrel", "possum", "kangaroo", "wallaby"], "dog"),
 (["hand", "finger", "glove", "arm", "touch", "fist", "palm", "grasp"], "hand"),
 (["heart", "love", "organ", "blood", "life", "vein", "pulse", "flesh", "brain", "lung", "liver", "stomach"], "heart"),
 (["house", "home", "room", "building", "apartment", "mansion", "cabin", "hotel", "hospital", "school", "church", "temple",
   "castle", "prison", "penitentiary", "restaurant", "diner", "store", "shop", "mall", "museum", "library", "office",
   "theatre", "theater", "cinema", "factory", "facility", "site", "complex", "bakery", "farm"], "house"),
 (["tower", "obelisk", "pillar", "lighthouse", "spire", "monument", "column", "tunnel"], "tower"),
 (["bone", "tooth", "teeth", "jaw", "molar", "fang"], "tooth"),
 (["fire", "flame", "burn", "burning", "ignite", "lighter", "match", "candle", "torch", "inferno", "heat", "hot", "lava",
   "magma", "ember", "smoke", "explosive", "bomb", "nuke", "nuclear"], "flame"),
 (["rain", "drop", "tear", "liquid", "fluid", "ink", "oil", "slime", "ooze", "river", "lake", "pool", "pond", "sea",
   "ocean", "fountain", "wet", "flood", "spring", "bath", "soup"], "drop"),
 (["star", "stellar", "astro", "cosmic", "galaxy", "space", "meteor", "comet", "universe", "moon", "lunar", "sun", "solar",
   "orbit", "nova"], "star"),
 (["gear", "machine", "engine", "device", "mechanical", "clockwork", "robot", "cyborg", "automaton", "tool", "contraption",
   "apparatus", "turbine", "factory", "mechanism", "motor", "drone", "droid"], "gear"),
 (["phone", "telephone", "radio", "signal", "broadcast", "intercom", "headphone", "speaker", "antenna", "transmission",
   "call", "dial", "pager", "receiver"], "phone"),
 (["tv", "television", "video", "movie", "film", "screen", "monitor", "display", "projector", "tape", "dvd", "vhs"], "tv"),
 (["ring", "bracelet", "necklace", "jewel", "gem", "crystal", "opal", "pendant", "locket", "diamond", "amulet", "bead"], "ring"),
 (["sword", "knife", "blade", "dagger", "gun", "weapon", "spear", "axe", "arrow", "bow", "scissors", "razor", "katana",
   "pistol", "rifle", "cannon", "guillotine", "nail", "needle", "pen"], "sword"),
 (["crown", "king", "queen", "emperor", "royal", "throne", "prince", "lord", "god", "angel", "divine", "deity", "saint",
   "holy", "pope", "majesty"], "crown"),
 (["flower", "rose", "bloom", "petal", "lily", "daisy", "orchid"], "flower"),
 (["snake", "serpent", "viper", "reptile", "lizard", "dragon", "cobra", "python", "worm", "jormun", "ouroboros"], "snake"),
 (["ghost", "spirit", "phantom", "shadow", "soul", "specter", "spectre", "haunt", "wraith", "poltergeist", "apparition",
   "dark", "darkness", "absence"], "ghost"),
 (["planet", "world", "earth", "globe", "sphere", "ball", "orb", "bubble"], "planet"),
 (["music", "song", "sing", "sound", "violin", "piano", "choir", "melody", "guitar", "harp", "flute", "drum", "noise",
   "voice", "whistle", "bell", "chord", "banjo", "gramophone", "record", "echo", "silence"], "note"),
 (["lock", "contract", "chain", "prison", "cage", "trap", "lockdown", "restraint", "cuff", "seal"], "lock"),
 (["pill", "drug", "medicine", "cure", "panacea", "vaccine", "antibiotic", "tablet", "virus", "plague", "infect", "disease",
   "flu", "sick", "contagi", "parasite", "pathogen", "fungus", "fungal", "mold", "cancer", "bacteria"], "pill"),
 (["cloud", "storm", "weather", "wind", "fog", "mist", "lightning", "thunder", "snow", "ice", "frost", "winter", "cold",
   "tornado", "hurricane", "blizzard"], "cloud"),
 (["mushroom", "fungus", "spore", "toadstool", "truffle", "fungi"], "mushroom"),
 (["man", "woman", "girl", "boy", "child", "children", "person", "people", "human", "baby", "guy", "lady", "gentleman",
   "mother", "father", "sister", "brother", "family", "agent", "doctor", "dr.", "mr.", "mrs", "miss", "nurse", "teacher",
   "farmer", "thief", "butler", "chef", "professor", "wizard", "witch", "monk", "priest", "soldier", "legion", "tyrant"], "human"),
 (["car", "bus", "train", "truck", "plane", "aircraft", "helicopter", "tank", "carriage", "wagon", "zeppelin", "cart",
   "locomotive", "vehicle", "tractor", "bike", "bicycle", "ship", "spacecraft", "forklift", "coaster"], "vehicle"),
 (["computer", "laptop", "program", "software", "digital", "code", "ai", "network", "online", "internet", "website",
   "server", "database", "hard drive", "floppy", "chip", "microchip", "app", "cpu", "keyboard", "typewriter", "printer"], "computer"),
 (["egg", "womb", "birth", "seed", "cocoon", "pod", "larva", "pupa", "chrysalis"], "egg"),
 (["cube", "box", "puzzle", "block", "dice", "square", "brick", "tile", "polyhedron", "rubik"], "cube"),
 (["shell", "snail", "conch", "nautilus", "scallop", "clam", "oyster", "carapace", "armor", "armour", "helmet", "shield"], "shell"),
 (["feather", "quill", "wing", "angel", "fly", "flight", "soar"], "feather"),
 (["coin", "money", "cash", "gold", "dollar", "currency", "treasure", "bank", "wealth", "credit", "dime", "penny", "penny"], "coin"),
]

# giant / tiny hints for mob scale (height in blocks relative to 1.95 vanilla humanoid)
GIANT = ["giant", "leviathan", "whale", "dragon", "titan", "colossus", "behemoth", "train", "tank", "elephant", "mountain",
         "tower", "building", "ship", "airline", "zeppelin", "jörmungandr", "bigfoot", "kaiju",
         "juggernaut", "goliath", "hulking", "mammoth", "dinosaur", "allosaurus", "sloth", "ursa"]
TINY = ["kitten", "mouse", "rat", "ant", "bug", "worm", "spider", "frog", "bee", "fly", "flies", "snail", "crab", "baby",
        "doll", "toy", "tiny", "mini", "miniature", "micro", "gnome", "cat", "hamster", "fish", "beetle", "wasp", "moth",
        "mosquito", "larva", "tick", "bird", "dove", "canary", "owl", "mite", "centipede", "puppy", "rabbit", "squirrel",
        "child", "children", "boy", "girl", "figure", "dummy", "goldfish", "bat", "kid", "teacup", "pet", "hornet", "cricket",
        "flea", "maggot", "snake", "eel"]
CREATURE = ["man", "woman", "girl", "boy", "child", "children", "person", "people", "human", "baby", "guy", "lady", "gentleman",
            "beast", "monster", "creature", "predator", "horror", "demon", "devil", "ghost", "spirit", "wraith", "phantom",
            "shadow", "dog", "cat", "wolf", "bear", "horse", "rabbit", "rat", "mouse", "bird", "owl", "crow", "fox", "snake",
            "serpent", "dragon", "spider", "insect", "bug", "ant", "bee", "fly", "worm", "fish", "shark", "whale", "crab",
            "frog", "turtle", "lizard", "reptile", "kitten", "puppy", "bigfoot", "ape", "monkey", "sloth", "llama", "giraffe",
            "elephant", "goat", "sheep", "cow", "pig", "bull", "king", "queen", "priest", "monk", "doctor", "agent",
            "butler", "farmer", "mother", "father", "sister", "brother", "family", "angel", "god", "witch", "wizard",
            "knight", "soldier", "legionnaire", "thief", "soldier", "mimic", "plague", "swarm", "ghoul", "zombie", "vampire",
            "werewolf", "were-", "wendigo", "cannibal", "gnome", "elf", "fairy", "fairies", "imp", "golem", "goblin",
            "hog", "boar", "deer", "stag", "hound", "mr.", "mrs", "miss", "dr.", "dr ", "nanny", "stalker", "hunter",
            "walker", "dweller", "eater", "feeder", "killer", "keeper", "shy guy", "sculpture", "slinky", "rake", "slender",
            "predatory", "hostile", "tulpa", "specter", "poltergeist", "revenant", "rider", "weaver", "able", "cain",
            "lilith", "daniel", "timmy", "lucky", "benny", "skip", "lucas", "vector", "bes", "iris", "tyler"]
PLACE = ["room", "house", "home", "building", "apartment", "mansion", "cabin", "hotel", "hospital", "school", "church",
         "temple", "castle", "prison", "penitentiary", "restaurant", "diner", "store", "shop", "mall", "museum", "library",
         "office", "theatre", "theater", "cinema", "factory", "facility", "site", "complex", "bakery", "farm", "tunnel",
         "hallway", "stairwell", "staircase", "elevator", "door", "gate", "portal", "cave", "cavern", "forest", "city",
         "town", "village", "island", "desert", "lake", "pool", "sea", "sand", "field", "garden", "park", "playground",
         "carnival", "fair", "station", "garage", "bus", "train", "bridge", "tower", "tree", "mountain", "labyrinth",
         "maze", "kingdom", "world", "dimension", "box", "machine", "booth", "fountain", "well", "wall", "floor", "ceiling",
         "attic", "basement", "cellar", "mine", "pit", "hole", "crater", "swamp", "ship", "airline", "plane"]


import re


def _tokens(title):
    return re.findall(r"[a-z0-9][a-z0-9'\-\.]*", title.lower().replace("’", "'"))


def _hit(k, toks, text):
    k = k.strip()
    if " " in k:
        return k in text
    for t in toks:
        t = t.rstrip(".")
        if t == k or t == k + "s" or t == k + "es" or (len(k) >= 5 and t.startswith(k)):
            return True
    return False


def icon_for(n, title):
    toks, text = _tokens(title), title.lower()
    for kws, icon in RULES:
        if any(_hit(k, toks, text) for k in kws):
            return icon
    return None


def glyph(n):
    """Unique symmetric 8x8 glyph, seeded by SCP number (for titles with no keyword)."""
    r = random.Random(n * 1315423911 & 0xFFFFFFFF)
    rows = []
    for _ in range(8):
        half = [r.random() < 0.52 for _ in range(4)]
        rows.append("".join("#" if b else "." for b in half + half[::-1]))
    return rows


def pixels(n, title):
    name = icon_for(n, title)
    rows = ICONS[name] if name else glyph(n)
    return name or "glyph", rows


def form_hint(title):
    toks, text = _tokens(title), title.lower()
    if any(_hit(k, toks, text) for k in CREATURE):
        return "entity"
    if any(_hit(k, toks, text) for k in PLACE):
        return "block"
    return "item"


def scale_hint(title, tags=None):
    """Estimated relative size when the article states none: tags first (wiki), then title words."""
    t = set(tags or [])
    if t & {"insect", "invertebrate", "swarm", "arachnid"}:
        return 0.3, "estimated"
    if t & {"bird", "rodent", "fish", "amphibian"}:
        return 0.45, "estimated"
    if "child" in t:
        return 0.7, "estimated"
    if t & {"humanoid"}:
        return 1.0, "estimated"
    toks, text = _tokens(title), title.lower()
    if any(_hit(k, toks, text) for k in GIANT):
        return 2.2, "estimated"
    if any(_hit(k, toks, text) for k in TINY):
        return 0.45, "estimated"
    return 1.0, "estimated" if t else "default"
