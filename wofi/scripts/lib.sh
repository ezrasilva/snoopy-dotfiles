#!/bin/bash
# Funções comuns dos menus do wofi (Wi-Fi, Bluetooth, telas).
current_theme() { grep -o 'snoopy-[a-z]*' "$HOME/.config/hypr/hyprland.lua" 2>/dev/null | head -1; }

# menu <prompt> [altura] [args extras do wofi]  — lê as opções do stdin, imprime a escolhida
menu() {
  local prompt="$1" height="${2:-360}"; shift 2 2>/dev/null || shift $#
  wofi --dmenu -i --cache-file /dev/null --hide-scroll \
    --style "$HOME/.config/wofi/themes/$(current_theme || echo snoopy-day).css" \
    --prompt "$prompt" --width 420 --height "$height" \
    --location top_right --xoffset -12 --yoffset 56 "$@"
}
note() { notify-send -a Snoopy "$1" "$2"; }
