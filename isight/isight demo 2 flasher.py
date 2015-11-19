#
# Grab a single isight image and display it
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

speed(5)

w = 640
h = 480

def setup():
    global w,h
    imagepath = isight.grab()
    imsize = imagesize(imagepath)
    w,h = imsize.width, imsize.height
    size(w,h)
    image(imagepath,0,0,width=w,height=h)

def draw():
    imagepath = isight.grab()
    imsize = imagesize(imagepath)
    w,h = imsize.width, imsize.height
    image(imagepath,0,0,width=w,height=h)
