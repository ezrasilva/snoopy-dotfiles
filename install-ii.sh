#!/bin/bash
# Instala o Snoopy POR CIMA do illogical-impulse, sem substituir nada seu.
# - copia ii/scripts/snoopy-theme.sh e ii/hypr/custom/snoopy.lua para ~/.config/hypr/custom/
# - acrescenta 1 linha em custom/general.lua (com backup .bak-<data>), se ainda não houver
# Uso: ./install-ii.sh [--dry-run]    Desfazer: ./install-ii.sh --uninstall
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
C="$HOME/.config/hypr/custom"
G="$C/general.lua"
LINE='require("custom.snoopy") -- snoopy-dotfiles'
DRY=0; [ "$1" = "--dry-run" ] && DRY=1
run() { if [ $DRY = 1 ]; then echo "[dry] $*"; else "$@"; fi; }

[ -d "$C" ] || { echo "Não achei $C — o illogical-impulse está instalado?" >&2; exit 1; }

if [ "$1" = "--uninstall" ]; then
  sed -i '/snoopy-dotfiles$/d' "$G"
  rm -f "$C/snoopy.lua" "$C/scripts/snoopy-theme.sh"
  echo "Removido. Rode 'hyprctl reload'."; exit 0
fi

run mkdir -p "$C/scripts"
run cp "$REPO/ii/hypr/custom/snoopy.lua" "$C/snoopy.lua"
run cp "$REPO/ii/scripts/snoopy-theme.sh" "$C/scripts/snoopy-theme.sh"
run chmod +x "$C/scripts/snoopy-theme.sh"
if ! grep -qF "snoopy-dotfiles" "$G" 2>/dev/null; then
  run cp "$G" "$G.bak-$(date +%Y%m%d-%H%M%S)"
  if [ $DRY = 1 ]; then echo "[dry] append em $G: $LINE"; else printf '\n%s\n' "$LINE" >> "$G"; fi
fi
echo "Pronto. 'hyprctl reload' e depois: $C/scripts/snoopy-theme.sh day   (ou SUPER+ALT+T)"
