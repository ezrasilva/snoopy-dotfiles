-- Tema snoopy-day
local c = require("colors.snoopy-day")
local home = os.getenv("HOME")

hl.exec_cmd("sh " .. home .. "/.config/hypr/scripts/switch-theme.sh snoopy-day")

hl.config({
    general = {
        gaps_in = 8,
        gaps_out = 16,
        border_size = 3,
        col = { active_border = c.red, inactive_border = c.bg5 },
        resize_on_border = true,
        layout = "dwindle",
    },
    decoration = {
        rounding = 14,
        blur = { enabled = false },
        shadow = { enabled = true, range = 0, render_power = 4, color = "rgb(2e2a25)", offset = {0, 8} },
        dim_inactive = false,
    },
    animations = { enabled = true },
    dwindle = { preserve_split = true },
})
hl.curve("bounce", { type = "bezier", points = {{1, 1.6}, {0.1, 0.85}} })
hl.curve("overshot", { type = "bezier", points = {{0.7, 0.6}, {0.1, 1.1}} })
hl.animation({ leaf = "windows", enabled = true, speed = 5, bezier = "bounce", style = "popin" })
hl.animation({ leaf = "fade", enabled = true, speed = 5, bezier = "overshot" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 6, bezier = "overshot", style = "slidevert" })

-- Wofi
local wofi = "sh " .. home .. "/.config/wofi/scripts/"
local css = home .. "/.config/wofi/themes/snoopy-day.css"
hl.bind("SUPER + D", hl.dsp.exec_cmd("pkill wofi || wofi --show drun --term=kitty --width=35% --height=50% --columns 1 -I -s " .. css))
hl.bind("SUPER + SHIFT + B", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "powermenu.sh snoopy-day --height=17%"))
hl.bind("SUPER + C", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "wofi-calc.sh snoopy-day"))
hl.bind("SUPER + V", hl.dsp.exec_cmd("pkill wofi || cliphist list | wofi --dmenu -s " .. css .. " | cliphist decode | wl-copy"))
hl.bind("SUPER + Period", hl.dsp.exec_cmd("pkill wofi || " .. wofi .. "wofi-emoji.sh snoopy-day"))
hl.bind("SUPER + SHIFT + T", hl.dsp.exec_cmd(wofi .. "theme-switcher.sh snoopy-day"))
