#!/bin/bash
# Instala via symlink em ~/.config, com backup do que já existir.
# Uso: ./install.sh [--dry-run]
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
CFG="$HOME/.config"
STAMP=$(date +%Y%m%d-%H%M%S)
DRY=0; [ "$1" = "--dry-run" ] && DRY=1
run() { if [ $DRY = 1 ]; then echo "[dry] $*"; else "$@"; fi; }

for d in hypr waybar wofi kitty dunst zsh fastfetch; do
  dst="$CFG/$d"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$REPO/$d" ]; then echo "ok: $d"; continue; fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    echo "backup: $dst -> $dst.bak-$STAMP"; run mv "$dst" "$dst.bak-$STAMP"
  fi
  echo "link: $dst -> $REPO/$d"; run ln -s "$REPO/$d" "$dst"
done
# zsh: 1 linha no ~/.zshrc (depois do p10k), com backup
ZRC="$HOME/.zshrc"; ZLINE='[[ -f ~/.config/zsh/snoopy.zsh ]] && source ~/.config/zsh/snoopy.zsh # snoopy-dotfiles'
if [ -f "$ZRC" ] && ! grep -qF "snoopy-dotfiles" "$ZRC"; then
  run cp "$ZRC" "$ZRC.bak-$STAMP"
  if [ $DRY = 1 ]; then echo "[dry] append em $ZRC"; else
    if grep -q 'p10k.zsh' "$ZRC"; then sed -i "/p10k.zsh/a $ZLINE" "$ZRC"; else printf '\n%s\n' "$ZLINE" >> "$ZRC"; fi
  fi
fi
echo "Pronto. Reinicie o Hyprland (ou 'hyprctl reload')."
