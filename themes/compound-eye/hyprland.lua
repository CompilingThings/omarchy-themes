local active_border_color = { colors = { "rgba(7bdc5eff)", "rgba(5c8effff)" }, angle = 45 }
local inactive_border_color = "rgba(1a1e22cc)"

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

-- A faint green glow around the focused window, like light on a metallic wing case
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(7bdc5e40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
