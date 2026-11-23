local active_border_color = { colors = { "rgba(e8c22eff)", "rgba(3cc87eff)" }, angle = 45 }
local inactive_border_color = "rgba(171a12cc)"

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

-- A faint gold glow around the focused window, like a stem slice under the blue lamp
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e8c22e33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
