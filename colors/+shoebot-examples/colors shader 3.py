try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

# Deep green gradient background.
size(400, 400)
W, H = WIDTH, HEIGHT

bg = rect(0, 0, W, H, draw=False)
colors.gradientpath(bg, color(0.15,0.2,0), color(0,0,0))
 
colors.shadow()
for i in range(50):
    x = random(W)
    y = random(H)    

    # A lightsource positioned at the centre of the canvas.
    d = colors.shader(x, y, W//2, H//2, angle=None, radius=150)    

    # Oval become smaller when further away from the light.
    # If they become too small, don't draw them.
    r = d*40

    if r < 4:
        continue

    p = oval(x, y, r*2, r*2, draw=False)    

    # Two colors for an oval gradient fill.
    # The green becomes lighter and more opaque
    # when elements are nearer to the light.
    nostroke()
    clr1 = color(0.4+d*0.5, 0.6+d*0.3, 0, 0.75)
    clr2 = color(0, 0, 0, d)
    colors.gradientpath(p, clr1, clr2, alpha=0.5+d, dx=r, dy=r)


#   add to the script above:
    nofill()
    stroke(clr1)
    strokewidth(0.25)
    autoclosepath(False)
    if d < 0.3:
        for j in range(random(10)):
            v = (1-d) * 150
            beginpath(x, y)
            curveto(x, y, x+random(-v,v), y+random(-v,v), W//2, H//2,)
            endpath()

    
#   add to the script above:
    if 1:
        supershape = ximport("supershape")
        strokewidth(d*0.75)
        if d > 0.25:
            p = supershape.path(x+r, y+r, r, r, 10, 1.5, -0.5, 1.5)
            drawpath(p)

