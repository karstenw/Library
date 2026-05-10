### ImageWells

#### What does it do?


It creates a text database of an image folder definition.

A file "imagewell.txt" when run through imagewells.loadImageWell() produces a textfile "imagewell.tab". Once created this file allows very fast access to a collection of images.

#### Scanning your images with ImageWells ####

The collage examples in the ```photobot``` library make use of the ```imagewells``` library and serve as examples for imagewells.

Abbreviated example from the ```photobot``` examples "Example collage 1.py"

```Python

import imagewells
loadImageWell = imagewells.loadImageWell


loadImageWell(  bgsize=(1280,1024),
                minsize=(256,256),
                maxfilesize=100*1024*1024,
                maxpixellength=8192,
                pathonly=True,
                additionals=None,
                ignorelibs=False,
                imagewellfilename="imagewell.txt",
                tabfilename=True,
                ignoreDotFolders=True,
                ignoreFolderNames=None):

```


After a script uses `loadImageWell()` for the first time there should be a file `imagewell.txt` in the same folder as the script excuting.


#### The file `imagewell.txt` looks like this: ####

```
/Library/Desktop Pictures
C:\Windows\Web
/usr/share/backgrounds
/usr/share/wallpapers
```
Each line represents a path for a platform. The file is NL terminated and UTF-8 encoded.

The first line is the "Desktop Pictures" folder on macos.

Line 2 is for windows.

Lines 3+4 are for linux.

If a folder does not exist, it will be ignored. The idea is to put your own image folders into that file. The not so obvious idea is to have different imagewell-THEMENAME.txt files to manage different collections of images.



#### The parameters for loadImageWell are as follows: ####

- bgsize=(w,h) - a tuple marking the size at which a image is designated 'background'. Usually the canvas size. This is for sorting purposes only.

- minsize=(w,h) - at least width>=w or height>=h for a image to be considered. If both are smaller, the image is ignored.

- pathonly=True|False - if False, a tuple with: (path, filesize, lastmodified, mode, islink, w0, h0, proportion, frac) is returned.

- addtionals=('folder',) - a list of folders to be added. If this is active, no caching is used.

- imagewellfilename="imagewell.txt" - the name of the folderlist file to be read.

- tabfilename="imagewell.tab" - the name of the resulting cache file.

- ignoreDotFolders=False - ignore folders starting with a '.'.  This is for MacOS '.thumbnails' folders which you usually want to ignore

- ignoreFolderNames=('folder',) - a list of folder names. If a scanned folder STARTS with a name from that list, it will be ignored.


#### The resulting dictionary contains the following keys: ####


- allimages - a list of all images

- tiles - a list of images with: minsize <= image <= bgsize

- backgrounds - a list of images considered backgrounds i.e. image > bgsize

- landscape - a list of images where WIDTH >= HEIGHT

- portrait - a list of images where WIDTH < HEIGHT

- fractions - dictionary with all the fractions as keys. A fraction key looks like: '1024:575', '4:3' or '16:9'. 

- 'WxH largest', 'WxH smallest' and 'WxH median': accumulated sizes

	- 'WxH largest': (8003, 5622),
	- 'WxH median': (1074.9886462882096, 754.4748180494905),
	- 'WxH smallest': (566, 167),

The items of each image list key will depend on the `pathonly` parameter.


### Examples ###

See "examples/Example collage *.py"

![](../photobot/examples/demo-images/photobot_2021-06-10_144446.png?raw=True)

![](../photobot/examples/demo-images/photobot_2021-06-10_144727.png?raw=True)

![](../photobot/examples/demo-images/photobot_2021-06-10_144808.png?raw=True)


See "examples/Layer\_function\_*.py"

![](../photobot/examples/demo-images/Layer_function_add_modulo.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_add.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_autocontrast.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_boxblur.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_brightness.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_color.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_contour.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_contrast.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_difference.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_emboss.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_enhance_more.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_enhance.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_find_edges.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_flip.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_hue.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_mask.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_multiply.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_opacity.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_overlay.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_posterize.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_screen.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_select.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_solarize.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_subtract_modulo.png?raw=True)

![](../photobot/examples/demo-images/Layer_function_subtract.png?raw=True)

