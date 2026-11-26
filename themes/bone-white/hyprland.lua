local active_border_color = { colors = { "rgba(e2cfa0ff)", "rgba(b07a3cff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1915cc)"

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

-- A faint ivory glow around the focused window, like a museum spotlight on bone
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e2cfa033)",
      color_inactive = "rgba(00000000)",
    },
  },
})
