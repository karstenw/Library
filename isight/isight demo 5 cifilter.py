#
# Grab a single isight image run a CIFilter and display it
# 
# Set the canvas size to the image size
#
# frame rate is about 1/3

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

coreimage = ximport("coreimage")

imagepath = isight.grab()
imsize = imagesize(imagepath)
w,h = imsize.width, imsize.height

size(w,h)

canvas = coreimage.canvas(w, h)

l = canvas.layer(imagepath)
l.filter_bumpdistortion(radius=h/3.0, scale=0.85, dx=0, dy=0)
# l.filter_triangletile(angle=17.43, width=84)
canvas.draw()