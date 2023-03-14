
pb = ximport("photobot")

import random as rnd
rnd.seed( 123456 )

import imagewells
loadImageWell = imagewells.loadImageWell

rangesize = 600
rangemin, rangemax = -int(rangesize/3), int(rangesize/3)
size( rangesize, rangesize )
imagewell = loadImageWell(   bgsize=(rangesize, rangesize),
                             minsize=(256,256),
                             pathonly=False,
                             imagewellfilename="imagewell.txt",
                             tabfilename="imagewell.tab",
                             ignoreDotFolders=True,
                             ignoreFolderNames=('+offline',))


imagerecord = choice(imagewell['backgrounds'])
print(imagerecord)
imgpath, _, _, _, _, imagewidth, imageheight, _,frac = imagerecord
print("imgpath:", imgpath)
print(frac)

def handler( value, name ):
    global x0,y0, x1,y1, x2,y2, x3,y3
    if name == 'x0':
        x0 = int(value)
        print("x0:", x0)
    elif name == 'y0':
        y0 = int(value)
        print("y0:", y0)
    elif name == 'x1':
        x1 = int(value)
        print("x1:", x1)
    elif name == 'y1':
        y1 = int(value)
        print("y1:", y1)
    elif name == 'x2':
        x2 = int(value)
        print("x2:", x2)
    elif name == 'y2':
        y2 = int(value)
        print("y2:", y2)
    elif name == 'x3':
        x3 = int(value)
        print("x3:", x3)
    elif name == 'y3':
        y3 = int(value)
        print("y3:", y3)
    paint()


var("x0", NUMBER, 0, rangemin, rangemax, handler=handler)
var("y0", NUMBER, 0, rangemin, rangemax, handler=handler)
var("x1", NUMBER, 0, rangemin, rangemax, handler=handler)
var("y1", NUMBER, 0, rangemin, rangemax, handler=handler)
var("x2", NUMBER, 0, rangemin, rangemax, handler=handler)
var("y2", NUMBER, 0, rangemin, rangemax, handler=handler)
var("x3", NUMBER, 0, rangemin, rangemax, handler=handler)
var("y3", NUMBER, 0, rangemin, rangemax, handler=handler)


def paint():
    global y2
    c = pb.canvas(rangesize, rangesize)

    pb.placeImage(c, imgpath, 0, 0, maxsize=rangesize)
    c.top.opacity(60)

    t,w,h = pb.placeImage(c, imgpath, 0, 0, maxsize= rangesize)
    c.top.opacity(60)
    c.top.distort( x0,y0, x1,y1, x2,y2, x3,y3 )
    c.draw()

paint()
