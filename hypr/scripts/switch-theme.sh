#!/bin/sh
# Aplica um tema Snoopy: wallpaper, waybar, kitty e GTK.
# Uso: switch-theme.sh snoopy-day|snoopy-night
# Não apaga nada fora de ~/.config/{waybar,kitty}; partes opcionais só rodam se o app existir.
T="$1"
# o Hyprland pode executar este script mais de uma vez por reload: serializa
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/snoopy-switch-theme.lock"
flock 9
stop() { pkill -x "$1" 2>/dev/null; for _ in 1 2 3 4 5 6 7 8 9 10; do pgrep -x "$1" >/dev/null || return 0; sleep 0.2; done; pkill -9 -x "$1" 2>/dev/null; }
J="$HOME/.config/hypr/themes/$T/$T.json"
[ -f "$J" ] || { echo "tema inválido: $T" >&2; exit 1; }
get() { jq -r "$1" "$J"; }

# wallpaper
stop hyprpaper; hyprpaper -c "$HOME/.config/hypr/hyprpaper/$T.conf" >/dev/null 2>&1 9>&- &

# waybar
stop waybar
waybar --config "$HOME/.config/waybar/$T/config" --style "$HOME/.config/waybar/$T/style.css" >/dev/null 2>&1 9>&- &

# kitty (primeira linha é o include da paleta)
if [ -f "$HOME/.config/kitty/kitty.conf" ]; then
  sed -i "1s#.*#include colors/$T.conf#" "$HOME/.config/kitty/kitty.conf"
  pkill -USR1 kitty
fi

# dunst (notificações e OSD de volume/brilho)
stop dunst; dunst -conf "$HOME/.config/dunst/$T.dunstrc" >/dev/null 2>&1 9>&- &

# hyprlock (1ª linha importa as cores/wallpaper do tema)
[ -f "$HOME/.config/hypr/hyprlock.conf" ] && sed -i "1s#.*#source = ~/.config/hypr/colors/$T.conf#" "$HOME/.config/hypr/hyprlock.conf"

# GTK / ícones / fonte (opcional)
if command -v gsettings >/dev/null 2>&1; then
  GTK=$(get .gtkTheme); ICON=$(get .iconTheme); FONT=$(get .font)
  gsettings set org.gnome.desktop.interface color-scheme "$(get .colorScheme)"
  gsettings set org.gnome.desktop.interface gtk-theme "$GTK"
  gsettings set org.gnome.desktop.interface icon-theme "$ICON"
  gsettings set org.gnome.desktop.interface font-name "$FONT 11"
fi
