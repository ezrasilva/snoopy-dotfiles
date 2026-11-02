#!/bin/bash
# Uso: theme-switcher.sh <tema-wofi-atual> [args extras do wofi]
# Escolhe Snoopy Day / Snoopy Night e troca o `source` na 1ª linha do hyprland.conf.
conf=~/.config/hypr/hyprland.conf
selected=$(printf 'Snoopy Day\nSnoopy Night\n' | wofi --dmenu $2 --style ~/.config/wofi/themes/$1.css --hide-scroll --cache-file /dev/null)

case $selected in
  "Snoopy Day")   theme=snoopy-day ;;
  "Snoopy Night") theme=snoopy-night ;;
  *) exit 0 ;;
esac
notify-send "Snoopy" "$selected"
sed -i "1s#.*#source = ~/.config/hypr/themes/$theme/$theme.conf#" "$conf"
hyprctl reload
