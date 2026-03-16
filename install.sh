#!/bin/bash
# Installiert circup via uv und die neopixel-Bibliothek fuer CircuitPython

echo "Installiere circup..."
uv tool install circup

echo "Installiere neopixel-Bibliothek..."
circup install neopixel

echo "Fertig!"
