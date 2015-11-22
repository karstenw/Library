## isight module ##

This module has been rewritten to use the newer [imagesnap](http://iharder.net/imagesnap) tool.



### grab ###

```grab(destfolder=False)```

Grabs a single image and returns the path to the file.

Unlike the previous version, you cannot define the size of the image.
``ìmagesnap``` always returns an image with the camera native size.

The usage pattern is:

```python

# grab one image to determine the cameras image size
imagepath = isight.grab()
imsize = imagesize(imagepath)
w,h = imsize.width, imsize.height

size(w,h)
image(imagepath,0,0,width=w,height=h)
```




```grabSequence(count=10, intervall=0.1, destfolder=False)```

Grab a sequence of images.

count: nr of images to read

intervall: time between shots

destfolder: the destination folder. If False, the folder ```~/Pictures/Nodebox-iSight-Sequences```will be used.

ATTENTION: The destination folder will grow with each run. Images are not deleted.