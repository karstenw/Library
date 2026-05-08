size(1200, 850)
background(0.15, 0.15, 0.7)
colors = ximport("colors")

font("Georgia", 292)
p = textpath("gradient", 50, 500)
g = colors.gradient(color(1, 1, 0.0), color(0.35, 0.35, 0.0))
colors.outline(p, g)
