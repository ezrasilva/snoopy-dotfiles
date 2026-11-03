"""Camada de sistema do Snoopy Settings: tudo que fala com hyprctl, nmcli, pactl etc."""
import json, os, re, shutil, subprocess
from pathlib import Path

HOME = Path.home()
CFG_DIR = HOME / ".config" / "snoopy"
SETTINGS_JSON = CFG_DIR / "settings.json"
SETTINGS_LUA = CFG_DIR / "settings.lua"
HYPR_DIR = HOME / ".config" / "hypr"
PICTURES = HOME / "Pictures"


def sh(cmd, timeout=15, inp=None):
    """Roda um comando; devolve (rc, stdout). Nunca levanta exceção."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, input=inp)
        return p.returncode, p.stdout.strip()
    except Exception as e:  # comando ausente, timeout...
        return 1, str(e)


def have(cmd):
    return shutil.which(cmd) is not None


# ------------------------------------------------------------------ tema
def current_theme():
    try:
        m = re.search(r"snoopy-[a-z]+", (HYPR_DIR / "hyprland.lua").read_text().splitlines()[0])
        return m.group(0) if m else "snoopy-night"
    except Exception:
        return "snoopy-night"


def set_theme(name):
    lua = HYPR_DIR / "hyprland.lua"
    lines = lua.read_text().split("\n")
    lines[0] = f'require("themes.{name}.{name}")'
    lua.write_text("\n".join(lines))
    sh(["hyprctl", "reload"])


def wallpaper_path(theme):
    return PICTURES / f"{theme}.png"


def set_wallpaper(theme, src):
    """Copia/converte a imagem escolhida para ~/Pictures/<tema>.png e reaplica o tema."""
    PICTURES.mkdir(exist_ok=True)
    dst = wallpaper_path(theme)
    if str(src).lower().endswith(".png"):
        shutil.copy(src, dst)
    elif have("magick"):
        sh(["magick", str(src), str(dst)], timeout=60)
    else:
        return False
    sh(["sh", str(HYPR_DIR / "scripts" / "switch-theme.sh"), current_theme()])
    return True


# ------------------------------------------------------------- configurações
DEFAULTS = {
    "general": {"gaps_in": 8, "gaps_out": 16, "border_size": 3},
    "decoration": {"rounding": 14, "blur": {"enabled": False}, "shadow": {"enabled": True}},
    "animations": {"enabled": True},
    "input": {"kb_layout": "br", "kb_variant": "", "kb_model": "abnt2", "kb_options": "caps:escape",
              "sensitivity": 0.0, "repeat_rate": 25, "repeat_delay": 600,
              "touchpad": {"natural_scroll": True}},
}
POWER_DEFAULTS = {"dim": 240, "lock": 300, "screen_off": 360, "suspend": 900}


def load_settings():
    try:
        return json.loads(SETTINGS_JSON.read_text())
    except Exception:
        return {}


def _get(d, path, default=None):
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def get_value(path, root="config"):
    """Valor salvo pelo usuário ou o padrão do tema."""
    s = load_settings().get(root, {})
    v = _get(s, path)
    if v is None:
        v = _get(DEFAULTS if root == "config" else {root: POWER_DEFAULTS}, path if root == "config" else path)
    return v


def _lua(v, ind=0):
    pad = "    " * (ind + 1)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, dict):
        items = ",\n".join(f"{pad}{k} = {_lua(x, ind + 1)}" for k, x in v.items())
        return "{\n" + items + "\n" + "    " * ind + "}"
    if isinstance(v, list):
        return "{ " + ", ".join(_lua(x, ind) for x in v) + " }"
    raise TypeError(type(v))


def _merge(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            _merge(a[k], v)
        else:
            a[k] = v


def save_settings(s):
    CFG_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_JSON.write_text(json.dumps(s, indent=2, ensure_ascii=False))
    parts = ["-- gerado pelo Snoopy Settings; edite pelo app"]
    if s.get("config"):
        parts.append("hl.config(" + _lua(s["config"]) + ")")
    for out, m in s.get("monitors", {}).items():
        parts.append("hl.monitor(" + _lua({"output": out, **m}) + ")")
    SETTINGS_LUA.write_text("\n".join(parts) + "\n")


def set_config(patch):
    """Aplica ao vivo (hyprctl eval) e persiste. patch = dict aninhado no formato do hl.config."""
    s = load_settings()
    s.setdefault("config", {})
    _merge(s["config"], patch)
    save_settings(s)
    sh(["hyprctl", "eval", "hl.config(" + _lua(patch) + ")"])


def nested(path, value):
    d = value
    for k in reversed(path):
        d = {k: d}
    return d


def set_monitor(name, **spec):
    s = load_settings()
    s.setdefault("monitors", {}).setdefault(name, {}).update(spec)
    save_settings(s)
    sh(["hyprctl", "eval", "hl.monitor(" + _lua({"output": name, **s["monitors"][name]}) + ")"])


def reset_settings():
    for f in (SETTINGS_JSON, SETTINGS_LUA):
        f.unlink(missing_ok=True)
    sh(["hyprctl", "reload"])


# ------------------------------------------------------------------ telas
def monitors():
    rc, out = sh(["hyprctl", "monitors", "all", "-j"])
    try:
        return json.loads(out)
    except Exception:
        return []


def monitor_layout(mode):
    """mode: extend | mirror | internal | external"""
    mons = [m["name"] for m in monitors()]
    internal = next((n for n in mons if n.startswith("eDP")), None)
    external = next((n for n in mons if not n.startswith("eDP")), None)
    if not internal or not external:
        return False
    if mode == "extend":
        set_monitor(internal, mode="preferred", position="0x0", scale=1, mirror="", disabled=False)
        set_monitor(external, mode="preferred", position="auto-right", scale=1, mirror="", disabled=False)
    elif mode == "mirror":
        set_monitor(internal, mode="preferred", position="0x0", mirror="", disabled=False)
        set_monitor(external, mode="preferred", position="0x0", mirror=internal, disabled=False)
    elif mode == "internal":
        set_monitor(internal, mode="preferred", position="0x0", mirror="", disabled=False)
        set_monitor(external, disabled=True)
    elif mode == "external":
        set_monitor(external, mode="preferred", position="0x0", mirror="", disabled=False)
        set_monitor(internal, disabled=True)
    return True


# --------------------------------------------------------------- brilho / som
def brightness():
    rc, out = sh(["brightnessctl", "-m"])
    try:
        return int(out.split(",")[3].rstrip("%"))
    except Exception:
        return None


def set_brightness(p):
    sh(["brightnessctl", "-q", "set", f"{int(p)}%"])


def _pactl(kind):
    rc, out = sh(["pactl", "-f", "json", "list", kind])
    try:
        return json.loads(out)
    except Exception:
        return []


def audio_devices(kind):  # kind: sinks | sources
    default = sh(["pactl", "get-default-" + kind[:-1]])[1]
    res = []
    for d in _pactl(kind):
        if d.get("monitor_source") is None and kind == "sources":
            pass
        if kind == "sources" and d["name"].endswith(".monitor"):
            continue
        vol = 0
        try:
            vol = int(list(d["volume"].values())[0]["value_percent"].rstrip("%"))
        except Exception:
            pass
        res.append({"name": d["name"], "desc": d.get("description", d["name"]), "volume": vol,
                    "mute": d.get("mute", False), "default": d["name"] == default})
    return res


def set_default_audio(kind, name):
    sh(["pactl", "set-default-" + kind[:-1], name])


def set_audio_volume(kind, name, pct):
    sh(["pactl", f"set-{kind[:-1]}-volume", name, f"{int(pct)}%"])


def set_audio_mute(kind, name, mute):
    sh(["pactl", f"set-{kind[:-1]}-mute", name, "1" if mute else "0"])


# ------------------------------------------------------------------ energia
def apply_power(p):
    s = load_settings()
    s["power"] = p
    save_settings(s)
    def block(t, on, resume=""):
        if not t:
            return ""
        r = f"\n    on-resume = {resume}" if resume else ""
        return f"listener {{\n    timeout = {t}\n    on-timeout = {on}{r}\n}}\n"
    conf = ("general {\n    lock_cmd = pidof hyprlock || hyprlock\n    before_sleep_cmd = loginctl lock-session\n"
            "    after_sleep_cmd = hyprctl dispatch dpms on\n}\n\n"
            + block(p["dim"], "brightnessctl -s set 20%", "brightnessctl -r")
            + block(p["lock"], "loginctl lock-session")
            + block(p["screen_off"], "hyprctl dispatch dpms off", "hyprctl dispatch dpms on && brightnessctl -r")
            + block(p["suspend"], "systemctl suspend"))
    CFG_DIR.mkdir(parents=True, exist_ok=True)
    (CFG_DIR / "hypridle.conf").write_text(conf)
    sh(["pkill", "-x", "hypridle"])
    subprocess.Popen(["hypridle", "-c", str(CFG_DIR / "hypridle.conf")], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)


def power_values():
    p = dict(POWER_DEFAULTS)
    p.update(load_settings().get("power", {}))
    return p


# --------------------------------------------------------------------- rede
def wifi_enabled():
    return sh(["nmcli", "radio", "wifi"])[1] == "enabled"


def wifi_set(on):
    sh(["nmcli", "radio", "wifi", "on" if on else "off"])


def wifi_list(rescan=False):
    rc, out = sh(["nmcli", "-t", "-f", "IN-USE,SIGNAL,SECURITY,SSID", "device", "wifi", "list",
                  "--rescan", "yes" if rescan else "no"], timeout=25)
    seen, res = set(), []
    for row in out.splitlines():
        inuse, rest = row.split(":", 1)
        sig, rest = rest.split(":", 1)
        sec, ssid = rest.split(":", 1)
        ssid = ssid.replace("\\:", ":")
        if not ssid or ssid in seen:
            continue
        seen.add(ssid)
        res.append({"ssid": ssid, "signal": int(sig or 0), "secure": bool(sec), "active": inuse == "*"})
    return sorted(res, key=lambda x: (not x["active"], -x["signal"]))


def wifi_saved(ssid):
    return ssid in sh(["nmcli", "-t", "-f", "NAME", "connection", "show"])[1].splitlines()


def wifi_connect(ssid, password=None):
    if password is None and wifi_saved(ssid):
        rc, out = sh(["nmcli", "connection", "up", "id", ssid], timeout=40)
    elif password:
        rc, out = sh(["nmcli", "--ask", "device", "wifi", "connect", ssid], timeout=40, inp=password + "\n")
    else:
        rc, out = sh(["nmcli", "device", "wifi", "connect", ssid], timeout=40)
    if rc != 0:
        sh(["nmcli", "connection", "delete", "id", ssid])
    return rc == 0


def wifi_disconnect(ssid):
    return sh(["nmcli", "connection", "down", "id", ssid])[0] == 0


def bt_powered():
    return "Powered: yes" in sh(["bluetoothctl", "show"])[1]


def bt_set(on):
    if on:
        sh(["rfkill", "unblock", "bluetooth"])
    sh(["bluetoothctl", "power", "on" if on else "off"])


def bt_devices():
    res = []
    for line in sh(["bluetoothctl", "devices"])[1].splitlines():
        parts = line.split(" ", 2)
        if len(parts) < 3:
            continue
        mac, name = parts[1], parts[2]
        info = sh(["bluetoothctl", "info", mac])[1]
        res.append({"mac": mac, "name": name, "connected": "Connected: yes" in info,
                    "paired": "Paired: yes" in info})
    return sorted(res, key=lambda d: (not d["connected"], not d["paired"], d["name"].lower()))


def bt_scan(seconds=8):
    sh(["bluetoothctl", "--timeout", str(seconds), "scan", "on"], timeout=seconds + 5)


def bt_toggle(dev):
    if dev["connected"]:
        return sh(["bluetoothctl", "disconnect", dev["mac"]])[0] == 0
    if not dev["paired"]:
        if sh(["bluetoothctl", "pair", dev["mac"]], timeout=40)[0] != 0:
            return False
        sh(["bluetoothctl", "trust", dev["mac"]])
    return sh(["bluetoothctl", "connect", dev["mac"]], timeout=25)[0] == 0


def bt_remove(mac):
    sh(["bluetoothctl", "remove", mac])


# ------------------------------------------------------------------ atalhos
BIND_RE = re.compile(r'hl\.bind\("([^"]+)",\s*(.+)\)\s*(?:,\s*\{[^}]*\})?\s*$')
DESC = {
    "hl.dsp.window.close": "Fechar janela", "hl.dsp.exit": "Sair do Hyprland",
    "hl.dsp.window.fullscreen": "Tela cheia", "hl.dsp.window.float": "Alternar flutuante",
    "hl.dsp.window.drag": "Mover janela (arrastar)", "hl.dsp.window.resize": "Redimensionar janela",
}


FRIENDLY = [
    ('"kitty"', "Abrir terminal"), ("toggle-gaps", "Alternar espaçamentos"),
    ("freeze-screenshot", "Captura de tela (área)"), ("lock-session", "Bloquear a tela"),
    ("display-menu", "Menu de telas"), ("wifi-menu", "Menu de Wi-Fi"), ("bluetooth-menu", "Menu de Bluetooth"),
    ("theme-switcher", "Trocar tema Day/Night"), ("--show drun", "Abrir o launcher"),
    ("powermenu", "Menu de energia"), ("wofi-calc", "Calculadora"), ("cliphist", "Histórico da área de transferência"),
    ("wofi-emoji", "Seletor de emoji"), ("snoopy-settings", "Abrir o Snoopy Settings"),
    ("volume up", "Aumentar volume"), ("volume down", "Diminuir volume"), ("volume mute", "Silenciar"),
    ("mic mute", "Silenciar microfone"), ("brightness up", "Aumentar brilho"), ("brightness down", "Diminuir brilho"),
    ("play-pause", "Tocar / pausar"), ("playerctl pause", "Pausar"), ("playerctl next", "Próxima faixa"),
    ("playerctl previous", "Faixa anterior"),
    ('workspace = "e+1"', "Próximo workspace"), ('workspace = "e-1"', "Workspace anterior"),
]


def keybinds():
    """Lê os hl.bind(...) dos arquivos Lua do rice e devolve [(atalho, descrição)]."""
    files = [HYPR_DIR / "hyprland.lua", HYPR_DIR / "themes" / current_theme() / f"{current_theme()}.lua"]
    out = []
    for f in files:
        try:
            text = f.read_text()
        except Exception:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("hl.bind("):
                continue
            m = BIND_RE.match(line)
            if not m:
                continue
            combo, action = m.group(1), m.group(2)
            desc = next((t for k, t in FRIENDLY if k in action), None) or \
                next((v for k, v in DESC.items() if action.startswith(k)), None)
            if not desc:
                if "focus({ workspace" in action:
                    desc = "Ir para o workspace"
                elif "window.move" in action:
                    desc = "Mover janela para o workspace"
                elif "focus({ direction" in action:
                    desc = "Focar janela vizinha"
                else:
                    desc = action[:48]
            out.append((combo.replace(" + ", " + "), desc))
    out += [("SUPER + 1 … 0", "Ir para o workspace 1–10"), ("SUPER + SHIFT + 1 … 0", "Mover janela para o workspace"),
            ("SUPER + ← ↑ ↓ →", "Focar janela vizinha")]
    return out


# -------------------------------------------------------------------- sobre
def system_info():
    def first(cmd):
        return sh(cmd)[1].splitlines()[0] if sh(cmd)[1] else "?"
    return {
        "Hyprland": first(["hyprctl", "version", "-j"]) and json.loads(sh(["hyprctl", "version", "-j"])[1]).get("tag", "?"),
        "Kernel": sh(["uname", "-r"])[1],
        "Shell": os.path.basename(os.environ.get("SHELL", "?")),
        "Terminal": "kitty " + (sh(["kitty", "--version"])[1].split()[1] if have("kitty") else "?"),
        "Tema": current_theme().replace("snoopy-", "Snoopy ").title(),
    }
