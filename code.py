import time
import random
import board
import neopixel
from textures import TEXTURES

# NeoPixel Setup: 320 LEDs (5 Panels x 64), Datenpin GPIO16
pixels = neopixel.NeoPixel(board.IO16, 320, brightness=0.1, auto_write=False)


def set_pixel(panel, x, y, color):
    """Setzt ein Pixel auf einem Panel. Serpentinen-Layout."""
    if y % 2 == 0:
        idx = panel * 64 + y * 8 + x
    else:
        idx = panel * 64 + y * 8 + (7 - x)
    pixels[idx] = color


def draw_texture(panel, texture):
    """Zeichnet eine 8x8 Textur auf ein Panel."""
    for y in range(8):
        for x in range(8):
            set_pixel(panel, x, y, texture[y][x])


def show_block(block):
    """Zeigt einen Block auf dem Wuerfel: Seiten 0-3 = sides, Seite 4 = top."""
    for panel in range(4):
        draw_texture(panel, block["sides"][panel])
    draw_texture(4, block["top"])
    pixels.show()


# Hauptloop
last_index = -1
while True:
    index = random.randint(0, len(TEXTURES) - 1)
    while index == last_index:
        index = random.randint(0, len(TEXTURES) - 1)
    last_index = index

    block = TEXTURES[index]
    print("Block:", block["name"])
    show_block(block)
    time.sleep(10)
