local active_border_color = { colors = { "rgba(ffc45cff)", "rgba(e8452cff)" }, angle = 45 }
local inactive_border_color = "rgba(2a1a12cc)"

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

-- A faint orange glow around the focused window, like the Sun's edge
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(ff8a3d40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
