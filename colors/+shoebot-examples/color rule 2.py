try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

translate(100,100)

clr = colors.rgb(0, 0.4, 0.6)
scheme = colors.left_complement(clr)
scheme.swarm(75, 75)
scheme.swatch(0, 0, w=25, h=25)