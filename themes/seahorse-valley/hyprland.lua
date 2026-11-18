local active_border_color = { colors = { "rgba(7aa2f7ff)", "rgba(bb9af7ff)" }, angle = 45 }
local inactive_border_color = "rgba(24283bcc)"

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

-- A faint Tokyo Night blue glow around the focused window, like the halo around the set in the pictures
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(7aa2f740)",
      color_inactive = "rgba(00000000)",
    },
  },
})
