size( 800, 800)
# The Twisted World example,
# with random images from MorgueFile
# http://nodebox.net/code/index.php/Twisted_world

# Import the Core Image library
try: 
    coreimage = ximport("coreimage")
except:
    print "IMPORT MISSED!"
    coreimage = ximport("__init__")
    reload(coreimage)

from random import shuffle

# get all images from system "Desktop Pictures" folder
filetuples = imagefiles( "/Library/Desktop Pictures", False )

# filter out all 1 pix one color images by ignoring all files < 100k
tiles = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 100000:
        continue
    tiles.append( path )

shuffle(tiles)

# Draw a dark grey background
fill(0.334)
rect(0,0,WIDTH,HEIGHT)

# Create a 800x500 canvas to hold layers.
canvas = coreimage.canvas(WIDTH,HEIGHT)

# Create 20 random layers.
# Remember, it may take a few seconds to load
# all the images during the first run.
for i in range(20):
    img = tiles.pop()
    l = canvas.append(img)
    
    # Give each layer a gradient mask.
    l.mask.gradient(type="radial")
    
    # Put it at a random location on the canvas.
    l.x = random(canvas.w)
    l.y = random(canvas.h)
    
    # Maybe flip it,
    # some random rotation and scaling.
    l.flip(horizontal=choice((True,False)))
    l.rotate(random(360))
    l.scale(random(0.05, 0.33))
    
    # Randomly apply kaleidoscopic, twirl and bump effects.
    if random() > 0.75:
        l.filter("kaleidoscope")
    if random() > 0.25:
        l.filter("twirl")
    if random() > 0.25:
        l.filter("bumpdistortion")

# Put a central image on top of the mess.
#img = choice(files("images/"+ query+"/*"))
#l = canvas.layer(img)
#l.mask.layer_radial_gradient()

# Add a fill color that hues
# all the layers below.
l = canvas.append(color(random(), random(), random()))
l.blend(50)
l.blend_hue()

# Put all the layers as a group in a second canvas, 
# then adjust the contrast of the group.
c2 = coreimage.canvas(WIDTH,HEIGHT)
l = c2.append(canvas)
l.contrast = 1.1

# Draw to NodeBox!
c2.draw()
