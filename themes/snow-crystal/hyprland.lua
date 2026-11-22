local active_border_color = { colors = { "rgba(8fd0ffff)", "rgba(f1e8daff)" }, angle = 45 }
local inactive_border_color = "rgba(2a1e1ccc)"

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

-- A faint icy glow around the focused window, like frost on a dark window pane
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(8fd0ff33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
