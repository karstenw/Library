try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    reload(colors)

# translate(100,100)

size(1500, 1500)

clr1 = colors.rgb(0.6, 0.8, 1.0)
clr2 = colors.rgb(0.0, 0.2, 0.4)
g = colors.gradient(clr1, clr2, steps=60)

for i in range(len(g)):
    fill(g[i])
    r = 700-i*10
    oval(-75+i*5, -180+i*5, r, r)
    # oval(i*5, i*5, r, r)

 
g.steps = 200
g = g.reverse()
 
colors.shadow(blur=12, alpha=0.3)
transform(CORNER)
translate(600,600) #(WIDTH/2, HEIGHT/2)
for i in range(len(g)):
    fill(g[i])
    rotate(3)
    oval(i*0.5, i*0.5, 200-i, 200-i)