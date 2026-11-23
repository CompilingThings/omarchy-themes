local active_border_color = { colors = { "rgba(f05ab4ff)", "rgba(2fd6a8ff)" }, angle = 45 }
local inactive_border_color = "rgba(1a161ecc)"

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

-- A faint pink glow around the focused window, like a stained cell under the laser
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f05ab433)",
      color_inactive = "rgba(00000000)",
    },
  },
})
