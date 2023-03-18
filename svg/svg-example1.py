size(900, 900)

mx, my = int(WIDTH / 2), int(HEIGHT / 2)

import pprint
pp=pprint.pprint
import io

try:
    svg = ximport("svg")
except:
    svg = ximport("__init__")
    reload(svg)

# The parse() command will return
# a list of the shapes in the SVG file.
#paths = svg.parse(open("flower.svg").read())
paths = svg.parse(io.open("flower.svg",'r', encoding="utf-8").read(), cached=True)
# pp(paths)
background(color(0.1, 0.1, 0.0))

for i in range(10):
    reset()
    transform(CORNER)
    
    translate(mx + random(-200, 200), my + random(-200, 200))
    scale(random(0.2, 2.6))
    rotate(random(360))

    fill(1, 1, 0.9, 0.1)

    for path in paths:
        # Use copies of the paths
        # that adhere to the transformations 
        # (translate, scale, rotate) we defined.
        drawpath(path.copy())
        
    reset()

# pp(list(svg._cache.keys()))
