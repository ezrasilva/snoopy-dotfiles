-- Snoopy sobre o illogical-impulse: bordas/gaps estilo tirinha + atalho Day/Night.
-- Carregado por custom/general.lua (que vem depois dos padrões do ii, então sobrescreve).
hl.config({
    general = {
        gaps_in = 6,
        gaps_out = 10,
        border_size = 3,
        col = { active_border = "rgb(c8423a)", inactive_border = "rgba(26323a55)" },
    },
    decoration = {
        rounding = 16,
        shadow = { enabled = true, range = 0, render_power = 4, color = "rgba(26323a99)", offset = {0, 6} },
    },
})

-- SUPER+ALT+T alterna Snoopy Day / Night (SUPER+SHIFT+T já é tradução de tela no ii)
hl.bind("SUPER + ALT + T", hl.dsp.exec_cmd("$HOME/.config/hypr/custom/scripts/snoopy-theme.sh toggle"),
    { description = "Snoopy: Day/Night" })
