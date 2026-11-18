local active_border_color = { colors = { "rgba(f5d46bff)", "rgba(d9a830ff)" }, angle = 45 }
local inactive_border_color = "rgba(2c1844cc)"

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

-- A soft gold glow around the focused window
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f0c84a48)",
      color_inactive = "rgba(00000000)",
    },
  },
})
