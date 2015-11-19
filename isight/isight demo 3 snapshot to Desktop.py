
#
# Grab a single image
# store it on the desktop (name: "NdBx-00000.jpg") and display it
#
try: 
    isight = ximport("isight")
except:
    isight = ximport("__init__")
    reload(isight)

import os

destfolder = os.path.expanduser( "~/Desktop" )

imagepath = isight.grab( destfolder=destfolder )

print imagesize(imagepath)
image(imagepath,0,0)
