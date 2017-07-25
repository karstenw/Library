# PhotoBot 0.8 beta - last updated for NodeBox 1rc4 
# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Manual: http://nodebox.net/code/index.php/PhotoBot
# Copyright (c) 2006 by Tom De Smedt.
# Refer to the "Use" section on http://nodebox.net/code/index.php/Use


import sys
import os
import types
FloatType = types.FloatType
StringType = types.StringType


import math
sqrt = math.sqrt
pow = math.pow
sin = math.sin
cos = math.cos
degrees = math.degrees
radians = math.radians
asin = math.asin

import datetime
import time
import hashlib

import colorsys

import pdb
import pprint
pp = pprint.pprint

import PIL
import PIL.ImageFilter as ImageFilter
import PIL.Image as Image
import PIL.ImageChops as ImageChops
import PIL.ImageEnhance as ImageEnhance
import PIL.ImageOps as ImageOps
import PIL.ImageDraw as ImageDraw
import PIL.ImageStat as ImageStat

# PIL interpolation modes
NEAREST = Image.NEAREST
BICUBIC = Image.BICUBIC
BILINEAR = Image.BILINEAR
LANCZOS = Image.LANCZOS
INTERPOLATION = Image.BICUBIC

LAYERS = []

# blend modes
NORMAL = "normal"
MULTIPLY = "multiply"
SCREEN = "screen"
OVERLAY = "overlay"
HUE = "hue"
COLOR = "color"

HORIZONTAL = 1
VERTICAL = 2

SOLID = "solid"
LINEAR = "linear"
RADIAL = "radial"
DIAMOND = "diamond"
COSINE = "cosine"
SINE = "sine"
ROUNDRECT = "roundrect"
RADIALCOSINE = "radialcosine"
QUAD = "quad"


def hashFromString( s ):
    h = hashlib.sha1()
    h.update( s )
    return h.hexdigest()

def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
    """Make an ISO datestring. The defaults are good for using the result of
    'datestring()' in a filename.
    """
    if not dt:
        now = str(datetime.datetime.now())
    else:
        now = str(dt)
    if not dateonly:
        now = now[:19]
    else:
        now = now[:10]
    if nospaces:
        now = now.replace(" ", "_")
    if nocolons:
        now = now.replace(":", "")
    return now


def invertimage( img ):
    alpha = img.split()[3]
    img = img.convert("RGB")
    img = ImageOps.invert(img)
    img = img.convert("RGBA")
    img.putalpha(alpha)
    return img


class Canvas:
    
    """Implements a canvas with layers.
    
    A canvas is an empty Photoshop document,
    where layers can be placed and manipulated.
    """

    def __init__(self, w, h):
        
        """Creates a new canvas.

        Creates the working area on which to blend layers.
        The canvas background is transparent,
        but a background color could be set using the fill() function.
        """
        
        self.interpolation = INTERPOLATION
        self.layers = Layers()
        self.w = w
        self.h = h
        
        img = Image.new("RGBA", (w,h), (255,255,255,0))
        self.layer(img, name="_bg")


    def layer(self, img, x=0, y=0, name=""):

        """Creates a new layer from file, Layer, PIL Image.

        If img is an image file or PIL Image object,
        Creates a new layer with the given image file.
        The image is positioned on the canvas at x, y.
        
        If img is a Layer,
        uses that layer's x and y position and name.
        """

        if isinstance(img, Image.Image):
            img = img.convert("RGBA")
            self.layers.append(Layer(self, img, x, y, name))
            return len(self.layers)-1

        if isinstance(img, Layer):
            img.canvas = self
            self.layers.append(img)
            return len(self.layers) - 1

        if type(img) in (str, unicode): 
            img = Image.open(img)
            img = img.convert("RGBA")
            self.layers.append(Layer(self, img, x, y, name))
            return len(self.layers)-1


    def fill(self, rgb, x=0, y=0, w=None, h=None, name=""):

        """Creates a new fill layer.

        Creates a new layer filled with the given rgb color.
        For example, fill((255,0,0)) creates a red fill.
        The layers fills the entire canvas by default.
        """ 

        if w == None:
            w = self.w - x
        if h == None:
            h = self.h - y
        img = Image.new("RGBA", (w,h), rgb)
        return self.layer(img, x, y, name)


    def makegradientimage(self, style, w, h):
        """Creates the actual gradient image.
        
        This has been factored out of gradient() so complex gradients like ROUNDRECT
        which consist of multiple images can be composed.
        """
        w0 = self.w 
        h0 = self.h
        if type(w) == FloatType:
            w *= w0
        if type(h) == FloatType:
            h *= h0
        
        if style not in (RADIALCOSINE,):
            img = Image.new("L", (int(w),int(h)), 255)
        else:
            img = Image.new("L", (int(w),int(h)), 0)
        draw = ImageDraw.Draw(img)

        if style == SOLID:
            draw.rectangle((0, 0, w, h), fill=255)

        if style == LINEAR:
            for i in range(int(w)):
                k = 255.0 * i/w
                draw.rectangle((i, 0, i, h), fill=int(k))
            
        if style == RADIAL:
            r = min(w,h)/2
            for i in range(int(r)):
                k = 255 - 255.0 * i/r
                draw.ellipse((w/2-r+i, h/2-r+i,
                              w/2+r-i, h/2+r-i), fill=int(k))
            
        if style == RADIALCOSINE:
            r = max(w,h) / 2.0
            rx = w / 2.0
            ry = h / 2.0
            
            deg = 90
            base = 90 - deg
            deltaxdeg = deg / rx
            deltaydeg = deg / ry
            deltadeg = deg / r
            #print "RADIALCOSINE w, h, r", w, h, r
            #print "RADIALCOSINE steps xy:", deltaxdeg, deltaydeg
            
            step = min(deltaxdeg, deltaydeg)
            for i in range(int(r)):
                # k = 255.0 * i/r
                k = 256 * sin( radians( base + i * deltadeg ) )
                ix = i * (rx / r)
                iy = i * (ry / r)
                draw.ellipse((0 + ix, 0 + iy,
                              w - ix, h - iy), fill=int(k))

        if style == DIAMOND:
            r = max(w,h)
            for i in range(int(r)):
                x = int(i*w/r*0.5)
                y = int(i*h/r*0.5)
                k = 255.0 * i/r
                draw.rectangle((x, y, w-x, h-y), outline=int(k))
        
        if style in (SINE, COSINE):
            # sin/cos 0...180 left to right
            action = sin
            deg = 180.0
            base = 0
            if style == COSINE:
                action = cos
                deg = 90.0
                base = 90.0 - deg
            deltadeg = deg / w
            for i in range( int(w) ):
                k = 256 * action( radians( base + i * deltadeg ) )
                # draw.rectangle((i, 0, i, h), fill=int(k))
                draw.line( (i,0,i, h), fill=int(k), width=1)

        result = img.convert("RGBA")
        del img
        del draw
        return result


    def gradient(self, style=LINEAR, w=1.0, h=1.0, name="", radius=0, radius2=0):

        """Creates a gradient layer.

        Creates a gradient layer, that is usually used together
        with the mask() function.

        All the image functions work on gradients, so they can
        easily be flipped, rotated, scaled, inverted, made brighter
        or darker, ...

        Styles for gradients are LINEAR, RADIAL, DIAMOND, SINE,
        COSINE and ROUNDRECT
        """

        w0 = self.w
        h0 = self.h
        if type(w) == FloatType:
            w = int(w*w0)
        if type(h) == FloatType:
            h = int(h*h0)

        img = None
        if style in (SOLID, LINEAR, RADIAL, DIAMOND, SINE, COSINE, RADIALCOSINE):
            img = self.makegradientimage(style, w, h)
            img = img.convert("RGBA")
            return self.layer(img, 0, 0, name=name)

        if style == QUAD:
            # make a rectangle with softened edges
            result = Image.new("L", (int(w),int(h)), 255)
            
            # 
            mask = Image.new("L", (w,h), 255)
            draw = ImageDraw.Draw(mask)

            if radius == 0 and radius2 == 0:
                radius = w / 4.0
                radius2 = w / 10.0

            r1 = int(round(radius,0))
            r2 = int(round(radius2,0))
            
            if r1 == 0:
                r1 = 1
            if r2 == 0:
                r2 = 1
            d1 = 2 * r1
            d2 = 2 * r2

            # create the base rect
            baserect = self.makegradientimage(SOLID, w-d1, h-d2)
            
            # create the vertical gradients
            verleft = self.makegradientimage(COSINE, r1, h)
            verleft = verleft.transpose(Image.FLIP_LEFT_RIGHT)
            vertright = verleft.rotate( 180 )

            # create the horizontal gradients
            # since LINEAR goes from left to right, 
            horup = self.makegradientimage(COSINE, r2, w)
            horup = horup.transpose(Image.FLIP_LEFT_RIGHT)
            hordown = horup.rotate( -90, expand=1 )
            horup = hordown.rotate( 180 )

            # assemble
            result.paste( baserect, box=( r1,     0) )
            result.paste( verleft,  box=( 0,      0) )
            result.paste( vertright,box=( w-r1,   0) )

            mask.paste( hordown,  box=( 0,     0) )
            mask.paste( horup,    box=( 0,     h-r2) )

            result = ImageChops.darker(result, mask)
            result = result.convert("RGBA")
            del mask
            del horup
            del hordown
            del baserect
            del verleft
            del vertright
            return self.layer(result, 0, 0, name=name)

        if style == ROUNDRECT:
            result = Image.new("L", (int(w),int(h)), 255)
            r1 = int(round(radius))
            r2 = int(round(radius2))
            if r1==0: r1=1
            if r2==0: r2=1
            d1 = 2 * r1
            d2 = 2 * r2

            # take 1 radial grad for the 4 corners
            corners = self.makegradientimage(RADIALCOSINE, d1, d2)
            # corners = invertimage( corners )

            # top left
            b = corners.copy()
            tl = b.crop( box=(0,0,r1,r2) )

            # top right
            b = corners.copy()
            tr = b.crop( box=(r1,0,d1,r2) )

            # bottom left
            b = corners.copy()
            bl = b.crop( box=(0,r2,r1,d2) )

            # bottom right
            b = corners.copy()
            br = b.crop( box=(r1,r2,d1,d2) )

            # create the base rect
            brw = w - d1
            brh = h - d2
            baserect = self.makegradientimage(SOLID, brw, brh)
            
            # create the vertical gradients
            verleft = self.makegradientimage(COSINE, r1, brh)
            verleft = verleft.transpose(Image.FLIP_LEFT_RIGHT)
            vertright = verleft.rotate( 180 )

            # create the horizontal gradients
            # since LINEAR goes from left to right, 
            horup = self.makegradientimage(COSINE, r2, brw)
            horup = horup.transpose(Image.FLIP_LEFT_RIGHT)
            hordown = horup.rotate( -90, expand=1 )
            horup = hordown.rotate( 180 )

            # assemble
            result.paste( baserect, box=( r1,     r2) )

            result.paste( hordown,    box=( r1,     0) )
            result.paste( horup,  box=( r1,     brh+r2) )

            result.paste( verleft,  box=( 0,     r2) )
            result.paste( vertright,box=( brw+r1, r2) )

            result.paste( tl,       box=( 0,     0) )
            result.paste( tr,       box=( brw+r1, 0) )
            result.paste( bl,       box=( 0,     brh+r2) )
            result.paste( br,       box=( brw+r1, brh+r2) )
            img = result.convert("RGBA")
            del corners, tl, tr, bl, br, b
            del horup
            del hordown
            del baserect
            del verleft
            del vertright
            return self.layer(img, 0, 0, name=name)


    def merge(self, layers):
        
        """Flattens the given layers on the canvas.
        
        Merges the given layers with the indices in the list
        on the bottom layer in the list.
        The other layers are discarded.
        
        """
        
        layers.sort()
        if layers[0] == 0: del layers[0]
        self.flatten(layers)


    def flatten(self, layers=[]):

        """Flattens all layers according to their blend modes.

        Merges all layers to the canvas,
        using the blend mode and opacity defined for each layer.
        Once flattened, the stack of layers is emptied except
        for the transparent background (bottom layer).
        """
        
        #When the layers argument is omitted,
        #flattens all the layers on the canvas.
        #When given, merges the indexed layers.
        
        #Layers that fall outside of the canvas are cropped:
        #this should be fixed by merging to a transparent background
        #large enough to hold all the given layers' data
        #(=time consuming).
        
        if layers == []: 
            layers = range(1, len(self.layers))
        background = self.layers._get_bg()
        background.name = "Background"
        
        for i in layers:

            layer = self.layers[i]
        
            #Determine which portion of the canvas
            #needs to be updated with the overlaying layer.
        
            x = max(0, layer.x)
            y = max(0, layer.y)
            w = min(background.w, layer.x+layer.w)
            h = min(background.h, layer.y+layer.h)
        
            base = background.img.crop((x, y, w, h))

            #Determine which piece of the layer
            #falls within the canvas.

            x = max(0, -layer.x)
            y = max(0, -layer.y)
            w -= layer.x
            h -= layer.y

            blend = layer.img.crop((x, y, w, h))
        
            #Buffer layer blend modes:
            #the base below is a flattened version
            #of all the layers below this one,
            #on which to merge this blended layer.
        
            if layer.blend == NORMAL:
                buffer = blend
            if layer.blend == MULTIPLY:
                buffer = ImageChops.multiply(base, blend)
            if layer.blend == SCREEN:
                buffer = ImageChops.screen(base, blend)
            if layer.blend == OVERLAY:
                buffer = Blend().overlay(base, blend)
            if layer.blend == HUE:
                buffer = Blend().hue(base, blend)
            if layer.blend == COLOR:
                buffer = Blend().color(base, blend)
            
            #Buffer a merge between the base and blend
            #according to the blend's alpha channel:
            #the base shines through where the blend is less opaque.
        
            #Merging the first layer to the transparent canvas
            #works slightly different than the other layers.
        
            alpha = buffer.split()[3]
            if i == 1:
                buffer = Image.composite(base, buffer, base.split()[3])
            else:
                buffer = Image.composite(buffer, base, alpha)
        
            #The alpha channel becomes a composite of
            #this layer and the base:
            #the base's (optional) tranparent background
            #is retained in arrays where the blend layer
            #is transparent as well.
        
            alpha = ImageChops.lighter(alpha, base.split()[3])
            buffer.putalpha(alpha)
        
            #Apply the layer's opacity,
            #merging the buffer to the base with
            #the given layer opacity.
        
            base = Image.blend(base, buffer, layer.alpha)

            #Merge the base to the flattened canvas.

            x = max(0, int(layer.x))
            y = max(0, int(layer.y))
            background.img.paste(base, (x,y))
            del base, buffer, alpha, blend

        layers.reverse()
        for i in layers:
            del self.layers[i].img
            del self.layers[i]

        img = Image.new("RGBA", (self.w,self.h), (255,255,255,0))
        self.layers._set_bg(Layer(self, img, 0, 0, name="_bg"))
        
        if len(self.layers) == 1:
            self.layers.append(background)
        else:
            self.layers.insert(layers[-1], background)
        
    def export(self, filename):

        """Exports the flattened canvas.

        Flattens the canvas.
        PNG retains the alpha channel information.
        Other possibilities are JPEG and GIF.

        """

        self.flatten()
        self.layers[1].img.save(filename, format="PNG")
        return filename
        
    def draw(self, x, y):
        
        """Places the flattened canvas in NodeBox.
        
        Exports to a temporary PNG file.
        Draws the PNG in NodeBox using the image() command.
        Removes the temporary file.
        
        """
        
        try:
            filename = "photobot_" + datestring() + ".png"
            filename = os.path.abspath(filename)
            self.export(filename)
            _ctx.image(filename, x, y)
            os.unlink(filename)
        except Exception, err:
            print err

    def preferences(interpolation=INTERPOLATION):

        """Settings that influence image manipulation.

        Currently, only defines the image interpolation, which
        can be set to NEAREST, BICUBIC, BILINEAR or LANCZOS.

        """

        self.interpolation = interpolation
        
    def topLayer( self ):
        # return top layer index
        return len(self.layers) -1


def canvas(w, h):
    return Canvas(w, h)
    
class Layers(list):
    
    """Extends the canvas.layers[] list so it indexes layers names.
    
    When the index is an integer, returns the layer at that  index.
    When the index is a string, returns the first layer with that name.
    
    The first element, canvas.layers[0],
    is the transparent background and must remain untouched.
    
    """
    
    def __getitem__(self, index):

        if type(index) in (int, long):
            return list.__getitem__(self, index)

        elif type(index) in (str, unicode):
            for layer in self:
                if layer.name == index:
                    return layer
        return None

    def _get_bg(self):
        
        return list.__getitem__(self, 0)
        
    def _set_bg(self, layer):
        
        list.__setitem__(self, 0, layer)

class Layer:
    
    """Implements a layer on the canvas.
    
    A canvas layer stores an image at a given position on the canvas,
    and all the Photoshop transformations possible for this layer:
    duplicate(), desature(), overlay(), rotate(), and so on.
    
    """
    
    def __init__(self, canvas, img, x=0, y=0, name=""):
        
        self.canvas = canvas
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.w = img.size[0]
        self.h = img.size[1]
        self.alpha = 1.0
        self.blend = NORMAL
        self.pixels = Pixels(self.img, self)
        

    def prnt(self):
        # for debugging
        print "-" * 20
        print "name:", self.name
        print "xy:", self.x, self.y
        print "wh:", self.w, self.h
        print "alpha:", self.alpha
        print "blend:", self.blend
        print "-" * 20

    def index(self):
        
        """Returns this layer's index in the canvas.layers[].
        
        Searches the position of this layer in the canvas'
        layers list, return None when not found.
        
        """
        
        for i in range(len(self.canvas.layers)):
            if self.canvas.layers[i] == self: break
        if self.canvas.layers[i] == self: 
            return i
        else:
            return None
            
    def copy(self):
        
        """Returns a copy of the layer.
        
        This is different from the duplicate() method,
        which duplicates the layer as a new layer on the canvas.
        The copy() method returns a copy of the layer
        that can be added to a different canvas.
        
        """
        
        layer = Layer(None, self.img.copy(), self.x, self.y, self.name)
        layer.w = self.w
        layer.h = self.h
        layer.alpha = self.alpha
        layer.blend = self.blend
        
        return layer
        
    def delete(self):
        
        """Removes this layer from the canvas.
              
        """
        
        i = self.index()
        if i != None: del self.canvas.layers[i]
        
    def up(self):
        
        """Moves the layer up in the stacking order.
        
        """
        
        i = self.index()
        if i != None:
            del self.canvas.layers[i]
            i = min(len(self.canvas.layers), i+1)
            self.canvas.layers.insert(i, self)
            
    def down(self):
        
        """Moves the layer down in the stacking order.
        
        """
        
        i = self.index()
        if i != None:
            del self.canvas.layers[i]
            i = max(0, i-1)
            self.canvas.layers.insert(i, self)

    def bounds(self):

        """Returns the size of the layer.

        This is the width and height of the bounding box,
        the invisible rectangle around the layer.

        """

        return self.img.size

    def select(self, path, feather=True):

        """Applies the polygonal lasso tool on a layer.

        The path paramater is a list of points,
        either [x1, y1, x2, y2, x3, y3, ...]
        or [(x1,y1), (x2,y2), (x3,y3), ...]

        The parts of the layer that fall outside
        this polygonal area are cut.
        
        The selection is not anti-aliased,
        but the feather parameter creates soft edges.

        """

        w, h = self.img.size
        mask = Image.new("L", (w,h), 0)
        draw = ImageDraw.Draw(mask)
        
        draw = ImageDraw.Draw(mask)
        draw.polygon(path, fill=255)

        if feather:
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
            
        mask = ImageChops.darker(mask, self.img.split()[3])
        self.img.putalpha(mask)

    def mask(self):

        """Masks the layer below with this layer.

        Commits the current layer to the alpha channel of 
        the previous layer. Primarily, mask() is useful when 
        using gradient layers as masks on images below. 

        For example:
        canvas.layer("image.jpg")
        canvas.gradient()
        canvas.layer(2).flip()
        canvas.layer(2).mask()

        Adds a white-to-black linear gradient to
        the alpha channel of image.jpg, 
        making it evolve from opaque on 
        the left to transparent on the right.

        """

        if len(self.canvas.layers) < 2:
            return
        i = self.index()
        if i == 0:
            return
        
        layer = self.canvas.layers[i-1]

        alpha = Image.new("L", layer.img.size, 0)

        #Make a composite of the mask layer in grayscale
        #and its own alpha channel.

        mask = self.canvas.layers[i]        
        flat = ImageChops.darker(mask.img.convert("L"), mask.img.split()[3])
        alpha.paste(flat, (mask.x,mask.y))
        alpha = ImageChops.darker(alpha, layer.img.split()[3])
        layer.img.putalpha(alpha)

        self.delete()

    def duplicate(self):

        """Creates a copy of the current layer.

        This copy becomes the top layer on the canvas.

        """

        i = self.canvas.layer(self.img.copy(), self.x, self.y, self.name)
        clone = self.canvas.layers[i]
        clone.alpha = self.alpha
        clone.blend = self.blend
                    
    def opacity(self, a=100):

        self.alpha = a * 0.01

    def multiply(self):

        self.blend = MULTIPLY

    def screen(self):

        self.blend = SCREEN

    def overlay(self):

        self.blend = OVERLAY
        
    def hue(self):

        self.blend = HUE
        
    def color(self):

        self.blend = COLOR
        
    def brightness(self, value=1.0):

        """Increases or decreases the brightness in the layer.

        The given value is a percentage to increase
        or decrease the image brightness,
        for example 0.8 means brightness at 80%.

        """
        if value > 5:
            value = value * 0.01
        b = ImageEnhance.Brightness(self.img) 
        self.img = b.enhance(value)

    def contrast(self, value=1.0):

        """Increases or decreases the contrast in the layer.

        The given value is a percentage to increase
        or decrease the image contrast,
        for example 1.2 means contrast at 120%.

        """

        if value > 5:
            value = value * 0.01
        c = ImageEnhance.Contrast(self.img) 
        self.img = c.enhance(value) 

    def desaturate(self):

        """Desaturates the layer, making it grayscale.

        Instantly removes all color information from the layer,
        while maintaing its alpha channel.

        """

        alpha = self.img.split()[3]
        self.img = self.img.convert("L")
        self.img = self.img.convert("RGBA")
        self.img.putalpha(alpha)

    def colorize(self, black, white):

        """Use the ImageOps.colorize() on desaturated layer.
        
        """
        # 
        alpha = self.img.split()[3]
        img = self.img.convert("L")
        img = ImageOps.colorize(img, black, white)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def invert(self):

        """Inverts the layer.

        """
        self.img = invertimage( self.img )

    def translate(self, x, y):

        """Positions the layer at the given coordinates.

        The x and y parameters define where to position 
        the top left corner of the layer,
        measured from the top left of the canvas.

        """

        self.x = int(x)
        self.y = int(y)

    def scale(self, w=1.0, h=1.0):

        """Resizes the layer to the given width and height.

        When width w or height h is a floating-point number,
        scales percentual, 
        otherwise scales to the given size in pixels.

        """

        w0, h0 = self.img.size
        if type(w) == FloatType: w = int(w*w0)
        if type(h) == FloatType: h = int(h*h0)

        self.img = self.img.resize((w,h), resample=LANCZOS)
        self.w = w
        self.h = h

    def distort(self, x1=0,y1=0, x2=0,y2=0, x3=0,y3=0, x4=0,y4=0):

        """Distorts the layer.
        
        Distorts the layer by translating 
        the four corners of its bounding box to the given coordinates:
        upper left (x1,y1), upper right(x2,y2),
        lower right (x3,y3) and lower left (x4,y4).
        
        """

        w, h = self.img.size
        quad = (-x1,-y1, -x4,h-y4, w-x3,w-y3, w-x2,-y2)
        # quad = (x1,y1, x2,y2, x3,y3, x4,y4)
        self.img = self.img.transform(self.img.size, Image.QUAD, quad) #, LANCZOS)

    def rotate(self, angle):

        """Rotates the layer.

        Rotates the layer by given angle.
        Positive numbers rotate counter-clockwise,
        negative numbers rotate clockwise.

        Rotate commands are executed instantly,
        so many subsequent rotates will distort the image.

        """

        #When a layer rotates, its corners will fall outside
        #of its defined width and height.
        #Thus, its bounding box needs to be expanded.

        #Calculate the diagonal width, and angle from the layer center.
        #This way we can use the layers's corners 
        #to calculate the bounding box.

        w0, h0 = self.img.size
        d = sqrt(pow(w0,2) + pow(h0,2))
        d_angle = degrees(asin((w0*0.5) / (d*0.5)))

        angle = angle % 360
        if angle > 90 and angle <= 270: d_angle += 180

        w = sin(radians(d_angle + angle)) * d
        w = max(w, sin(radians(d_angle - angle)) * d)
        w = int(abs(w))

        h = cos(radians(d_angle + angle)) * d
        h = max(h, cos(radians(d_angle - angle)) * d)
        h = int(abs(h))

        dx = int((w-w0) / 2)
        dy = int((h-h0) / 2)
        d = int(d)

        #The rotation box's background color
        #is the mean pixel value of the rotating image.
        #This is the best option to avoid borders around
        #the rotated image.

        bg = ImageStat.Stat(self.img).mean
        bg = (int(bg[0]), int(bg[1]), int(bg[2]), 0)

        box = Image.new("RGBA", (d,d), bg)
        box.paste(self.img, ((d-w0)/2, (d-h0)/2))
        box = box.rotate(angle, Image.BICUBIC)
        box = box.crop(((d-w)/2+2, (d-h)/2, d-(d-w)/2, d-(d-h)/2))
        self.img = box

        #Since rotate changes the bounding box size,
        #update the layers' width, height, and position,
        #so it rotates from the center.

        self.x += (self.w-w)/2
        self.y += (self.h-h)/2
        self.w = w
        self.h = h   

    def flip(self, axis=HORIZONTAL):

        """Flips the layer, either HORIZONTAL or VERTICAL.

        """

        if axis & HORIZONTAL:
            #print "FLIP HOR", axis
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        if axis & VERTICAL:
            #print "FLIP VERT", axis
            self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

    def blur(self):
        
        """Blurs the layer.
        
        """

        self.img = self.img.filter(ImageFilter.BLUR)

    def sharpen(self, value=1.0):

        """Increases or decreases the sharpness in the layer.

        The given value is a percentage to increase
        or decrease the image sharpness,
        for example 0.8 means sharpness at 80%.

        """
     
        s = ImageEnhance.Sharpness(self.img) 
        self.img = s.enhance(value)
        
    def statistics(self):
        
        return ImageStat.Stat(self.img, self.img.split()[3])
        
    def levels(self):
        
        """Returns a histogram for each RGBA channel.
        
        Returns a 4-tuple of lists, r, g, b, and a.
        Each list has 255 items, a count for each pixel value.
                
        """
        
        h = self.img.histogram()
        r = h[0:255]
        g = h[256:511]
        b = h[512:767]
        a = h[768:1024]
        
        return r, g, b, a

class Blend:
    
    """Layer blending modes.
    
    Implements additional blending modes to those present in PIL.
    These blending functions can not be used separately from
    the canvas.flatten() method, where the alpha compositing
    of two layers is handled.
    
    Since these blending are not part of a C library,
    but pure Python, they take forever to process.
    
    """
    
    def overlay(self, img1, img2):

        """Applies the overlay blend mode.

        Overlays image img2 on image img1.
        The overlay pixel combines multiply and screen:
        it multiplies dark pixels values and screen light values.
        Returns a composite image with the alpha channel retained.

        """

        p1 = list(img1.getdata())
        p2 = list(img2.getdata())

        for i in range(len(p1)):
        
            p3 = ()
            for j in range(len(p1[i])):

                a = p1[i][j] / 255.0
                b = p2[i][j] / 255.0
            
                #When overlaying the alpha channels,
                #take the alpha of the most transparent layer.
            
                if j == 3:
                    #d = (a+b)*0.5
                    #d = a
                    d = min(a,b)
                elif a > 0.5: 
                    d = 2*(a+b-a*b)-1
                else: 
                    d = 2*a*b            
                p3 += (int(d*255),)
        
            p1[i] = p3
        
        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

    def hue(self, img1, img2):

        """Applies the hue blend mode.

        Hues image img1 with image img2.
        The hue filter replaces the hues of pixels in img1
        with the hues of pixels in img2.
        Returns a composite image with the alpha channel retained.

        """

        p1 = list(img1.getdata())
        p2 = list(img2.getdata())
        for i in range(len(p1)):
        
            r1, g1, b1, a1 = p1[i]
            r1 = r1 / 255.0
            g1 = g1 / 255.0
            b1 = b1 / 255.0
        
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
        
            r2, g2, b2, a2 = p2[i]
            r2 = r2 / 255.0
            g2 = g2 / 255.0
            b2 = b2 / 255.0
            h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
        
            r3, g3, b3 = colorsys.hsv_to_rgb(h2, s1, v1)
        
            r3 = int(r3*255)
            g3 = int(g3*255)
            b3 = int(b3*255)
            p1[i] = (r3, g3, b3, a1)

        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

    def color(self, img1, img2):

        """Applies the color blend mode.

        Colorize image img1 with image img2.
        The color filter replaces the hue and saturation of pixels in img1
        with the hue and saturation of pixels in img2.
        Returns a composite image with the alpha channel retained.

        """
        p1 = list(img1.getdata())
        p2 = list(img2.getdata())
        for i in range(len(p1)):
        
            r1, g1, b1, a1 = p1[i]
            r1 = r1 / 255.0
            g1 = g1 / 255.0
            b1 = b1 / 255.0
        
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
        
            r2, g2, b2, a2 = p2[i]
            r2 = r2 / 255.0
            g2 = g2 / 255.0
            b2 = b2 / 255.0
            h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
        
            r3, g3, b3 = colorsys.hsv_to_rgb(h2, s2, v1)
        
            r3 = int(r3*255)
            g3 = int(g3*255)
            b3 = int(b3*255)
            p1[i] = (r3, g3, b3, a1)

        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

class Pixels:
    
    """Provides direct access to a layer's pixels.
    
    The layer.pixels[] contains all pixel values
    in a 1-dimensional array.
    Each pixel is a tuple containing (r,g,b,a) values.
    
    After the array has been updated, layer.pixels.update()
    must be called for the changes to commit.
    
    """
    
    def __init__(self, img, layer):
        
        self.layer = layer
        self.img = img
        self.data = None
        
    def __getitem__(self, i):

        w, h = self.img.size
        if i >= w*h: i -= w*h
        if i < 0: i += w*h
        
        if self.data == None: self.data = list(self.img.getdata())
        return self.data[i]
        
    def __setitem__(self, i, rgba):
        
        w, h = self.img.size
        if i >= w*h: i -= w*h
        if i < 0: i += w*h
        
        if self.data == None: self.data = list(self.img.getdata())
        self.data[i] = rgba

    def __iter__(self):
        
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        
        w, h = self.img.size
        return w * h
                    
    def update(self):
        
        if self.data != None: 
            self.img.putdata(self.data)
            self.data = None
        
    def convolute(self, kernel, scale=None, offset=0):
        
        """A (3,3) or (5,5) convolution kernel.
        
        The kernel argument is a list with either 9 or 25 elements,
        the weight for each surrounding pixels to convolute.
        
        """
        
        if len(kernel)   ==  9: size = (3,3)
        elif len(kernel) == 25: size = (5,5)
        else: return
        
        if scale == None:
            scale = 0
            for x in kernel: scale += x
            if scale == 0: scale = 1
     
        f = ImageFilter.BuiltinFilter()
        f.filterargs = size, scale, offset, kernel
        self.layer.img = self.layer.img.filter(f)


def aspectRatio(size, maxsize):
    """scale a (w,h) tuple to maxsize (either w or h)."""

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


def normalizeOrientationImage( img ):
    """Rotate an image according to exif info."""

    rotation = 0
    try:
        info = img._getexif()
        if 274 in info:
            r = info[274]
            if r == 3:
                rotation = 180
            elif r == 6:
                rotation = -90
            elif r == 8:    
                rotation = 90
    except (Exception, IndexError), err:
        pass
    if rotation != 0:
        return img.rotate( rotation )
    return img


def resizeImage( filepath, maxsize, orientation=True):
    """Get a downsampled image for use in layers."""

    try:
        img = Image.open(filepath)
    except Exception, err:
        print "\nresizeImage() FAILED", repr(filepath,)
        print err
        return ""
    # downsample the image
    if maxsize:
        newx, newy = aspectRatio( (img.size), maxsize)
        img = img.resize( (newx, newy), resample=Image.LANCZOS)

    # respect exif orientation
    if orientation:
        img = normalizeOrientationImage( img )
    return img.convert("RGBA")


