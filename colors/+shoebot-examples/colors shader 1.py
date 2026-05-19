try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)


size(550, 300)
W, H = WIDTH, HEIGHT



background(0.1,0,0.05)
colormode(HSB)
colors.shadow()
for i in range(3000):
    x = random(W)
    y = random(H)
    r = random(10,30)
    d = colors.shader(x, y, W, H, angle=150)

    # HSB is brighter and opaque in the centre of the light.
    fill(0.84+d*0.1, 1, 0.2+0.8*d, d)
    oval(x, y, r, r)
