def aspectRatio(size, maxsize):
    """scale a (w,h) tuple to maxsize (either w or h."""
    maxcurrent = max(size)
    if maxcurrent == maxsize:
        return size
    elif maxsize == 0:
        return size
    else:
        ratio = maxcurrent / float(maxsize)
        neww = int(round(size[0] / ratio))
        newh = int(round(size[1] / ratio))
        return neww, newh


def label(s,x,y):
    _ctx.push()
    _ctx.fill(1)
    _ctx.text(s, x, y+20)
    _ctx.fill(0)
    _ctx.text(s, x+1, y+21)
    _ctx.pop()


def insetRect( rectangle, horInset, vertInset):
    x, y, w, h = rectangle
    dh = horInset / 2.0
    dv = vertInset / 2.0
    return x+dh, y+dv, w-horInset, h-vertInset


def cropImageToRatioHorizontal( layer, ratio ):
    w, h = layer.bounds()
    neww = int( round( h*ratio) )
    d = int( neww / 2.0 )
    x,y,w,h = insetRect( (0,0,w,h), d, 0 )
    layer.img = layer.img.crop(box=(x,y,x+w,y+h))
    return layer


def scaleLayerToHeight( layer, newheight ):
    # get current image bounds
    w, h = layer.bounds()

    # calculate scale & apply
    w,h = aspectRatio( (w,h), newheight)
    layer.scale(w, h)
    return layer
