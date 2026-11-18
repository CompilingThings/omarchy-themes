local active_border_color = { colors = { "rgba(e07a4fff)", "rgba(8db4dcff)" }, angle = 45 }
local inactive_border_color = "rgba(2a1d18cc)"

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

-- A faint rust glow around the focused window, like dust hanging in the Martian air
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e07a4f40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
