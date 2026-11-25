# SCP Foundation (Fabric, Minecraft Java 26.3)

SCP-0000 through SCP-2000 (2001 entries) plus Foundation facility blocks, keycards and a tranquilizer gun.

## Build (you do NOT need to install Gradle)
You only need **JDK 25** (https://adoptium.net, pick Temurin 25). The project bundles Gradle's launcher.

    ./gradlew build          # Windows: gradlew.bat build

The finished mod is `build/libs/scp-foundation-1.0.0.jar` (ignore the `-sources` jar). First build downloads Minecraft and
Gradle, so it needs internet and a few minutes. To test: `./gradlew runClient`.

**No local setup at all:** put this folder in a GitHub repo. The included `.github/workflows/build.yml` builds the jar on every push;
download it from the Actions tab (Artifacts).

## Installing the mod (for players)
1. Install Fabric Loader 0.20.1+ for Minecraft 26.3 (https://fabricmc.net/use).
2. Put **Fabric API** (0.166.2+26.3 or newer for 26.3) and `scp-foundation-1.0.0.jar` in your `mods` folder.
3. Launch the Fabric profile.

Built against: Minecraft 26.3, Fabric Loader 0.20.1, Fabric API 0.166.2+26.3, Loom 1.19, Gradle 9.8.2 (versions from the official
Fabric example mod). Not yet compiled by the author: if a Mojang name changed, the compiler points at the exact line.

## How the SCPs work
Each SCP has one entry in `scp_registry.json` (generated). Its form decides what it is in game:

| Form | In game | What it does |
|---|---|---|
| item (~824) | item | right-click applies its effects |
| entity (~699) | spawn item, right-click a block | one shared mob type, stats from class, behaviors from its entry |
| block (~478) | placeable block | stepping on or right-clicking it applies its effects |

Behaviors are mixed from libraries (20 entity, 12 item, 7 block). Class sets health and damage
(Safe 20/2, Euclid 40/6, Keter 100/12, Thaumiel 80/4, Apollyon 250/20).

**Data source:** `tools/scp_wiki_data.json` was built from the public dataset https://github.com/scp-data/scp-api
(SCP wiki articles and tags, CC BY-SA 3.0) with `tools/extract_from_scp_data.py`. From it, for 1980 of the 2001 numbers:
- **Object class** is the wiki's own class tag (Safe/Euclid/Keter/Thaumiel). It overrides anything typed by hand.
- **Form** (mob / block / item) is decided from wiki tags (humanoid, animal, hostile -> mob; location, building, portal -> block; else item).
- **Behaviours** are inferred from tags (e.g. `observational` -> freezes when watched, `fire` -> fire aura, `teleportation` -> blink).
- **Mob size** uses the height stated in the article when it has one (about 210 mobs); the rest are estimated from tags/title and
  marked `estimated` in `/scp info`. Most articles state no height, so this cannot be fully real.
- 21 numbers have no article in the dataset (deleted/reserved, e.g. 029, 050, 161); they use generated values.
- 47 SCPs have hand-tuned behaviours in `tools/scp_overrides.psv` (173, 096, 049, 106, 682, ...). Their class still comes from the wiki.
Titles for all 2000 SCPs are in `tools/names_series1.txt` / `names_series2.txt`.

## Survival
Everything is also craftable (and in the Creative tabs). Every SCP has a unique shapeless recipe:
one tier ingredient (Safe iron ingot, Euclid gold ingot, Keter diamond, Thaumiel emerald, Apollyon nether star)
plus 3 vanilla items. Look one up in game with `/scp recipe <n>`.
Facility blocks, keycards (each level upgrades the previous), doors and the tranquilizer gun have their own recipes.

## Replace stand-ins with canon data
Edit `tools/scp_overrides.psv` (format: `number|name|class|form|BEHAVIOR;BEHAVIOR`), then:

    python3 tools/generate_resources.py     # needs Pillow

It regenerates the registry, lang, models, blockstates, loot tables and 16x16 textures.

## Other content
- Facility blocks: Containment Wall, Reinforced Floor, Hazard Stripe, Containment Lamp, Foundation Logo
- Level 0-5 Keycards and Level 0-5 Keycard Doors (right-click with a card of equal or higher level; opens 3 s)
- Tranquilizer Gun: freezes SCP entities for 15 s, slows and weakens others
- Commands (op): `/scp give <0-2000>`, `/scp info <0-2000>`, `/scp recipe <0-2000>`, `/breach [count]`
- Five creative tabs: Foundation Gear, Safe, Euclid, Keter, Thaumiel/Apollyon

## Textures and sizes (every SCP)
- **Item/block tiles (all 2001):** class-coloured tile with an 8x8 icon picked from the SCP's title (key, mask, book, eye, fish,
  flame, door, ... ~50 original icons) plus the number. Titles with no keyword (about half) get a unique symmetric glyph, so no two tiles match.
- **Mob skins (all entity SCPs):** one unique 64x64 skin each (colour, pattern, eyes, mouth, clothing); the mod picks it by SCP number.
- **Mob size:** `Attributes.SCALE`. Real heights are used when `tools/scp_wiki_data.json` exists; otherwise sizes are
  **estimated from the title** (tiny things x0.45, giants x2.2, everything else x1.0). `/scp info <n>` shows `estimated` or `wiki`.
- **Your own art:** drop `tools/custom_art/scp_0173.png` (16x16 tile) or `scp_0173_skin.png` (64x64 mob skin), re-run the generator.
- **Refresh data:** `git clone --depth 1 https://github.com/scp-data/scp-api`, run `python3 tools/extract_from_scp_data.py <clone>`, then the generator.

## Known limits
- All SCP mobs use the vanilla zombie model (only skin and size differ).
- Icons are generic pictograms, not the SCPs' official art.
- No custom sounds, structures or dimension.
- Entity SCPs spawn as items-to-mobs; they do not spawn naturally.

SCP Foundation content is licensed CC BY-SA 3.0. Credit: https://scp-wiki.wikidot.com
