size(1200, 1000)

svg = ximport("svg")

allpaths = []
for name in ("path.svg", "char.svg"):
    with open(name, 'r') as f:
        t = f.read()
        s = svg.parse(t)
        allpaths.append( s )

# print(allpaths)

# Create a copy of the path
# we can manipulate with
# rotate() and scale() etc.
for paths in allpaths:
    points = []
    for pt in paths[0]:
        points.append(pt)
    reset()
    background(0,0.2,0.3)
    for i in range(30):
        fill(1, 1, 1, 0.05)
        stroke(1, 1, 1, 0.1)
        strokewidth(0.5)
        scale(0.93)
        rotate(-i*0.2)
        translate(i,0)
        drawpath(points)
