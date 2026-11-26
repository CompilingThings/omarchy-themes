local active_border_color = { colors = { "rgba(f4632aff)", "rgba(5cd0d6ff)" }, angle = 45 }
local inactive_border_color = "rgba(1c1612cc)"

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

-- A faint orange glow around the focused window, like a crystal lit between polarisers
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(f4632a33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
