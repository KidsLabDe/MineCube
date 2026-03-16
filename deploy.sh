#!/bin/bash
# Kopiert die Projektdateien auf das CIRCUITPY-Laufwerk

CIRCUITPY="/Volumes/CIRCUITPY"

if [ ! -d "$CIRCUITPY" ]; then
    echo "Fehler: CIRCUITPY nicht gefunden. Ist der S2 Mini angeschlossen?"
    exit 1
fi

echo "Kopiere Dateien nach $CIRCUITPY..."
cp code.py "$CIRCUITPY/"
cp textures.py "$CIRCUITPY/"

echo "Deploy abgeschlossen!"
