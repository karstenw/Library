from math import sin, cos
try:
    supershape = ximport("supershape")
except:
    supershape = ximport("__init__")
    reload(supershape)

size(1200, 1200)

x, y = 200, 200
w, h = 43, 50
m = 6.0
n1 = 1.0
n2 = 1.0
n3 = 1.0
i = 0.0

stroke(0)
strokewidth(1)
nofill()

m = 1
for x,y in grid(3, 4, 200, 200):
    push()
    reset()
    translate(100,100)
    n1 = 5.0 + sin(m*2)
    n2 = 10 + cos(i) * 10
    n3 = sin(m*3) * 10
    i += 0.05
    
    #rotate(i*10)
    p = supershape.path(x, y, w, h, m, n1, n2, n3)
    drawpath(p)
    m += 1
    
    pop()