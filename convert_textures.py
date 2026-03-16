#!/usr/bin/env python3
"""
Konvertiert 8x8 Minecraft-Texturen aus einem Texture Pack
zu RGB-Arrays fuer textures.py.

Bloecke mit verschiedenen Seiten bekommen 4 individuelle Seitentexturen.
Format: {"name", "top", "sides": [front, right, back, left]}

Usage: uv run convert_textures.py
"""
# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow"]
# ///

from pathlib import Path
from PIL import Image

PACK_PATH = Path.home() / "Downloads/assets/minecraft/textures"
MAX_BRIGHTNESS = 40

# Biome-Tint fuer Gras (Plains-Biome)
GRASS_TINT = (124, 189, 107)

# Einfache Bloecke: (Name, Side, Top, Tint-Side, Tint-Top)
# Side wird fuer alle 4 Seiten verwendet
SIMPLE_BLOCKS = [
    ("Grass Block",    "blocks/grass_side.png",    "blocks/grass_top.png",    None,       GRASS_TINT),
    ("Dirt",           "blocks/dirt.png",           None,                      None,       None),
    ("Stone",          "blocks/stone.png",          None,                      None,       None),
    ("Diamond Ore",    "blocks/diamond_ore.png",    None,                      None,       None),
    ("Oak Log",        "blocks/log_oak.png",        "blocks/log_oak_top.png",  None,       None),
    ("Cobblestone",    "blocks/cobblestone.png",    None,                      None,       None),
    ("Gold Ore",       "blocks/gold_ore.png",       None,                      None,       None),
    ("Iron Ore",       "blocks/iron_ore.png",       None,                      None,       None),
    ("Emerald Ore",    "blocks/emerald_ore.png",    None,                      None,       None),
    ("Redstone Ore",   "blocks/redstone_ore.png",   None,                      None,       None),
    ("Lapis Ore",      "blocks/lapis_ore.png",      None,                      None,       None),
    ("Melon",          "blocks/melon_side.png",     "blocks/melon_top.png",    None,       None),
    ("Bookshelf",      "blocks/bookshelf.png",      "blocks/planks_oak.png",   None,       None),
    ("Obsidian",       "blocks/obsidian.png",       None,                      None,       None),
    ("Glowstone",      "blocks/glowstone.png",      None,                      None,       None),
]

# Bloecke mit verschiedenen Seiten: (Name, Top, Front, Right, Back, Left)
MULTI_SIDE_BLOCKS = [
    ("TNT",            "blocks/tnt_top.png",
     "blocks/tnt_side.png", "blocks/tnt_side.png",
     "blocks/tnt_side.png", "blocks/tnt_side.png"),
    ("Pumpkin",        "blocks/pumpkin_top.png",
     "blocks/pumpkin_face_off.png", "blocks/pumpkin_side.png",
     "blocks/pumpkin_side.png",     "blocks/pumpkin_side.png"),
    ("Crafting Table", "blocks/crafting_table_top.png",
     "blocks/crafting_table_front.png", "blocks/crafting_table_side.png",
     "blocks/crafting_table_front.png", "blocks/crafting_table_side.png"),
    ("Furnace",        "blocks/furnace_top.png",
     "blocks/furnace_front_on.png", "blocks/furnace_side.png",
     "blocks/furnace_side.png",     "blocks/furnace_side.png"),
]

# Creeper-Kopf: Crop-Bereiche aus der 32x16 Entity-Textur
CREEPER_SRC = "entity/creeper/creeper.png"
CREEPER_CROPS = {
    "top":   (8, 0, 16, 8),
    "front": (8, 8, 16, 16),
    "right": (0, 8, 8, 16),
    "back":  (24, 8, 32, 16),
    "left":  (16, 8, 24, 16),
}


def load_png(rel_path, crop_box=None):
    """Liest eine PNG-Textur. Optional mit Crop."""
    path = PACK_PATH / rel_path
    img = Image.open(path).convert("RGBA")
    if crop_box:
        img = img.crop(crop_box)
    bg = Image.new("RGB", img.size, (0, 0, 0))
    bg.paste(img, mask=img.split()[3])
    return bg


def apply_tint(img, tint):
    """Multipliziert Bildfarben mit einem Tint (fuer Gras etc.)."""
    if tint is None:
        return img
    tr, tg, tb = tint
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            px[x, y] = (r * tr // 255, g * tg // 255, b * tb // 255)
    return img


def dim_color(r, g, b):
    """Dimmt eine Farbe so, dass kein Kanal MAX_BRIGHTNESS ueberschreitet."""
    max_val = max(r, g, b, 1)
    if max_val > MAX_BRIGHTNESS:
        scale = MAX_BRIGHTNESS / max_val
        r = int(r * scale)
        g = int(g * scale)
        b = int(b * scale)
    return (r, g, b)


def img_to_array(img):
    """Konvertiert ein PIL-Image zu einem 8x8 RGB-Array."""
    if img.size != (8, 8):
        img = img.resize((8, 8), Image.LANCZOS)
    grid = []
    for y in range(8):
        row = []
        for x in range(8):
            r, g, b = img.getpixel((x, y))[:3]
            row.append(dim_color(r, g, b))
        grid.append(row)
    return grid


def make_grass_side(tint):
    """Grass-Seite mit Overlay + Tint."""
    side_img = load_png("blocks/grass_side.png")
    overlay_path = PACK_PATH / "blocks/grass_side_overlay.png"
    if overlay_path.exists():
        overlay_rgba = Image.open(overlay_path).convert("RGBA")
        overlay_rgb = load_png("blocks/grass_side_overlay.png")
        overlay_rgb = apply_tint(overlay_rgb, tint)
        side_img.paste(overlay_rgb, (0, 0), overlay_rgba.split()[3])
    return side_img


def format_row(row):
    pixels = ", ".join(f"({r:>2}, {g:>2}, {b:>2})" for r, g, b in row)
    return f"            [{pixels}]"


def format_texture(grid):
    rows = ",\n".join(format_row(row) for row in grid)
    return f"[\n{rows},\n        ]"


def main():
    if not PACK_PATH.exists():
        print(f"Fehler: Texture Pack nicht gefunden: {PACK_PATH}")
        return

    entries = []  # (name, top_grid, [front, right, back, left])

    # Einfache Bloecke
    for name, side_rel, top_rel, tint_side, tint_top in SIMPLE_BLOCKS:
        if not (PACK_PATH / side_rel).exists():
            print(f"WARNUNG: {side_rel} nicht gefunden, ueberspringe {name}")
            continue

        if name == "Grass Block":
            side_img = make_grass_side(GRASS_TINT)
        else:
            side_img = load_png(side_rel)
            side_img = apply_tint(side_img, tint_side)

        side_grid = img_to_array(side_img)

        if top_rel and (PACK_PATH / top_rel).exists():
            top_img = load_png(top_rel)
            top_img = apply_tint(top_img, tint_top)
            top_grid = img_to_array(top_img)
        else:
            top_grid = side_grid

        entries.append((name, top_grid, [side_grid, side_grid, side_grid, side_grid]))
        print(f"OK: {name}")

    # Bloecke mit verschiedenen Seiten
    for name, top_rel, front_rel, right_rel, back_rel, left_rel in MULTI_SIDE_BLOCKS:
        if not (PACK_PATH / front_rel).exists():
            print(f"WARNUNG: {front_rel} nicht gefunden, ueberspringe {name}")
            continue

        top_grid = img_to_array(load_png(top_rel))
        sides = []
        for rel in [front_rel, right_rel, back_rel, left_rel]:
            sides.append(img_to_array(load_png(rel)))

        entries.append((name, top_grid, sides))
        print(f"OK: {name} (multi-side)")

    # Creeper-Kopf
    creeper_path = PACK_PATH / CREEPER_SRC
    if creeper_path.exists():
        top_grid = img_to_array(load_png(CREEPER_SRC, CREEPER_CROPS["top"]))
        sides = [
            img_to_array(load_png(CREEPER_SRC, CREEPER_CROPS["front"])),
            img_to_array(load_png(CREEPER_SRC, CREEPER_CROPS["right"])),
            img_to_array(load_png(CREEPER_SRC, CREEPER_CROPS["back"])),
            img_to_array(load_png(CREEPER_SRC, CREEPER_CROPS["left"])),
        ]
        entries.append(("Creeper Head", top_grid, sides))
        print("OK: Creeper Head (multi-side)")
    else:
        print("WARNUNG: Creeper-Textur nicht gefunden")

    # textures.py generieren
    lines = [
        "# MineCube Texturen - generiert aus 8x8 Texture Pack",
        "# 8x8 RGB-Arrays, gedimmt (max ~40 pro Kanal)",
        "# Format: sides = [front, right, back, left]",
        "",
        "TEXTURES = [",
    ]

    for name, top_grid, sides in entries:
        lines.append("    {")
        lines.append(f'        "name": "{name}",')
        lines.append(f'        "top": {format_texture(top_grid)},')
        lines.append(f'        "sides": [')
        for side_grid in sides:
            lines.append(f'            {format_texture(side_grid)},')
        lines.append(f'        ],')
        lines.append("    },")

    lines.append("]")
    lines.append("")

    output = Path(__file__).parent / "textures.py"
    output.write_text("\n".join(lines))
    print(f"\ntextures.py geschrieben mit {len(entries)} Bloecken!")


if __name__ == "__main__":
    main()
