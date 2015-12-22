background( 0.5 )

#size(900,200)

try:
    pb = ximport("photobot")
except ImportError:
    pb = ximport("__init__")
    reload(pb)

import os

repeats = 5

canvas = photobot.canvas(WIDTH, HEIGHT)

folder = "/Library/Desktop Pictures/Nature"
if not os.path.exists( folder ):
    folder = "/Library/Desktop Pictures"


rawfiles = [f for f in os.listdir(folder)]

def layerTop( c ):
    # return top layer index
    nlayers = len(c.layers)
    return nlayers -1


tiles = []
for t in rawfiles:
    if os.path.splitext(t)[1].lower() in [".jpg", ".png", ".tif", ".tiff", ".jpeg", ".gif"]:
        path = t
        if not path.startswith('/'):
            path = os.path.abspath(os.path.join(folder, t))
        tiles.append( path )

nextImagePath = choice(tiles)
print "path", repr(nextImagePath)
canvas.layer( nextImagePath )
w, h = canvas.layers[1].bounds()
canvas.layers[1].scale(0.33,0.33)
print "w,h", w,h
destWidth = WIDTH / float(repeats)
print "destWidth", destWidth
sc = 1 / (w / destWidth)
print "scale", sc
# canvas.layers[1].scale(sc, sc)

print "layersSize", layerTop(canvas)
for i in range(repeats):
    # canvas.layers[1].duplicate()
    canvas.layer( nextImagePath )
    # canvas.layers[2+i].scale(sc, sc)

    if random() < 0.8:
        canvas.layers[2+i].scale(sc, sc)
    else:
        sc2 = 1.0 + random() * 3.0
        canvas.layers[2+i].scale(sc*sc*sc2, sc*sc*sc2)

    if random() > 0.5:
        canvas.layers[2+i].sharpen()
    if random() > 0.5:
        canvas.layers[2+i].blur()
    if random() > 0.5:
        canvas.layers[2+i].desaturate()
    if random() > 0.5:
        canvas.layers[2+i].invert()
    r = -15 + random() * 30
    canvas.layers[2+i].rotate(r)
    canvas.layers[2+i].translate(i*int(destWidth*0.8),i*60)
    
canvas.draw(0,0)