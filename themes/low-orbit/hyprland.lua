local active_border_color = { colors = { "rgba(4fc9c4ff)", "rgba(f2c063ff)" }, angle = 45 }
local inactive_border_color = "rgba(16292ecc)"

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

-- A faint cyan glow around the focused window, like the thin line of air along Earth's edge seen from orbit
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(4fc9c440)",
      color_inactive = "rgba(00000000)",
    },
  },
})
