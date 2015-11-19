
#
# Grab a sequence of images from the isight
# store it on the desktop in a folder named "iSightSequence"
# and make a collage of it using coreimage
#
#
#
try: 
    isight = ximport("isight")
except:
    isight = ximport("__init__")
    reload(isight)

coreimage = ximport("coreimage")


# needed for path functions
import os

# needed to get screen size
import AppKit
s = AppKit.NSScreen.mainScreen()
X,Y = s.frame().size

size(X, Y)


destfolder = os.path.join( os.path.expanduser( "~" ), "Desktop", "iSightSequence" )

imagepaths = isight.grabSequence( count=30, intervall=0.1, destfolder=destfolder )


# fill( 0.94, 0.91, 0.13)
fill( 0.167, 0.167, 0.167)
rect( 0, 0, WIDTH, HEIGHT )



canv = coreimage.canvas( WIDTH, HEIGHT )

nooffiles = len( imagepaths )

# imagepaths.shuffle()

noofpicts = len( imagepaths )

for pict in imagepaths:
    l = canv.layer( pict )
    if not l:
        print "FAIL:", pict
        continue
    l.scale(0.33)
    lpw, lph = l.size()
    m = l.mask.layer_radial_gradient()

    if lpw>lph:
        m.scale(w=lpw/lph, h=1.0)
    else:
        m.scale(w=1.0, h=lph/lpw)

    r = random( -30, 30)

    l.rotate( r )
    ox, oy = int( lpw / 2 ), int( lph / 2 )
    px = random(ox, WIDTH - ox)
    py = random(oy, HEIGHT - oy)
    l.x, l.y = px, py

canv.draw( 0, 0) #, helper=True )
