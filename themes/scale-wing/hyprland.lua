local active_border_color = { colors = { "rgba(4fa0e8ff)", "rgba(f0962aff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1813cc)"

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

-- A faint blue glow around the focused window, like a shimmer on the scales
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(4fa0e833)",
      color_inactive = "rgba(00000000)",
    },
  },
})
