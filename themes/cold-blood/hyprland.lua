local active_border_color = { colors = { "rgba(ee3b3bff)", "rgba(5ac82eff)" }, angle = 45 }
local inactive_border_color = "rgba(1c2416cc)"

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

-- A faint red glow around the focused window, like a tree frog's eye at night
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(ee3b3b33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
