def topLayer( c ):
    # return top layer index
    return len(c.layers) -1


def aspectRatio(size, maxheight):
    """scale a (w,h) tuple to maxheight."""    
    w, h = size
    if h == maxheight:
        return 1.0
    elif maxheight == 0:
        return 1.0
    else:
        return float(maxheight) / h


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
    s = aspectRatio( (w,h), newheight)
    layer.scale(s, s)
    return layer
