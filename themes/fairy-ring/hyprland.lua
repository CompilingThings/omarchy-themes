local active_border_color = { colors = { "rgba(f0563fff)", "rgba(b56ee0ff)" }, angle = 45 }
local inactive_border_color = "rgba(2a201acc)"

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

-- A faint red glow around the focused window, like a fly agaric cap in low forest light
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f0563f40)",
      color_inactive = "rgba(00000000)",
    },
  },
})
