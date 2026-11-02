#!/bin/sh
# Congela a tela e captura uma área. Uso: freeze-screenshot.sh [0=salvar | 1=copiar]
# Requer: hyprpicker, grimblast, wl-clipboard
MODE="${1:-1}"
mkdir -p "$HOME/Pictures/screenshots"
hyprpicker -r -z & picker_proc=$!
sleep 0.2
if [ "$MODE" -eq 0 ]; then
    grimblast save area "$HOME/Pictures/screenshots/$(date +'%s_snoopy.png')"
else
    grimblast save area - | wl-copy
fi
kill $picker_proc
