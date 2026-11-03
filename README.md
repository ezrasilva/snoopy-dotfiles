# snoopy-dotfiles 🐶

Rice de Hyprland com tema **Peanuts / Snoopy**, em duas variantes:

- **Day**: nuvens creme, céu turquesa, grama verde e coleira vermelha do Snoopy.
- **Night**: céu azul-marinho do Barão Vermelho, lua, texto creme.

Baseado na estrutura de [MathisP75/summer-day-and-night](https://github.com/MathisP75/summer-day-and-night)
(Hyprland + Waybar + Wofi + Kitty). Cores, wallpapers e scripts foram refeitos; os scripts do original que
mexiam em Firefox/WebCord/Obsidian/VSCode foram removidos.

## O que tem
`hypr/` · `waybar/` · `wofi/` · `kitty/` · `tools/gen-colors.py`

## Dependências
`hyprland (0.56+, config em Lua) hyprpaper waybar wofi kitty jq cliphist wl-clipboard libnotify` + fonte **JetBrainsMono Nerd Font**.
Opcionais: `grimblast hyprpicker` (screenshot), `papirus-icon-theme`.

## Dois modos

### A) Por cima do illogical-impulse (end-4) — recomendado se você já usa
Não substitui nada seu. O shell gera as cores Material You a partir dos wallpapers do Snoopy.
```sh
./install-ii.sh --dry-run   # mostra o que faria
./install-ii.sh             # copia 2 arquivos p/ ~/.config/hypr/custom e acrescenta 1 linha em custom/general.lua (com backup)
hyprctl reload
```
- `SUPER+ALT+T` alterna **Day/Night** (ou `~/.config/hypr/custom/scripts/snoopy-theme.sh day|night`).
- Aplica bordas vermelhas, gaps e sombra estilo tirinha (`ii/hypr/custom/snoopy.lua`).
- Desfazer: `./install-ii.sh --uninstall`.

### B) Rice completo (Hyprland + Waybar + Wofi + Kitty)
Para quem **não** usa illogical-impulse.
```sh
./install.sh --dry-run
./install.sh             # symlinks em ~/.config (backup *.bak-<data>)
```
⚠️ Substitui `~/.config/hypr`. Ajuste o bloco "AJUSTE PARA O SEU PC" em `hypr/hyprland.lua` (monitor/teclado).

## Terminal
Kitty afinado (fonte 13, padding, abas arredondadas, cursor com rastro), prompt **powerlevel10k** nas cores do tema
(segue Day/Night) e `ff` = fastfetch com o wallpaper do Snoopy. O `install.sh` acrescenta 1 linha ao `~/.zshrc`
(com backup). Opcionais para cores/sugestões: `sudo pacman -S zsh-autosuggestions zsh-syntax-highlighting fzf`.

## Atalhos principais
`SUPER+Enter` kitty · `SUPER+D` launcher · `SUPER+B` power menu · `SUPER+C` calculadora ·
`SUPER+V` clipboard · `SUPER+.` emoji · `SUPER+SHIFT+T` **trocar Day/Night** · `SUPER+Q` fechar.

## Mudar as cores
Edite as paletas em `tools/gen-colors.py` e rode `python3 tools/gen-colors.py` — regenera hypr, waybar, wofi,
kitty e power-menu de uma vez.

## Wallpapers
Por serem arte da Peanuts Worldwide, **não estão no repo**. Baixe um de dia e um de noite
(ex.: [Snoopy](https://wallpapers.com/snoopy-pictures), [Woodstock](https://wallpapers.com/woodstock-background),
[Peanuts](https://wallpapers.com/peanuts-background)) e salve como `~/Pictures/snoopy-day.png` e
`~/Pictures/snoopy-night.png` (os caminhos ficam em `hypr/hyprpaper/*.conf`).

*Peanuts e Snoopy são marcas de Peanuts Worldwide / Charles M. Schulz. Projeto de fã, sem fins comerciais.*
