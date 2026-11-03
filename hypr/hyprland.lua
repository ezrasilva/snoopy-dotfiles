require("themes.snoopy-day.snoopy-day")
-- Snoopy dotfiles (Hyprland 0.56+, Lua). A 1ª linha escolhe o tema; o theme-switcher edita ela.

-- ---- AJUSTE PARA O SEU PC -------------------------------------------------
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })
hl.config({
    input = {
        kb_layout = "br", kb_model = "abnt2", kb_options = "caps:escape",
        follow_mouse = 1,
        touchpad = { natural_scroll = true },
    },
})
-- Workspaces: 1-5 na tela principal, 6-10 na secundária (se ela não existir, tudo cai na principal)
local main, side = "eDP-1", "HDMI-A-1"
for i = 1, 10 do
    hl.workspace_rule({ workspace = tostring(i), monitor = (i <= 5) and main or side,
                        persistent = true, default = (i == 1 or i == 6) })
end
-- ---------------------------------------------------------------------------

hl.config({ misc = { disable_hyprland_logo = true } })

hl.env("XDG_SESSION_TYPE", "wayland")
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("GDK_BACKEND", "wayland,x11")

hl.on("hyprland.start", function()
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
    hl.exec_cmd("hypridle")
    hl.exec_cmd("wl-paste --type text --watch cliphist store")
    hl.exec_cmd("wl-paste --type image --watch cliphist store")
    hl.exec_cmd("hyprctl setcursor Bibata-Modern-Classic 24")
end)

local scripts = "$HOME/.config/hypr/scripts"
hl.bind("SUPER + Return", hl.dsp.exec_cmd("kitty"))
hl.bind("SUPER + Q", hl.dsp.window.close())
hl.bind("SUPER + SHIFT + E", hl.dsp.exit())
hl.bind("SUPER + F", hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" }))
hl.bind("SUPER + Space", hl.dsp.window.float({ action = "toggle" }))
hl.bind("SUPER + G", hl.dsp.exec_cmd("sh " .. scripts .. "/toggle-gaps.sh"))
hl.bind("SUPER + L", hl.dsp.exec_cmd("loginctl lock-session"))
hl.bind("SUPER + S", hl.dsp.exec_cmd("sh " .. scripts .. "/freeze-screenshot.sh"))

local dirs = { Left = "l", Right = "r", Up = "u", Down = "d" }
for key, d in pairs(dirs) do
    hl.bind("SUPER + " .. key, hl.dsp.focus({ direction = d }))
end
for i = 1, 10 do
    local key = tostring(i % 10)
    hl.bind("SUPER + " .. key, hl.dsp.focus({ workspace = i }))
    hl.bind("SUPER + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end
hl.bind("SUPER + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind("SUPER + mouse_up", hl.dsp.focus({ workspace = "e-1" }))
hl.bind("SUPER + bracketright", hl.dsp.focus({ workspace = "e+1" }))
hl.bind("SUPER + bracketleft", hl.dsp.focus({ workspace = "e-1" }))
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Teclas Fn: volume, microfone, brilho e mídia (funcionam com a tela travada)
local osd = "sh " .. scripts .. "/osd.sh "
local fn = { locked = true, repeating = true }
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd(osd .. "volume up"), fn)
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd(osd .. "volume down"), fn)
hl.bind("XF86AudioMute", hl.dsp.exec_cmd(osd .. "volume mute"), { locked = true })
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd(osd .. "mic mute"), { locked = true })
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd(osd .. "brightness up"), fn)
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd(osd .. "brightness down"), fn)
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl pause"), { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true })

-- Menus: telas (SUPER+P), Wi-Fi e Bluetooth também pelo teclado
local wofi = "sh $HOME/.config/wofi/scripts/"
hl.bind("SUPER + P", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "display-menu.sh"))
hl.bind("SUPER + N", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "wifi-menu.sh"))
hl.bind("SUPER + SHIFT + N", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "bluetooth-menu.sh"))
