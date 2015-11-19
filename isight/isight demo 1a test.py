
#
# another speed demo
#
# Run this in full screen mode
#


# Import the library
try: 
    # This is the statement you normally use.
    isight = ximport("isight")
except:
    # But since this example is "inside" the library
    # we may need to try something different when
    # the library is not located in /Application Support
    isight = ximport("__init__")
    reload(isight)

import Foundation, AppKit
s = AppKit.NSScreen.mainScreen()
X,Y = s.frame().size

import itertools

size(X, Y)

imagewidth = 200
columns = int( round(X / imagewidth, 0))
intervall = 0.25

# get 1 image for imagesize
calibrationimage = isight.grab()

# get imagesize
imsize = imagesize( calibrationimage )

# get image ratio
ratio = imsize.width / imsize.height

# now that ratio is known we can calculate the number of rows
rows = int(round(Y / (imagewidth / ratio), 0))

imheight = imagewidth / ratio


# grab columns*rows images
imagepaths = isight.grabSequence( count=columns*rows, intervall=intervall )

# set the canvas size
size(imagewidth*columns,  imheight*rows)

background(None)

# make the image path list an iterator
# the list may be shorter
well = itertools.cycle( imagepaths )

for x, y in grid(columns, rows, imagewidth, imheight):
    image(well.next(), x, y, width=imagewidth, height=imheight)
