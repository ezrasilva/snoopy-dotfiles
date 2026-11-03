"""Páginas do Snoopy Settings. Cada build_* recebe a janela (win) e devolve um widget."""
import subprocess
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk

import backend as B
import style
from ui import (action_row, bg, button, clear, combo_row, entry_row, glyph, group, new_list, page, pill,
                scale_row, spin_row, switch_row)


# ============================================================ Tema
def build_theme(win):
    pg = page("Tema")
    cur = B.current_theme()

    g = group("Tema", "Escolha entre o dia e a noite do Snoopy. Troca barra, terminal, menus, bloqueio e wallpaper.")
    row = Gtk.Box(spacing=16, homogeneous=True)
    cards = {}

    def select(name):
        for n, c in cards.items():
            (c.add_css_class if n == name else c.remove_css_class)("selected")
        win.toast("Aplicando tema…")
        bg(lambda: B.set_theme(name), lambda _r: (win.reload_theme(), win.toast("Tema aplicado")))

    for name, label, glyph_ in (("snoopy-day", "Snoopy Day", "󰖙"), ("snoopy-night", "Snoopy Night", "󰖔")):
        card = Gtk.Button()
        card.add_css_class("theme-card")
        card.add_css_class("flat")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        wp = B.wallpaper_path(name)
        if wp.exists():
            pic = Gtk.Picture.new_for_filename(str(wp))
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(280, 160)
            pic.set_overflow(Gtk.Overflow.HIDDEN)
            box.append(pic)
        else:
            ph = Gtk.Label(label="sem wallpaper")
            ph.set_size_request(280, 160)
            ph.add_css_class("dim-label")
            box.append(ph)
        t = Gtk.Label(label=f"{glyph_}  {label}", xalign=0)
        t.add_css_class("name")
        box.append(t)
        card.set_child(box)
        card.connect("clicked", lambda _b, n=name: select(n))
        if name == cur:
            card.add_css_class("selected")
        cards[name] = card
        row.append(card)
    g.add(row)
    pg.add(g)

    g2 = group("Wallpapers", "As imagens ficam em ~/Pictures (snoopy-day.png / snoopy-night.png).")
    for name, label in (("snoopy-day", "Wallpaper do dia"), ("snoopy-night", "Wallpaper da noite")):
        r = action_row(label, str(B.wallpaper_path(name)).replace(str(B.HOME), "~"))
        def choose(_n=name):
            dlg = Gtk.FileDialog()
            flt = Gtk.FileFilter()
            flt.set_name("Imagens")
            flt.add_mime_type("image/png")
            flt.add_mime_type("image/jpeg")
            flt.add_mime_type("image/webp")
            store = Gio.ListStore.new(Gtk.FileFilter)
            store.append(flt)
            dlg.set_filters(store)
            def done(d, res):
                try:
                    f = d.open_finish(res)
                except GLib.Error:
                    return
                win.toast("Aplicando wallpaper…")
                bg(lambda: B.set_wallpaper(_n, f.get_path()),
                   lambda ok: win.toast("Wallpaper aplicado" if ok is True else "Não consegui converter a imagem"))
            dlg.open(win, None, done)
        r.add_suffix(button("Escolher…", choose))
        g2.add(r)
    pg.add(g2)

    g3 = group("Paleta atual")
    pal = style.palette(cur)
    sw = Gtk.Box(spacing=6, homogeneous=True)
    for k in ("red", "orange", "yellow", "green", "aqua", "blue", "purple", "fg", "bg0"):
        da = Gtk.DrawingArea()
        da.set_content_height(44)
        def draw(_a, cr, w, h, col=pal[k]):
            c = col.lstrip("#")
            cr.set_source_rgb(*(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)))
            r = 10
            cr.new_sub_path()
            cr.arc(w - r, r, r, -1.5708, 0); cr.arc(w - r, h - r, r, 0, 1.5708)
            cr.arc(r, h - r, r, 1.5708, 3.1416); cr.arc(r, r, r, 3.1416, 4.7124)
            cr.close_path(); cr.fill()
        da.set_draw_func(draw)
        da.set_tooltip_text(f"{k}  {pal[k]}")
        sw.append(da)
    g3.add(sw)
    pg.add(g3)
    return pg


# ============================================================ Aparência
def build_appearance(win):
    pg = page("Aparência")
    g = group("Janelas", "As mudanças valem na hora e ficam salvas.")
    def cfg(path):
        return B.get_value(path)
    def put(path):
        return lambda v: B.set_config(B.nested(path, int(v) if isinstance(v, float) and float(v).is_integer() else v))
    g.add(spin_row("Espaço entre janelas", "gaps_in", 0, 40, 1, cfg(["general", "gaps_in"]), put(["general", "gaps_in"])))
    g.add(spin_row("Espaço até a borda da tela", "gaps_out", 0, 60, 1, cfg(["general", "gaps_out"]), put(["general", "gaps_out"])))
    g.add(spin_row("Espessura da borda", "border_size", 0, 10, 1, cfg(["general", "border_size"]), put(["general", "border_size"])))
    g.add(spin_row("Arredondamento", "rounding", 0, 40, 1, cfg(["decoration", "rounding"]), put(["decoration", "rounding"])))
    pg.add(g)

    g2 = group("Efeitos")
    g2.add(switch_row("Sombra sólida", "Efeito 3D embaixo das janelas", cfg(["decoration", "shadow", "enabled"]),
                      lambda v: B.set_config({"decoration": {"shadow": {"enabled": v}}})))
    g2.add(switch_row("Desfoque (blur)", "Mais bonito, mais pesado para a GPU", cfg(["decoration", "blur", "enabled"]),
                      lambda v: B.set_config({"decoration": {"blur": {"enabled": v}}})))
    g2.add(switch_row("Animações", None, cfg(["animations", "enabled"]),
                      lambda v: B.set_config({"animations": {"enabled": v}})))
    pg.add(g2)

    g3 = group("Restaurar")
    g3.add(action_row("Voltar ao padrão do tema", "Apaga todos os ajustes salvos por este app",
                      button("Restaurar", lambda: (B.reset_settings(), win.toast("Ajustes restaurados"),
                                                   win.show_page("appearance", rebuild=True)), "destructive-action")))
    pg.add(g3)
    return pg


# ============================================================ Telas
def build_displays(win):
    pg = page("Telas")
    g = group("Disposição", "Como usar o notebook e a tela externa.")
    box = Gtk.Box(spacing=10, homogeneous=True)
    for mode, label in (("extend", "󰍹  Estender"), ("mirror", "󰍺  Espelhar"),
                        ("internal", "󰌢  Só notebook"), ("external", "󰍹  Só externa")):
        box.append(button(label, lambda m=mode: bg(lambda: B.monitor_layout(m),
                   lambda ok: win.toast("Disposição aplicada" if ok else "Conecte uma segunda tela")), valign=False))
    g.add(box)
    pg.add(g)

    for m in B.monitors():
        name = m["name"]
        gm = group(f"{name}", m.get("description", ""))
        modes = []
        for s in m.get("availableModes", []):
            if s not in modes:
                modes.append(s)
        cur = f'{m["width"]}x{m["height"]}@{m["refreshRate"]:.2f}Hz'
        idx = next((i for i, s in enumerate(modes) if s.startswith(f'{m["width"]}x{m["height"]}@') and
                    abs(float(s.split("@")[1][:-2]) - m["refreshRate"]) < 0.5), 0)
        if modes:
            gm.add(combo_row("Resolução e taxa", f"Atual: {cur}", modes, idx,
                             lambda i, n=name, ms=modes: B.set_monitor(n, mode=ms[i], position="auto" if False else
                                                                       f'{[x for x in B.monitors() if x["name"] == n][0]["x"]}x{[x for x in B.monitors() if x["name"] == n][0]["y"]}',
                                                                       scale=[x for x in B.monitors() if x["name"] == n][0]["scale"])))
        gm.add(spin_row("Escala", "1 = tamanho normal; 2 = HiDPI", 0.5, 3, 0.25, m["scale"],
                        lambda v, n=name: B.set_monitor(n, scale=v), digits=2))
        gm.add(action_row("Posição", f'{m["x"]}x{m["y"]}  ·  {"principal" if m.get("focused") else ""}'.strip(" ·")))
        pg.add(gm)
    return pg


# ============================================================ Som
def build_sound(win):
    pg = page("Som")
    for kind, title, glyph_ in (("sinks", "Saída", "󰕾"), ("sources", "Entrada (microfone)", "󰍬")):
        g = group(title)
        devs = B.audio_devices(kind)
        if not devs:
            g.add(action_row("Nenhum dispositivo encontrado"))
            pg.add(g)
            continue
        di = next((i for i, d in enumerate(devs) if d["default"]), 0)
        state = {"dev": devs[di]}
        vol_row = scale_row(f"{glyph_}  Volume", None, 0, 150, state["dev"]["volume"],
                            lambda v: B.set_audio_volume(kind, state["dev"]["name"], v), fmt="{:.0f}%")
        mute = switch_row("Mudo", None, state["dev"]["mute"], lambda v: B.set_audio_mute(kind, state["dev"]["name"], v))
        def pick(i, devs=devs, vol_row=vol_row, mute=mute, kind=kind, state=state):
            state["dev"] = devs[i]
            B.set_default_audio(kind, devs[i]["name"])
            vol_row.scale.set_value(devs[i]["volume"])
            mute.set_active(devs[i]["mute"])
        g.add(combo_row("Dispositivo", "O padrão do sistema", [d["desc"] for d in devs], di, pick))
        g.add(vol_row)
        g.add(mute)
        pg.add(g)
    g = group("Mais")
    g.add(action_row("Mixer completo", "Volume por aplicativo e perfis de áudio",
                     button("Abrir pavucontrol", lambda: subprocess.Popen(["pavucontrol"],
                            start_new_session=True) if B.have("pavucontrol") else win.toast("pavucontrol não instalado"))))
    pg.add(g)
    return pg


# ============================================================ Brilho e energia
def build_power(win):
    pg = page("Energia")
    g = group("Tela")
    b = B.brightness()
    if b is None:
        g.add(action_row("Brilho indisponível", "brightnessctl não encontrou uma tela com controle"))
    else:
        g.add(scale_row("󰃠  Brilho", "Também funciona com as teclas Fn", 1, 100, b, B.set_brightness, fmt="{:.0f}%"))
    pg.add(g)

    p = B.power_values()
    g2 = group("Inatividade", "Em minutos. 0 desativa a etapa. Usa o hypridle.")
    rows = {}
    for key, title, sub in (("dim", "Diminuir o brilho", "Baixa para 20% quando você para de usar"),
                            ("lock", "Bloquear a tela", "hyprlock com o visual do tema"),
                            ("screen_off", "Desligar a tela", "Liga de volta ao mexer no mouse"),
                            ("suspend", "Suspender", "Economiza energia")):
        rows[key] = spin_row(title, sub, 0, 120, 1, p[key] / 60, lambda v: None, digits=0)
        g2.add(rows[key])
    def apply():
        vals = {k: int(r.get_value() * 60) for k, r in rows.items()}
        B.apply_power(vals)
        win.toast("Tempos aplicados")
    g2.add(action_row("Aplicar", "Reinicia o hypridle com os novos tempos", button("Aplicar", apply, "suggested-action")))
    pg.add(g2)

    g3 = group("Sessão")
    for label, cmd in (("󰌾  Bloquear agora", ["loginctl", "lock-session"]),
                       ("󰤄  Suspender", ["systemctl", "suspend"])):
        g3.add(action_row(label.split("  ")[1], "", button(label.split("  ")[0] and "Executar",
                         lambda c=cmd: subprocess.Popen(c, start_new_session=True))))
    pg.add(g3)
    return pg


# ============================================================ Rede
def build_network(win):
    pg = page("Rede")

    gw = group("Wi-Fi")
    sw = switch_row("Wi-Fi", "Ligar ou desligar o rádio", B.wifi_enabled(), lambda v: (B.wifi_set(v), refresh_wifi()))
    gw.add(sw)
    wl = new_list()
    gw.add(wl)
    gw.set_header_suffix(button("Atualizar", lambda: refresh_wifi(True), "flat"))
    pg.add(gw)

    def ask_password(ssid):
        dlg = Adw.AlertDialog(heading=f"Senha de {ssid}", body="Digite a senha da rede.")
        entry = Gtk.PasswordEntry(show_peek_icon=True)
        dlg.set_extra_child(entry)
        dlg.add_response("cancel", "Cancelar")
        dlg.add_response("ok", "Conectar")
        dlg.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dlg.set_default_response("ok")
        entry.connect("activate", lambda _e: dlg.response("ok") if hasattr(dlg, "response") else None)
        def resp(d, r):
            if r == "ok" and entry.get_text():
                connect(ssid, entry.get_text())
        dlg.connect("response", resp)
        dlg.present(win)

    def connect(ssid, pwd=None):
        win.toast(f"Conectando a {ssid}…")
        bg(lambda: B.wifi_connect(ssid, pwd),
           lambda ok: (win.toast("Conectado" if ok is True else "Falha ao conectar"), refresh_wifi()))

    def refresh_wifi(rescan=False):
        clear(wl)
        if not B.wifi_enabled():
            wl.append(action_row("Wi-Fi desligado"))
            return
        wl.append(action_row("Procurando redes…"))
        def done(nets):
            clear(wl)
            if isinstance(nets, Exception) or not nets:
                wl.append(action_row("Nenhuma rede encontrada"))
                return
            for n in nets:
                bars = "󰤨" if n["signal"] >= 75 else "󰤥" if n["signal"] >= 50 else "󰤢" if n["signal"] >= 25 else "󰤟"
                r = action_row(f'{bars}  {n["ssid"]}', ("Conectada · " if n["active"] else "") +
                               ("protegida" if n["secure"] else "aberta") + f'  ·  {n["signal"]}%')
                if n["active"]:
                    r.add_suffix(pill("conectada", "ok"))
                    r.add_suffix(button("Desconectar", lambda s=n["ssid"]: bg(lambda: B.wifi_disconnect(s),
                                                                              lambda _r: refresh_wifi())))
                else:
                    r.add_suffix(button("Conectar", lambda n=n: connect(n["ssid"]) if B.wifi_saved(n["ssid"]) or not n["secure"]
                                        else ask_password(n["ssid"]), "suggested-action"))
                wl.append(r)
        bg(lambda: B.wifi_list(rescan), done)

    gb = group("Bluetooth")
    bsw = switch_row("Bluetooth", "Ligar ou desligar o adaptador", B.bt_powered(), lambda v: (B.bt_set(v), refresh_bt()))
    gb.add(bsw)
    bl = new_list()
    gb.add(bl)
    gb.set_header_suffix(button("Procurar", lambda: scan_bt(), "flat"))
    pg.add(gb)

    def scan_bt():
        win.toast("Procurando dispositivos por 8 s…")
        bg(lambda: B.bt_scan(8), lambda _r: refresh_bt())

    def refresh_bt():
        clear(bl)
        if not B.bt_powered():
            bl.append(action_row("Bluetooth desligado"))
            return
        def done(devs):
            clear(bl)
            if isinstance(devs, Exception) or not devs:
                bl.append(action_row("Nenhum dispositivo conhecido", "Use “Procurar” com o aparelho em modo de pareamento"))
                return
            for d in devs:
                st = "conectado" if d["connected"] else "pareado" if d["paired"] else "novo"
                r = action_row(("󰂱  " if d["connected"] else "󰂯  ") + d["name"], d["mac"] + "  ·  " + st)
                if d["connected"]:
                    r.add_suffix(pill("conectado", "ok"))
                r.add_suffix(button("Desconectar" if d["connected"] else "Conectar" if d["paired"] else "Parear",
                                    lambda d=d: (win.toast("Aguarde…"), bg(lambda: B.bt_toggle(d),
                                    lambda ok: (win.toast("Pronto" if ok else "Não deu certo"), refresh_bt()))),
                                    "" if d["connected"] else "suggested-action"))
                if d["paired"]:
                    r.add_suffix(button("Esquecer", lambda d=d: (B.bt_remove(d["mac"]), refresh_bt()), "flat"))
                bl.append(r)
        bg(B.bt_devices, done)

    refresh_wifi()
    refresh_bt()
    return pg


# ============================================================ Entrada
def build_input(win):
    pg = page("Entrada")
    def cfg(p):
        return B.get_value(["input"] + p)
    g = group("Teclado")
    for key, title, sub in (("kb_layout", "Layout", "ex.: br, us, us,br"), ("kb_variant", "Variante", "ex.: intl"),
                            ("kb_model", "Modelo", "ex.: abnt2"), ("kb_options", "Opções", "ex.: caps:escape, grp:alt_shift_toggle")):
        g.add(entry_row(title, cfg([key]), lambda t, k=key: (B.set_config({"input": {k: t}}), win.toast("Teclado atualizado"))))
    g.add(spin_row("Atraso de repetição", "ms até repetir a tecla", 150, 1000, 25, cfg(["repeat_delay"]),
                   lambda v: B.set_config({"input": {"repeat_delay": int(v)}})))
    g.add(spin_row("Velocidade de repetição", "caracteres por segundo", 5, 80, 1, cfg(["repeat_rate"]),
                   lambda v: B.set_config({"input": {"repeat_rate": int(v)}})))
    pg.add(g)
    g2 = group("Mouse e touchpad")
    g2.add(switch_row("Rolagem natural", "O conteúdo acompanha o dedo", cfg(["touchpad", "natural_scroll"]),
                      lambda v: B.set_config({"input": {"touchpad": {"natural_scroll": v}}})))
    g2.add(scale_row("Sensibilidade", "-1 = lento · 1 = rápido", -1, 1, float(cfg(["sensitivity"]) or 0),
                     lambda v: B.set_config({"input": {"sensitivity": round(v, 2)}}), step=0.05, fmt="{:+.2f}"))
    pg.add(g2)
    return pg


# ============================================================ Atalhos
def build_shortcuts(win):
    pg = page("Atalhos")
    g = group("Atalhos do teclado", "Lidos dos arquivos do tema atual.")
    search = Gtk.SearchEntry(placeholder_text="Buscar atalho…")
    g.add(search)
    lb = new_list()
    rows = []
    for combo, desc in B.keybinds():
        r = Adw.ActionRow(title=GLib.markup_escape_text(desc))
        keys = Gtk.Box(spacing=4)
        for k in combo.replace(" + ", "+").split("+"):
            kc = Gtk.Label(label=k.replace("SUPER", "Super").replace("SHIFT", "Shift").replace("CTRL", "Ctrl")
                           .replace("ALT", "Alt"))
            kc.add_css_class("keycap")
            keys.append(kc)
        keys.set_valign(Gtk.Align.CENTER)
        r.add_suffix(keys)
        r._text = (desc + " " + combo).lower()
        lb.append(r)
        rows.append(r)
    def flt(row):
        q = search.get_text().lower()
        return q in getattr(row, "_text", "")
    lb.set_filter_func(flt)
    search.connect("search-changed", lambda _s: lb.invalidate_filter())
    g.add(lb)
    pg.add(g)
    return pg


# ============================================================ Sobre
def build_about(win):
    pg = page("Sobre")
    g = group()
    top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, halign=Gtk.Align.CENTER)
    p = glyph("\uf1b0", "stat")
    top.append(p)
    t = Gtk.Label(label="Snoopy Settings")
    t.add_css_class("heading")
    top.append(t)
    s = Gtk.Label(label="Hyprland + tema Peanuts")
    s.add_css_class("dim-label")
    top.append(s)
    g.add(top)
    pg.add(g)
    g2 = group("Sistema")
    for k, v in B.system_info().items():
        g2.add(action_row(k, str(v)))
    pg.add(g2)
    g3 = group("Ações")
    g3.add(action_row("Reaplicar tema", "Reinicia barra, wallpaper, notificações e cores do terminal",
                      button("Reaplicar", lambda: bg(lambda: subprocess.run(
                          ["sh", str(B.HYPR_DIR / "scripts" / "switch-theme.sh"), B.current_theme()]),
                          lambda _r: win.toast("Tema reaplicado")))))
    g3.add(action_row("Repositório", "github.com/ezrasilva/snoopy-dotfiles",
                      button("Abrir", lambda: subprocess.Popen(["xdg-open", "https://github.com/ezrasilva/snoopy-dotfiles"],
                                                               start_new_session=True))))
    pg.add(g3)
    return pg


PAGES = [
    ("theme", "󰏘", "Tema", build_theme),
    ("appearance", "󰣆", "Aparência", build_appearance),
    ("displays", "󰍹", "Telas", build_displays),
    ("sound", "󰕾", "Som", build_sound),
    ("power", "󰁹", "Energia", build_power),
    ("network", "󰖩", "Rede", build_network),
    ("input", "󰌌", "Entrada", build_input),
    ("shortcuts", "󰌓", "Atalhos", build_shortcuts),
    ("about", "󰋽", "Sobre", build_about),
]
