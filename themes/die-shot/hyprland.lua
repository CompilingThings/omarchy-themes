local active_border_color = { colors = { "rgba(eab44eff)", "rgba(7ccfc8ff)" }, angle = 45 }
local inactive_border_color = "rgba(15191acc)"

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

-- A faint gold glow around the focused window, like a bond pad under the microscope lamp
hl.config({
  decoration = {
    shadow = {
      enabled = true,
      range = 20,
      render_power = 2,
      offset = { 0, 0 },
      color = "rgba(eab44e33)",
      color_inactive = "rgba(00000000)",
    },
  },
})
