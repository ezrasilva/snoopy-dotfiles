#!/usr/bin/env bash
# Troca o tema Snoopy no illogical-impulse (usa o switchwall.sh do shell: ele gera
# as cores Material You do wallpaper e aplica em shell, GTK, Qt, terminal e VSCode).
# Uso: snoopy-theme.sh day | night | toggle
set -e
SWITCHWALL="$HOME/.config/quickshell/ii/scripts/colors/switchwall.sh"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/snoopy-theme"
PICS="${SNOOPY_WALLPAPER_DIR:-$HOME/Pictures}"

mode="${1:-toggle}"
if [ "$mode" = toggle ]; then
  [ "$(cat "$STATE" 2>/dev/null)" = day ] && mode=night || mode=day
fi

case "$mode" in
  day)   img="$PICS/snoopy-day.png";   scheme=light ;;
  night) img="$PICS/snoopy-night.png"; scheme=dark  ;;
  *) echo "uso: $0 day|night|toggle" >&2; exit 1 ;;
esac
[ -f "$img" ] || { echo "faltando: $img (veja o README)" >&2; exit 1; }
[ -x "$SWITCHWALL" ] || { echo "switchwall.sh não encontrado em $SWITCHWALL" >&2; exit 1; }

mkdir -p "$(dirname "$STATE")"; echo "$mode" > "$STATE"
"$SWITCHWALL" --image "$img" --mode "$scheme" --type scheme-content
command -v notify-send >/dev/null && notify-send "Snoopy" "Tema: $mode"
