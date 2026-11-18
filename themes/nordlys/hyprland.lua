local active_border_color = { colors = { "rgba(57e39bff)", "rgba(b18cffff)" }, angle = 45 }
local inactive_border_color = "rgba(16222ccc)"

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

-- A faint green glow around the focused window, like snow lit by the aurora
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(57e39b40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
