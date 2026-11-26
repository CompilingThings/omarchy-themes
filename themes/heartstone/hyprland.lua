local active_border_color = { colors = { "rgba(e8509aff)", "rgba(f0862aff)" }, angle = 45 }
local inactive_border_color = "rgba(1c161ccc)"

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

-- A faint pink glow around the focused window, like the coloured electron image
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e8509a33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
