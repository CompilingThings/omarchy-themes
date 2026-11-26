local active_border_color = { colors = { "rgba(b86bf2ff)", "rgba(e8b84aff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1424cc)"

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

-- A faint violet glow around the focused window, like light through a polariser
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(b86bf233)",
      color_inactive = "rgba(00000000)",
    },
  },
})
