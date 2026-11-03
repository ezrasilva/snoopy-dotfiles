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
-- ---------------------------------------------------------------------------

hl.config({ misc = { disable_hyprland_logo = true } })

hl.env("XDG_SESSION_TYPE", "wayland")
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("GDK_BACKEND", "wayland,x11")

hl.on("hyprland.start", function()
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
    hl.exec_cmd("dunst")
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
for i = 1, 9 do
    hl.bind("SUPER + " .. i, hl.dsp.focus({ workspace = i }))
    hl.bind("SUPER + SHIFT + " .. i, hl.dsp.window.move({ workspace = i }))
end
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
