local active_border_color = { colors = { "rgba(eca01eff)", "rgba(4fd6d4ff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1914cc)"

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

-- A faint gold glow around the focused window, like a vein lit between crossed polarisers
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(eca01e33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
