# SHADER

try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

supershape = ximport("supershape")

# Deep green gradient background.
size(400, 400)
W, H = WIDTH, HEIGHT
W2 = W // 2
H2 = H // 2
R = W * 3 // 8


bg1 = color( 0.15, 0.4, 0.8 )
bg2 = color( 0, 0, 0 )

def setBG( col1, col2):
    bg = rect(0,0,WIDTH,HEIGHT,draw=False)
    colors.gradientfill(bg, col1, col2 )
    colors.shadow()

setBG( bg1, bg2 )


def handler(value, name):
    global x, y, ang, radius
    setBG( bg1, bg2 )
    if name == 'x':
        x = int(round( value ) )
    elif name == 'y':
        y = int(round( value ) )
    elif name == 'ang':
        ang = round( value, 2 )
    elif name == 'radius':
        radius = int(round( value ))
    run(x, y, ang, radius)


def run( x, y, ang, radius ):
    #x = W2
    #y = H2
    if ang == 0:
        ang = None

    # print("RUN (%i, %i), %s, %i" % ( x, y, repr(ang), radius ))
    # A lightsource positioned at the centre of the canvas.
    d = colors.shader(x, y, W2, H2, angle=ang, radius=radius)

    # Ovals become smaller when further away from the light.
    # If they become too small, don't draw them.
    r = d * 40

    clr1 = color(0.4+d*0.5, 0.6+d*0.3, 0, 0.75)
    clr2 = color(0, 0, 0, d)

    p = oval(x, y, r*2, r*2, draw=False)

    # Two colors for an oval gradient fill.
    # The green becomes lighter and more opaque
    # when elements are nearer to the light.
    nostroke()
    colors.gradientpath(p, clr1, clr2, alpha=0.5+d, dx=r, dy=r)






var("x", NUMBER, W2, 0, W, handler=handler)
var("y", NUMBER, H2, 0, H, handler=handler)
var("ang", NUMBER, 0, 0, 360.0, handler=handler)
var("radius", NUMBER, W2//2, 10, max(W,H), handler=handler)
run(x, y, ang, radius)
