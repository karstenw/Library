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


imagewidth = 200
columns = 4
rows = 12
intervall = 0.25

import itertools


# Create a grid of columns x rows with each image grabbed from the iSight.
# This will take considerably less time than the previous library.


# grab columns*rows images, 0.1 sec apart i.e. ca 5 seconds
imagepaths = isight.grabSequence( count=columns*rows, intervall=intervall )


# get imagesize from first image
imsize = imagesize( imagepaths[0] )

# get image ratio
ratio = imsize.width / imsize.height

imheight = imagewidth / ratio

# set the canvas size
size(imagewidth*columns,  imheight*rows)

background(None)

# make the image path list an iterator
# the list may be shorter
well = itertools.cycle( imagepaths )

for x, y in grid(columns, rows, imagewidth, imheight):
    image(well.next(), x, y, width=imagewidth, height=imheight)
