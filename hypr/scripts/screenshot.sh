#!/bin/sh
# Uso: screenshot.sh area|screen  — salva em ~/Pictures/screenshots e copia pro clipboard
DIR="$HOME/Pictures/screenshots"; mkdir -p "$DIR"
F="$DIR/$(date +'%Y-%m-%d_%H-%M-%S')_snoopy.png"
case "$1" in
  screen) grim "$F" || exit 1 ;;
  *) pgrep -x slurp >/dev/null && exit 0
     G=$(slurp -d -b '#1c213699' -c '#ef5b4f' -s '#00000000' -w 3) || exit 0
     grim -g "$G" "$F" || exit 1 ;;
esac
wl-copy < "$F"
notify-send -i "$F" "Print salvo" "$(basename "$F") (copiado)"
