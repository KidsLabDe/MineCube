# MineCube – Minecraft NeoPixel Würfel

Ein LED-Würfel aus 5 NeoPixel 8×8 Panels, der Minecraft-Blocktexturen anzeigt und alle 10 Sekunden wechselt.

## Hardware

- **MCU:** S2 Mini (ESP32-S2) mit CircuitPython
- **LEDs:** 5 × WS2812B 8×8 NeoPixel Matrix (320 LEDs)
- **Datenpin:** GPIO16
- **Verkettung:** Seite 1 → Seite 2 → Seite 3 → Seite 4 → Deckel

## Setup

### 1. CircuitPython & Bibliotheken

CircuitPython auf den S2 Mini flashen, dann:

```bash
./install.sh
```

### 2. Texturen generieren (optional)

Die `textures.py` ist bereits fertig generiert. Falls du sie aus einem eigenen Texture Pack neu generieren willst:

```bash
uv run convert_textures.py
```

### 3. Auf den S2 Mini übertragen

```bash
./deploy.sh
```

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `code.py` | Hauptprogramm (läuft auf dem S2 Mini) |
| `textures.py` | 20 Minecraft-Blocktexturen als 8×8 RGB-Arrays |
| `convert_textures.py` | Konvertiert Texture Pack PNGs → `textures.py` |
| `boot.py` | Deaktiviert USB-Drive für schnelleren Boot |
| `install.sh` | Installiert CircuitPython-Bibliotheken |
| `deploy.sh` | Kopiert Dateien auf CIRCUITPY |

## Blöcke

Grass Block, Dirt, Stone, Diamond Ore, Oak Log, Cobblestone, Gold Ore, Iron Ore, Emerald Ore, Redstone Ore, Lapis Ore, Melon, Bookshelf, Obsidian, Glowstone, TNT, Pumpkin, Crafting Table, Furnace, Creeper Head

Blöcke mit verschiedenen Seiten (Pumpkin, Furnace, Crafting Table, Creeper Head) zeigen die korrekten Texturen pro Würfelseite.

## Gehäuse

STL-Dateien für den 3D-Druck folgen.

## Lizenz

MIT
