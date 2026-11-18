local active_border_color = { colors = { "rgba(f38bbfff)", "rgba(f5b95fff)" }, angle = 45 }
local inactive_border_color = "rgba(221a2ecc)"

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

-- A faint rose glow around the focused window, like hydrogen lit by a hot young star
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f38bbf40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
