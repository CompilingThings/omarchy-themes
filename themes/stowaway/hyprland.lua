local active_border_color = { colors = { "rgba(c060e0ff)", "rgba(e0b030ff)" }, angle = 45 }
local inactive_border_color = "rgba(1a1620cc)"

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

-- A faint violet glow around the focused window, like dark-field light
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(c060e033)",
      color_inactive = "rgba(00000000)",
    },
  },
})
