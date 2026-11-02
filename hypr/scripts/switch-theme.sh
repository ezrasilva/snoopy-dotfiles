#!/bin/sh
# Aplica um tema Snoopy: wallpaper, waybar, kitty e GTK.
# Uso: switch-theme.sh snoopy-day|snoopy-night
# Não apaga nada fora de ~/.config/{waybar,kitty}; partes opcionais só rodam se o app existir.
T="$1"
J="$HOME/.config/hypr/themes/$T/$T.json"
[ -f "$J" ] || { echo "tema inválido: $T" >&2; exit 1; }
get() { jq -r "$1" "$J"; }

# wallpaper
pkill hyprpaper; hyprpaper -c "$HOME/.config/hypr/hyprpaper/$T.conf" >/dev/null 2>&1 &

# waybar
pkill waybar
waybar --config "$HOME/.config/waybar/$T/config" --style "$HOME/.config/waybar/$T/style.css" >/dev/null 2>&1 &

# kitty (primeira linha é o include da paleta)
if [ -f "$HOME/.config/kitty/kitty.conf" ]; then
  sed -i "1s#.*#include colors/$T.conf#" "$HOME/.config/kitty/kitty.conf"
  pkill -USR1 kitty
fi

# GTK / ícones / fonte (opcional)
if command -v gsettings >/dev/null 2>&1; then
  GTK=$(get .gtkTheme); ICON=$(get .iconTheme); FONT=$(get .font)
  gsettings set org.gnome.desktop.interface color-scheme "$(get .colorScheme)"
  gsettings set org.gnome.desktop.interface gtk-theme "$GTK"
  gsettings set org.gnome.desktop.interface icon-theme "$ICON"
  gsettings set org.gnome.desktop.interface font-name "$FONT 11"
fi
