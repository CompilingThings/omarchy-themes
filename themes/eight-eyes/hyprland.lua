local active_border_color = { colors = { "rgba(e8a23cff)", "rgba(3cc8d8ff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1712cc)"

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

-- A faint amber glow around the focused window, like light caught in a spider's eyes
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(e8a23c33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
