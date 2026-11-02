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

## Instalar
```sh
./install.sh --dry-run   # mostra o que faria
./install.sh             # symlinks em ~/.config (backup *.bak-<data> do que existir)
```
⚠️ Isso **substitui** `~/.config/hypr` (inclui o seu, se usar illogical-impulse/end-4). O backup fica ao lado;
para voltar, apague o symlink e renomeie o `.bak`. Antes, ajuste em `hypr/hyprland.lua` o bloco
"AJUSTE PARA O SEU PC" (monitores e layout de teclado).

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
