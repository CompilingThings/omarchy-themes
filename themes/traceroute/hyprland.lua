local active_border_color = { colors = { "rgba(ffe14dff)", "rgba(f5c518ff)" }, angle = 45 }
local inactive_border_color = "rgba(1a2a3acc)"

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

-- A soft yellow glow around the focused window
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(ffd84a48)",
      color_inactive = "rgba(00000000)",
    },
  },
})
