#!/usr/bin/env python3
"""Snoopy Settings — central de configurações do rice Hyprland/Snoopy (GTK4 + libadwaita)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, GLib, Gtk

import backend as B
import style
from pages import PAGES


class Window(Adw.ApplicationWindow):
    def __init__(self, app, start="theme"):
        super().__init__(application=app, title="Snoopy Settings", default_width=1120, default_height=760)
        self.provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.provider,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.reload_theme()
        self.cache = {}

        root = Gtk.Box()
        # --- barra lateral
        side = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        side.add_css_class("snoopy-sidebar")
        side.set_size_request(250, -1)
        brand = Gtk.Label(use_markup=True, xalign=0)
        brand.set_markup('<span size="large" foreground="#ef5b4f"></span>  Snoopy <span size="small" alpha="60%">Settings</span>')
        brand.add_css_class("snoopy-brand")
        side.append(brand)
        self.nav = Gtk.ListBox()
        self.nav.add_css_class("snoopy-nav")
        self.nav.set_selection_mode(Gtk.SelectionMode.SINGLE)
        for pid, ic, label, _b in PAGES:
            row = Gtk.ListBoxRow()
            row.pid = pid
            box = Gtk.Box()
            i = Gtk.Label(label=ic)
            i.add_css_class("icon")
            box.append(i)
            box.append(Gtk.Label(label=label, xalign=0))
            row.set_child(box)
            self.nav.append(row)
        self.nav.connect("row-selected", self.on_nav)
        side.append(self.nav)
        root.append(side)

        # --- conteúdo
        self.toasts = Adw.ToastOverlay()
        tv = Adw.ToolbarView()
        self.header = Adw.HeaderBar()
        self.title = Adw.WindowTitle(title="Tema", subtitle="")
        self.header.set_title_widget(self.title)
        tv.add_top_bar(self.header)
        self.stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE, hexpand=True, vexpand=True)
        tv.set_content(self.stack)
        self.toasts.set_child(tv)
        self.toasts.set_hexpand(True)
        root.append(self.toasts)
        self.set_content(root)
        self.show_page(start)

    def on_nav(self, _lb, row):
        if row:
            self.show_page(row.pid)

    def show_page(self, pid, rebuild=False):
        meta = next(p for p in PAGES if p[0] == pid)
        if rebuild or pid not in self.cache:
            old = self.cache.pop(pid, None)
            if old is not None:
                self.stack.remove(old)
            w = meta[3](self)
            self.cache[pid] = w
            self.stack.add_named(w, pid)
        self.stack.set_visible_child_name(pid)
        self.title.set_title(meta[2])
        row = self.nav.get_row_at_index([p[0] for p in PAGES].index(pid))
        if self.nav.get_selected_row() is not row:
            self.nav.select_row(row)

    def toast(self, text):
        self.toasts.add_toast(Adw.Toast(title=text, timeout=2))

    def reload_theme(self):
        theme = B.current_theme()
        Adw.StyleManager.get_default().set_color_scheme(
            Adw.ColorScheme.FORCE_LIGHT if theme.endswith("day") else Adw.ColorScheme.FORCE_DARK)
        self.provider.load_from_string(style.css(theme))


class App(Adw.Application):
    def __init__(self, start):
        super().__init__(application_id="dev.snoopy.Settings")
        self.start = start

    def do_activate(self):
        win = self.props.active_window or Window(self, self.start)
        win.present()


if __name__ == "__main__":
    start = "theme"
    if "--page" in sys.argv:
        start = sys.argv[sys.argv.index("--page") + 1]
    sys.exit(App(start).run([sys.argv[0]]))
