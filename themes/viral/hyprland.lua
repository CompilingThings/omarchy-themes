local active_border_color = { colors = { "rgba(e8473aff)", "rgba(2eb4c4ff)" }, angle = 45 }
local inactive_border_color = "rgba(151a21cc)"

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

-- A faint red glow around the focused window, like a virus coloured in on the micrograph
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e8473a33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
