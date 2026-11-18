local active_border_color = { colors = { "rgba(4fc1d1ff)", "rgba(d6aa6aff)" }, angle = 45 }
local inactive_border_color = "rgba(1a2a2ecc)"

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

-- A faint teal glow around the focused window, like Neptune's blue seen from far away
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(4fc1d140)",
      color_inactive = "rgba(00000000)",
    },
  },
})
