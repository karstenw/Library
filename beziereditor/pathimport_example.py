size(1200, 1000)

try:
    svg = ximport("svg")
except ImportError:
    svg = ximport("__init__")
    reload(pb)

paths = svg.parse(open("path.svg").read())

# Create a copy of the path
# we can manipulate with
# rotate() and scale() etc.
points = []
for pt in paths[0]:
    points.append(pt)

background(0,0.2,0.3)
for i in range(70):
    fill(1, 1, 1, 0.05)
    stroke(1, 1, 1, 0.1)
    strokewidth(0.5)
    scale(0.93)
    rotate(-i*0.2)
    translate(i,0)
    drawpath(points)
