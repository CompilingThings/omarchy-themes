local active_border_color = { colors = { "rgba(4fc1daff)", "rgba(e0a050ff)" }, angle = 45 }
local inactive_border_color = "rgba(182028cc)"

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

-- A faint teal glow around the focused window, like dark-field light round a water flea
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(4fc1da33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
