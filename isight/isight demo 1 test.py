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

# the width of the used images
imagewidth = 400

# the height will be determined later when we see, what the camera delivers

# the grod size
columns = 2
rows = 6

# image time intervall
intervall = 0.25

# needed to feed the list of paths to the grid
import itertools


# Create a grid of columns x rows with each image grabbed from the iSight.
# This will take considerably less time than the previous library.


# grab columns*rows images, intervall sec apart
imagepaths = isight.grabSequence( count=columns*rows, intervall=intervall )

# get imagesize from first image
imsize = imagesize( imagepaths[0] )

# get image ratio
ratio = imsize.width / imsize.height

# now we know how high the delivered image will be
imheight = imagewidth / ratio

# set the canvas size
size(imagewidth*columns,  imheight*rows)

background(None)

# make the image path list an iterator
# the list may be shorter
well = itertools.cycle( imagepaths )

for x, y in grid(columns, rows, imagewidth, imheight):
    image(well.next(), x, y, width=imagewidth, height=imheight)
