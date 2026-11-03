#!/usr/bin/env python3
"""Fonte única das paletas Snoopy. Gera as cores de hypr, waybar, wofi, kitty e power-menu.

Uso: python3 tools/gen-colors.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PALETTES = {
    # Wallpaper "Snoopy na colina": nuvens creme, céu turquesa, grama verde, coleira vermelha
    "snoopy-day": dict(
        bg_dim="#e6e1b8", bg0="#f7f1d2", bg1="#f0ebc6", bg2="#e6e1b8", bg3="#d9d8ae",
        bg4="#c8cfa5", bg5="#a6b79a", bg_visual="#e3e5b0", bg_red="#f4d6c8",
        bg_green="#d8ebc4", bg_blue="#cfe9e6", bg_yellow="#f6e8a6",
        fg="#26323a", red="#c8423a", orange="#e08a3c", yellow="#e0b020",
        green="#3f9a64", aqua="#2a9d8f", blue="#1b8a99", purple="#7d6aa6",
        grey0="#9aa28c", grey1="#7f897a", grey2="#5f6b66",
    ),
    # Barão Vermelho à noite: céu azul-marinho, lua e Woodstock amarelo
    "snoopy-night": dict(
        bg_dim="#141829", bg0="#1c2136", bg1="#232942", bg2="#2b324f", bg3="#353d5e",
        bg4="#40496d", bg5="#56608a", bg_visual="#4a3b52", bg_red="#4a2f3b",
        bg_green="#2f4a3f", bg_blue="#2b4466", bg_yellow="#4d4531",
        fg="#f5ecd7", red="#ef5b4f", orange="#ff9f55", yellow="#ffd35c",
        green="#8fc479", aqua="#5cc3b8", blue="#6aa9e8", purple="#c39bd3",
        grey0="#7b83a6", grey1="#9aa1c0", grey2="#b8bdd6",
    ),
}
KEYS = list(PALETTES["snoopy-day"])


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def main():
    for name, p in PALETTES.items():
        write(f"hypr/colors/{name}.lua",
              "-- gerado por tools/gen-colors.py\nreturn {\n"
              + "".join(f'    {k} = "rgb({p[k][1:]})",\n' for k in KEYS) + "}\n")
        write(f"hypr/colors/{name}.conf",
              "# gerado por tools/gen-colors.py (usado pelo hyprlock)\n"
              + "".join(f"${k} = rgb({p[k][1:]})\n" for k in KEYS)
              + f"$wallpaper = ~/Pictures/{name}.png\n")
        css = "\n".join(f"@define-color {k} {p[k]};" for k in KEYS) + "\n"
        write(f"waybar/colors/{name}.css", css)
        write(f"wofi/colors/{name}.css", css)

        ansi = [
            ("0", "8", p["bg3"], p["bg5"]), ("1", "9", p["red"], p["red"]),
            ("2", "10", p["green"], p["green"]), ("3", "11", p["yellow"], p["yellow"]),
            ("4", "12", p["blue"], p["blue"]), ("5", "13", p["purple"], p["purple"]),
            ("6", "14", p["aqua"], p["aqua"]),
            ("7", "15", p["fg"] if name == "snoopy-night" else p["grey2"], p["fg"]),
        ]
        k = [
            f"# Snoopy — gerado por tools/gen-colors.py ({name})",
            f"foreground            {p['fg']}", f"background            {p['bg0']}",
            f"selection_foreground  {p['fg']}", f"selection_background  {p['bg_visual']}",
            f"url_color             {p['blue']}", f"cursor                {p['red']}",
            f"cursor_text_color     {p['bg0']}",
            f"active_border_color   {p['red']}", f"inactive_border_color {p['bg5']}",
            f"active_tab_background {p['red']}", f"active_tab_foreground {p['bg0']}",
            f"inactive_tab_background {p['bg2']}", f"inactive_tab_foreground {p['fg']}",
        ]
        for a, b, c1, c2 in ansi:
            k += [f"color{a}  {c1}", f"color{b} {c2}"]
        write(f"kitty/colors/{name}.conf", "\n".join(k) + "\n")

        def a(h):
            return h.lstrip("#").upper() + "FF"
        write(f"waybar/scripts/power-menu/shared/colors/{name}.rasi",
              "* {\n"
              f"    background:     #{a(p['bg0'])};\n    background-alt: #{a(p['bg2'])};\n"
              f"    foreground:     #{a(p['fg'])};\n    selected:       #{a(p['red'])};\n"
              f"    active:         #{a(p['green'])};\n    urgent:         #{a(p['orange'])};\n}}\n")
    print("ok:", ", ".join(PALETTES))


if __name__ == "__main__":
    main()
