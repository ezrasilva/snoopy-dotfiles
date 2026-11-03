"""CSS do app a partir da paleta do tema (Day/Night). Visual: cartões com borda inferior 3D, cantos redondos."""
import json
from pathlib import Path

PALETTES = json.loads((Path(__file__).parent / "palettes.json").read_text())


def palette(theme):
    return PALETTES.get(theme, PALETTES["snoopy-night"])


def darker(h, f=0.78):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def css(theme):
    p = palette(theme)
    night = theme.endswith("night")
    side = p["bg_dim"] if night else p["fg"]           # barra lateral: escura nos dois temas
    side_fg = p["fg"] if night else p["bg0"]
    return f"""
@define-color window_bg_color {p['bg0']};
@define-color window_fg_color {p['fg']};
@define-color view_bg_color {p['bg0']};
@define-color view_fg_color {p['fg']};
@define-color card_bg_color {p['bg1']};
@define-color card_fg_color {p['fg']};
@define-color headerbar_bg_color {p['bg0']};
@define-color headerbar_fg_color {p['fg']};
@define-color popover_bg_color {p['bg1']};
@define-color popover_fg_color {p['fg']};
@define-color dialog_bg_color {p['bg0']};
@define-color dialog_fg_color {p['fg']};
@define-color accent_bg_color {p['blue']};
@define-color accent_color {p['blue']};
@define-color accent_fg_color {p['bg0']};
@define-color success_bg_color {p['green']};
@define-color warning_bg_color {p['yellow']};
@define-color error_bg_color {p['red']};
@define-color destructive_bg_color {p['red']};

* {{ font-family: "JetBrainsMono Nerd Font", monospace; }}
window, .background {{ background: {p['bg0']}; color: {p['fg']}; }}

/* ---- barra lateral ---- */
.snoopy-sidebar {{ background: {side}; color: {side_fg}; padding: 14px 10px; }}
.snoopy-brand {{ font-size: 18px; font-weight: 800; color: {side_fg}; padding: 6px 10px 14px 10px; }}
.snoopy-brand .paw {{ color: {p['red']}; font-size: 22px; }}
.snoopy-nav {{ background: transparent; }}
.snoopy-nav row {{
  border-radius: 12px; margin: 3px 0; padding: 9px 12px; color: {side_fg};
  background: transparent; border-bottom: 4px solid transparent;
}}
.snoopy-nav row:hover {{ background: alpha({side_fg}, .10); }}
.snoopy-nav row:selected {{
  background: {p['red']}; color: {p['bg0']}; border-bottom: 4px solid {darker(p['red'])};
}}
.snoopy-nav .icon {{ font-size: 18px; margin-right: 10px; }}

/* ---- conteúdo ---- */
headerbar {{ background: {p['bg0']}; box-shadow: none; border-bottom: 1px solid {p['bg3']}; }}
.title {{ font-weight: 800; }}
preferencespage > scrolledwindow > viewport > clamp > box {{ margin-top: 10px; }}

/* grupos e linhas viram cartões "3D" como na barra do rice */
preferencesgroup > box > box > list, .snoopy-card, list.boxed-list {{
  background: {p['bg1']}; border-radius: 16px; border: none;
  border-bottom: 4px solid {p['bg4']}; box-shadow: none;
}}
row {{ background: transparent; color: {p['fg']}; }}
list.boxed-list > row:first-child {{ border-top-left-radius: 14px; border-top-right-radius: 14px; }}
list.boxed-list > row:last-child {{ border-bottom-left-radius: 14px; border-bottom-right-radius: 14px; }}
row .subtitle, .dim-label {{ color: {p['grey2']}; }}
preferencesgroup > box > label.heading, .heading {{ color: {p['fg']}; font-weight: 800; }}

/* botões */
button {{ border-radius: 12px; border: none; background: {p['bg2']}; color: {p['fg']};
  border-bottom: 3px solid {p['bg4']}; box-shadow: none; padding: 6px 14px; }}
button:hover {{ background: {p['bg3']}; }}
button:active {{ border-bottom-width: 1px; margin-top: 2px; }}
button.suggested-action, button.snoopy-primary {{
  background: {p['blue']}; color: {p['bg0']}; border-bottom: 3px solid {darker(p['blue'])}; }}
button.destructive-action {{ background: {p['red']}; color: {p['bg0']}; border-bottom: 3px solid {darker(p['red'])}; }}
button.flat {{ background: transparent; border-bottom: none; }}

/* sliders, switches, campos */
scale trough {{ background: {p['bg3']}; border-radius: 99px; min-height: 8px; }}
scale highlight {{ background: {p['blue']}; border-radius: 99px; }}
scale slider {{ background: {p['bg0']}; border: 3px solid {p['blue']}; border-radius: 99px;
  min-width: 18px; min-height: 18px; box-shadow: none; }}
switch {{ background: {p['bg3']}; border-radius: 99px; border: none; }}
switch:checked {{ background: {p['green']}; }}
switch slider {{ background: {p['bg0']}; border-radius: 99px; box-shadow: none; }}
entry, spinbutton, .boxed-list entry {{ background: {p['bg2']}; border-radius: 10px; border: none;
  border-bottom: 3px solid {p['bg4']}; box-shadow: none; color: {p['fg']}; }}
row spinbutton, row spinbutton text, row spinbutton entry {{ background: transparent; border: none; box-shadow: none; min-width: 0; }}
row spinbutton button {{ min-width: 30px; }}
dropdown > button {{ background: {p['bg2']}; }}
popover contents, popover > contents {{ background: {p['bg1']}; border-radius: 14px; }}
levelbar trough {{ background: {p['bg3']}; border-radius: 99px; }}
levelbar block.filled {{ background: {p['blue']}; border-radius: 99px; }}

/* cartões de tema (Day/Night) */
.theme-card {{ background: {p['bg1']}; border-radius: 18px; padding: 10px;
  border-bottom: 5px solid {p['bg4']}; border-left: 3px solid transparent; border-right: 3px solid transparent;
  border-top: 3px solid transparent; }}
.theme-card.selected {{ border-color: {p['red']}; border-bottom: 5px solid {darker(p['red'])}; background: {p['bg_visual']}; }}
.theme-card picture {{ border-radius: 12px; }}
.theme-card .name {{ font-weight: 800; font-size: 15px; }}

.pill {{ background: {p['bg3']}; border-radius: 99px; padding: 2px 10px; font-size: 12px; }}
.pill.ok {{ background: {p['green']}; color: {p['bg0']}; }}
.pill.bad {{ background: {p['red']}; color: {p['bg0']}; }}
.keycap {{ background: {p['bg3']}; color: {p['fg']}; border-radius: 8px; border-bottom: 3px solid {p['bg5']};
  padding: 2px 8px; font-weight: 700; font-size: 12px; }}
.big-icon {{ font-size: 34px; color: {p['blue']}; }}
.stat {{ font-size: 28px; font-weight: 800; }}
toast {{ background: {p['fg']}; color: {p['bg0']}; border-radius: 14px; }}
"""
