local active_border_color = { colors = { "rgba(f072e0ff)", "rgba(e6d53aff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1826cc)"

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

-- A faint magenta glow around the focused window, like light through a crystal
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f072e033)",
      color_inactive = "rgba(00000000)",
    },
  },
})
