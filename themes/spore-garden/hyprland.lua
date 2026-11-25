local active_border_color = { colors = { "rgba(4ed27aff)", "rgba(c064e0ff)" }, angle = 45 }
local inactive_border_color = "rgba(17141ccc)"

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

-- A faint green glow around the focused window, like the threads in the opening picture
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(4ed27a33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
