local active_border_color = { colors = { "rgba(a6e61eff)", "rgba(eab01eff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1b12cc)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
})

-- A faint green glow around the focused window, like a glowing compound eye
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(a6e61e33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
