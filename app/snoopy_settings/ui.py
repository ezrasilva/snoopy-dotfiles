"""Pequenos construtores de widgets para manter as páginas curtas."""
import threading
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk


def bg(fn, done=None):
    """Roda fn numa thread; done(resultado) volta na thread da interface."""
    def work():
        try:
            res = fn()
        except Exception as e:  # nunca deixa a UI quebrar por erro de comando
            res = e
        if done:
            GLib.idle_add(done, res)
    threading.Thread(target=work, daemon=True).start()


def debounce(fn, ms=250):
    """Devolve um callback que só dispara fn depois de ms sem novas chamadas (sliders)."""
    state = {"id": 0}
    def call(*a):
        if state["id"]:
            GLib.source_remove(state["id"])
        def fire():
            state["id"] = 0
            fn(*a)
            return False
        state["id"] = GLib.timeout_add(ms, fire)
    return call


def page(title, icon=None):
    p = Adw.PreferencesPage()
    p.set_title(title)
    return p


def group(title=None, desc=None, header_suffix=None):
    g = Adw.PreferencesGroup()
    if title:
        g.set_title(title)
    if desc:
        g.set_description(desc)
    if header_suffix is not None:
        g.set_header_suffix(header_suffix)
    return g


def glyph(ch, css="big-icon"):
    l = Gtk.Label(label=ch)
    l.add_css_class(css)
    return l


def switch_row(title, subtitle, active, on_toggle):
    r = Adw.SwitchRow(title=title, subtitle=subtitle or "")
    r.set_active(bool(active))
    r.connect("notify::active", lambda w, _p: on_toggle(w.get_active()))
    return r


def spin_row(title, subtitle, lo, hi, step, value, on_change, digits=0):
    r = Adw.SpinRow.new_with_range(lo, hi, step)
    r.set_title(title)
    r.set_subtitle(subtitle or "")
    r.set_digits(digits)
    r.set_value(value)
    cb = debounce(on_change, 300)
    r.connect("notify::value", lambda w, _p: cb(w.get_value()))
    return r


def scale_row(title, subtitle, lo, hi, value, on_change, step=1, fmt="{:.0f}"):
    r = Adw.ActionRow(title=title, subtitle=subtitle or "")
    s = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, lo, hi, step)
    s.set_value(value)
    s.set_hexpand(True)
    s.set_size_request(240, -1)
    s.set_valign(Gtk.Align.CENTER)
    lab = Gtk.Label(label=fmt.format(value))
    lab.set_width_chars(5)
    lab.add_css_class("pill")
    cb = debounce(on_change, 200)
    def changed(w):
        lab.set_label(fmt.format(w.get_value()))
        cb(w.get_value())
    s.connect("value-changed", changed)
    r.add_suffix(s)
    r.add_suffix(lab)
    r.scale = s
    return r


def combo_row(title, subtitle, items, selected, on_select):
    r = Adw.ComboRow(title=title, subtitle=subtitle or "")
    r.set_model(Gtk.StringList.new(items))
    if items:
        r.set_selected(max(0, min(selected, len(items) - 1)))
    r.connect("notify::selected", lambda w, _p: on_select(w.get_selected()))
    return r


def entry_row(title, text, on_apply):
    r = Adw.EntryRow(title=title)
    r.set_text(text or "")
    r.set_show_apply_button(True)
    r.connect("apply", lambda w: on_apply(w.get_text()))
    return r


def button(label, on_click, css=None, valign=True):
    b = Gtk.Button(label=label)
    if css:
        b.add_css_class(css)
    if valign:
        b.set_valign(Gtk.Align.CENTER)
    b.connect("clicked", lambda _b: on_click())
    return b


def action_row(title, subtitle="", suffix=None, activatable=False):
    r = Adw.ActionRow(title=GLib.markup_escape_text(title), subtitle=GLib.markup_escape_text(subtitle or ""))
    if suffix is not None:
        r.add_suffix(suffix)
    r.set_activatable(activatable)
    return r


def pill(text, kind=""):
    l = Gtk.Label(label=text)
    l.add_css_class("pill")
    if kind:
        l.add_css_class(kind)
    l.set_valign(Gtk.Align.CENTER)
    return l


def clear(listbox):
    child = listbox.get_first_child()
    while child:
        nxt = child.get_next_sibling()
        listbox.remove(child)
        child = nxt


def new_list():
    lb = Gtk.ListBox()
    lb.set_selection_mode(Gtk.SelectionMode.NONE)
    lb.add_css_class("boxed-list")
    return lb
