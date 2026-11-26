local active_border_color = { colors = { "rgba(5c8cf0ff)", "rgba(d0583cff)" }, angle = 45 }
local inactive_border_color = "rgba(161a24cc)"

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

-- A faint blue glow around the focused window, like light through the eyepiece
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(5c8cf033)",
      color_inactive = "rgba(00000000)",
    },
  },
})
