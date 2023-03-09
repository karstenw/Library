size(1200, 1000)

try:
    svg = ximport("svg")
except ImportError:
    svg = ximport("__init__")
    reload(pb)

allpaths = []
try:
    allpaths.append( svg.parse(open("path.svg").read()) )
    allpaths.append( svg.parse(open("char.svg").read()) )
except:
    pass

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
