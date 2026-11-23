local active_border_color = { colors = { "rgba(29c8eeff)", "rgba(e1dd18ff)" }, angle = 45 }
local inactive_border_color = "rgba(121c20cc)"

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

-- A faint cyan glow around the focused window, like a water flea lit on black
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(29c8ee33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
