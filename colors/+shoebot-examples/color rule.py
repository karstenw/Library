try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

clr = colors.rgb(0.0, 0.4, 0.6)
x = 10
for name in colors.rules:
    scheme = colors.rule(name, clr)
    scheme.swatch(x, 10)
    x += 40

