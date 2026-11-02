#!/bin/bash
# Instala via symlink em ~/.config, com backup do que já existir.
# Uso: ./install.sh [--dry-run]
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
CFG="$HOME/.config"
STAMP=$(date +%Y%m%d-%H%M%S)
DRY=0; [ "$1" = "--dry-run" ] && DRY=1
run() { if [ $DRY = 1 ]; then echo "[dry] $*"; else "$@"; fi; }

for d in hypr waybar wofi kitty; do
  dst="$CFG/$d"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$REPO/$d" ]; then echo "ok: $d"; continue; fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    echo "backup: $dst -> $dst.bak-$STAMP"; run mv "$dst" "$dst.bak-$STAMP"
  fi
  echo "link: $dst -> $REPO/$d"; run ln -s "$REPO/$d" "$dst"
done
echo "Pronto. Reinicie o Hyprland (ou 'hyprctl reload')."
