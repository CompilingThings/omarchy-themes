local active_border_color = { colors = { "rgba(7a8cf0ff)", "rgba(9cc83aff)" }, angle = 45 }
local inactive_border_color = "rgba(17182acc)"

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

-- A faint violet glow around the focused window, like light through a glass shell
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(7a8cf033)",
      color_inactive = "rgba(00000000)",
    },
  },
})
