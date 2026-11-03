#!/bin/bash
# Menu de telas: estender, espelhar, só uma tela. (Usa `hyprctl eval`, API Lua do Hyprland 0.56+)
. "$(dirname "$0")/lib.sh"
mapfile -t MONS < <(hyprctl monitors all -j | jq -r '.[].name')
INT=$(printf '%s\n' "${MONS[@]}" | grep -m1 '^eDP' )
EXT=$(printf '%s\n' "${MONS[@]}" | grep -vm1 '^eDP' )
[ "${#MONS[@]}" -lt 2 ] && { note "Telas" "Só há uma tela conectada"; exit 0; }

mon() { # mon <nome> <posição|disable> [mirror-de]   (mirror="" desfaz espelhamento anterior)
  local m=""; [ -n "$3" ] && m="$3"
  if [ "$2" = disable ]; then hyprctl eval "hl.monitor({ output = \"$1\", disabled = true })" >/dev/null
  else hyprctl eval "hl.monitor({ output = \"$1\", mode = \"preferred\", position = \"$2\", scale = 1, mirror = \"$m\" })" >/dev/null; fi
}
sel=$(printf '󰍹  Estender (notebook + externa)\n󰍺  Espelhar\n󰌢  Só o notebook\n󰍹  Só a tela externa\n' | menu "Telas" 240) || exit 0
case "$sel" in
  *Estender*) mon "$INT" 0x0; mon "$EXT" auto-right ;;
  *Espelhar*) mon "$INT" 0x0; mon "$EXT" 0x0 "$INT" ;;
  *"Só o notebook"*) mon "$INT" 0x0; mon "$EXT" disable ;;
  *externa*) mon "$EXT" 0x0; mon "$INT" disable ;;
  *) exit 0 ;;
esac
note "Telas" "${sel#*  }"
