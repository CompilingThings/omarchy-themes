local active_border_color = { colors = { "rgba(a98bffff)", "rgba(5fa8ffff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1930cc)"

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

-- A faint violet glow around the focused window, like a sky lit by lightning
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(a98bff33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
