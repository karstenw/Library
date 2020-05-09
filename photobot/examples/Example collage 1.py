# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
import sys, os

import pprint
pp = pprint.pprint
kwdbg = False

# need a different name
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)


W, H = 1024,768




# import photobot
try:
    pb = ximport("photobot")
    size(W, H)
    background( 0.333 )
except ImportError:
    pb = ximport("__init__")
    reload(pb)
    size(W, H)
    background( 0.333 )
except NameError:
    import photobot as pb
    WIDTH. HEIGHT = W, H
RATIO = WIDTH / HEIGHT

# load the image library
# check for command line folders
additionals = sys.argv[1:]

# get all images from user image wells
imagewell = pb.loadImageWell(   bgsize=(1024,768),
                                minsize=(256,256),
                                pathonly=True,
                                additionals=additionals)

# tiles are images >256x256 and <=1024x768
tiles = imagewell['tiles']

# backgrounds are images >1024x768
backgrounds = imagewell['backgrounds']
rnd.shuffle(tiles)
rnd.shuffle(backgrounds)

print "tiles:", len(tiles)
print "backgrounds:", len(backgrounds)


# CONFIGURATION

# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (85,85,85) )


# CONFIGURATION

columns = 3
rows = 2

randomblur = 1
paintoverlay = 1


# 
y_offset = HEIGHT / (rows)


# 
if 1:
    top = c.layer(backgrounds.pop())
    w, h = c.top.bounds()
    w1,h1 = pb.aspectRatio( (w,h), HEIGHT, height=True, assize=True )
    c.top.scale(w1,h1)

for j in range(rows):
    colw = 0
    for i in range(columns):

        # new layer with a random image
        top = c.layer( tiles.pop() )

        # get current image bounds
        w, h = c.top.bounds()

        # calculate scale & apply
        s = pb.aspectRatio( (w,h), y_offset, height=True)
        c.top.scale(s, s)

        # uniform
        layer = pb.cropImageToRatioHorizontal( c.top, RATIO )

        # add contrast
        c.top.contrast(1.1)

        # get the new image bounds
        w, h = c.top.bounds()

        r = 0.4 
        r = rnd.random()
        # 10%
        if r < 0.1:
            # create a dual ramp gradient
            _ = c.gradient(pb.LINEAR, w/2, h)
            c.top.flip( pb.HORIZONTAL )

            # layer translate half a pict right
            c.top.translate(w/2, j*y_offset)

            # create another gradient layer and merge with first gradient
            top = c.gradient(pb.LINEAR, w/2, h)
            # merge both gradients; destroys top layer
            c.merge([ top-1 , top ])
        elif 0.1 <= r < 0.5:
            #print "SINE"
            top = c.gradient(pb.SINE, w, h)
            
        elif 0.6 <= r < 0.75:
            #print "RADIALCOSINE"
            top = c.gradient(pb.RADIALCOSINE, w, h)
            c.top.invert()
        else:
            #print "ROUNDRECT"
            # 25%
            top = c.gradient(pb.ROUNDRECT, w, h, radius=int(w/5.0))

        c.top.brightness(1.4)

        # mask destroys top layer
        c.top.mask()

        c.top.translate(colw+i*w, j*y_offset)

        if randomblur:
            if rnd.random() > 0.5:
                c.top.flip()

            if rnd.random() > 0.5:
                c.top.blur()

if 1:
    # orange hue mask finish
    top = c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()

if paintoverlay:
    # paint overlay
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.top.bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.top.scale(s, s)
    c.top.opacity(10)
    c.top.overlay()

c.draw(0, 0)
