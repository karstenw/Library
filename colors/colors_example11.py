# SORTING COLOR LISTS

# Import the library
try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

# from the docs

r = colors.range(h=(0.75,0.95))
transform(CORNER)
rotate(45)
for i in range(HEIGHT/10):
    fill(choice(r))
    rect(-WIDTH, i*15, WIDTH*2, 20)

###

reset()

font("Georgia", 58)
p = textpath("gradient text is back!", 10, 350)
g = colors.gradient(color(1,0,0.5), color(0,0.5,1))
 
colors.outline(p, g)

###

reset()
x = 20
y = 20
for shade in colors.shades:
    text(shade.name, x, y-5, fill=0.2, fontsize=12)
    clr = shade(colors.yellow(), n=8)
    clr.swatch(x, y)
    x += 45

###
reset()
#size(550, 275)
# background( sand() )

sand = colors.theme()
sand.add_range("soft ivory", weight=0.5)
sand.add_range("dark goldenrod", weight=0.25)
sand.add_range("warm brown", weight=0.25) 
sand.swatch(2, 2, w=7, h=7, padding=1)

colors.shadow(alpha=0.4, dx=-40, blur=10)

translate(0,500)
 
for clr in sand:
    fill(clr)
    translate(10)
    scale(0.96)
    skew(10)
    rect(0, -40, 400, 400)
