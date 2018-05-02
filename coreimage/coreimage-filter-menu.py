size(800, 800)

coreimage = ximport("__init__")
reload(coreimage)

import time
import pprint
pp=pprint.pprint



# remove the "# " before the l.filter lines and re-run to check a filter
filters = [
    "average", 
    "bloom", "bumpdistortion", "checkerboard", "circlesplash", "circularwrap",
    "crystallize", "dotscreen", "edges", "holedistortion", "kaleidoscope", "levels",
    "lighting", "linearbump", "lineoverlay", "motionblur", "noisereduction", "pagecurl",
    "parallelogramtile", "perspectivetile", "pixelate", "shading", "starshine",
    "stretch", "triangletile", "twirl", "zoomblur",
    "boxblur", "discblur", "sharpen", "unsharpmask"
     ]

filternames = filters

def handleFiltermenu( m ):
    global filter
    filter = m
    handleButton("dummy")



def handleParameter( value, name ):
    global helper, dx,dy, dx0,dy0,dz0, dx1,dy1, dx2,dy2, dx3,dy3
    global amount, angle_, radius, noise, sharpness, scale_, width, tilt, count
    global x_scale, x_angle, x_width, epsilon, intensity, helper, texture, threshold, contrast
    global r, g, b, a, brightness, concentration, time_

    if name == 'helper':
        helper = bool(value)
    elif name == 'dx':
        dx = float(value)
    elif name == 'dy':
        dy = float(value)

    elif name == 'dx0':
        dx0 = float(value)
    elif name == 'dy0':
        dy0 = float(value)
    elif name == 'dz0':
        dz0 = float(value)

    elif name == 'dx1':
        dx1 = float(value)
    elif name == 'dy1':
        dy1 = float(value)

    elif name == 'dx2':
        dx2 = float(value)
    elif name == 'dy2':
        dy2 = float(value)

    elif name == 'dx3':
        dx3 = float(value)
    elif name == 'dy3':
        dy3 = float(value)

    elif name == 'amount':
        amount = float(value)
    elif name == 'angle_':
        angle_ = float(value)
    elif name == 'radius':
        radius = float(value)
    elif name == 'noise':
        noise = float(value)
    elif name == 'sharpness':
        sharpness = float(value)
    elif name == 'scale_':
        scale_ = float(value)
    elif name == 'width':
        width = float(value)
    elif name == 'tilt':
        tilt = float(value)
    elif name == 'count':
        count = float(value)

    elif name == 'x_scale':
        x_scale = float(value)
    elif name == 'x_angle':
        x_angle = float(value)
    elif name == 'x_width':
        x_width = float(value)
    elif name == 'epsilon':
        epsilon = float(value)

    elif name == 'intensity':
        intensity = float(value)
    elif name == 'color_':
        color_ = float(value)
    elif name == 'threshold':
        threshold = float(value)
    elif name == 'contrast':
        contrast = float(value)

    elif name == 'r':
        r = float(value)
    elif name == 'g':
        g = float(value)
    elif name == 'b':
        b = float(value)
    elif name == 'a':
        a = float(value)
    elif name == 'brightness':
        brightness = float(value)
    elif name == 'concentration':
        concentration = float(value)
    elif name == 'time_':
        time_ = float(value)
    handleButton("dummy")



def handleButton(name):
    global filternames
    canvas = coreimage.canvas(WIDTH, HEIGHT)
    canvas.append(color(0.5))
    canvas.append("leaf.jpg")
    clr1=color(0)
    clr2=color((1,1,0))

    # layer = canvas.append("lily.tif")
    # layer = canvas.append("images/demo/_MG_4714.jpg")
    # layer = canvas.append("images/demo/Carmie 4.jpg")
    layer = canvas.append("images/demo/Fotobuch Argenturen 2010 016.jpg")
    label = "NO LABEL!"
    if filter == "average":
        pass
        # layer.filter(filter, dx=dx, dy=dy)
        # label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, scale=%.2f)" % (filter, dx,dy,radius,scale_)
    elif filter == "bloom":
        layer.filter(filter, radius=radius, intensity=intensity)
        label = "layer.filter('%s', radius=%.2f, intensity=%.2f)" % (filter, radius, intensity)
    elif filter == "bumpdistortion":
        layer.filter(filter, scale=scale_, dx=dx, dy=dy, radius=radius)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, scale=%.2f)" % (filter, dx,dy,radius,scale_)
    elif filter == "bumpdistortionlinear":
        layer.filter(filter, scale=scale_, dx=dx, dy=dy, radius=radius)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, scale=%.2f)" % (filter, dx,dy,radius,scale_)
    elif filter == "checkerboard":
        layer.filter(filter, clr1=clr1, clr2=clr2, width=width, sharpness=sharpness, angle=angle_)
        label = "layer.filter('%s', width=%.2f, sharpness=%.2f)" % (filter, width, sharpness)
    elif filter == "circlesplash":
        layer.filter(filter, dx=dx, dy=dy, radius=radius)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f)" % (filter, dx,dy,radius)
    elif filter == "circularwrap":
        layer.filter(filter, radius=radius, angle=angle_)
        label = "layer.filter('%s', radius=%.2f, angle=%.2f)" % (filter, radius, angle_)
    elif filter == "crystallize":
        layer.filter(filter, radius=radius)
        label = "layer.filter('%s', radius=%.2f)" % (filter, radius)
    elif filter == "dotscreen":
        layer.filter(filter, dx=dx, dy=dy, angle=angle_, width=width, sharpness=sharpness)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, angle=%.2f, width=%.2f, sharpness=%.2f)" % (filter, dx,dy,angle_,width,sharpness)
    elif filter == "edges":
        layer.filter(filter, intensity=intensity)
        label = "layer.filter('%s', intensity=%.2f)" % (filter, intensity)
    elif filter == "holedistortion":
        layer.filter(filter, dx=dx, dy=dy, radius=radius)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f)" % (filter, dx,dy,radius)
    elif filter == "kaleidoscope":
        layer.filter(filter, dx=dx, dy=dy, count=count)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, count=%.2f)" % (filter, dx,dy,count)
    elif filter == "levels":
        layer.filter(filter, r=r, g=g, b=b, a=a)
        label = "layer.filter('%s', r=%.2f, g=%.2f, b=%.2f, a=%.2f)" % (filter, r,g,b,a)
    elif filter == "lighting":
        layer.filter(filter, dx0=dx0, dy0=dy0, dz0=dz0, dx1=dx1, dy1=dy1, brightness=brightness, concentration=concentration, color=None)
        label = "layer.filter('%s', dx0=%.2f, dy0=%.2f, dz0=%.2f, dx1=%.2f, dy1=%.2f, brightness=%.2f, concentration=%.2f)" % (filter, dx0,dy0,dz0,dx1,dx2,brightness,concentration)
    elif filter == "linearbump":
        layer.filter(filter, scale=scale_, dx=dx, dy=dy, radius=radius, angle=angle_)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, scale=%.2f, angle=%.2f)" % (filter, dx,dy,radius,scale_,angle_)
    elif filter == "lineoverlay":
        layer.filter(filter, noise=noise, sharpness=sharpness, intensity=intensity, threshold=threshold, contrast=contrast)
        label = "layer.filter('%s', noise=%.2f, sharpness=%.2f, intensity=%.2f, threshold=%.2f, contrast=%.2f)" % (filter, noise,sharpness,intensity,threshold,contrast)
    elif filter == "motionblur":
        layer.filter(filter, angle=angle_, radius=radius)
        label = "layer.filter('%s', angle=%.2f, radius=%.2f)" % (filter, angle_,radius)
    elif filter == "noisereduction":
        layer.filter(filter, noise=noise, sharpness=sharpness)
        label = "layer.filter('%s', noise=%.2f, sharpness=%.2f)" % (filter, noise,sharpness)
    elif filter == "pagecurl":
        layer.filter(filter, time=time_, radius=radius, angle=angle_)
        label = "layer.filter('%s', time=%.2f, radius=%.2f, angle=%.2f)" % (filter, time_,radius,angle_)
    elif filter == "parallelogramtile":
        layer.filter(filter, dx=-dx, dy=dy, angle=angle_, width=width, tilt=tilt)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, angle=%.2f, width=%.2f, tilt=%.2f)" % (filter, dx,dy,angle_,width,tilt)
    elif filter == "perspectivetile":
        layer.filter(filter, dx0=dx0, dy0=dy0, dx1=dx1, dy1=dy1, dx2=dx2, dy2=dy2, dx3=dx3, dy3=dy3)
        label = "layer.filter('%s', dx0=%.2f, dy0=%.2f, dx1=%.2f, dy1=%.2f, dx2=%.2f, dy2=%.2f, dx3=%.2f, dy3=%.2f)" % (filter, dx0,dy0,dx1,dy1,dx2,dy2,dx3,dy3)
    elif filter == "pixelate":
        layer.filter(filter, scale=scale_)
        label = "layer.filter('%s', scale=%.2f)" % (filter, scale_)
    elif filter == "shading":
        layer.filter(filter, dx=dx, dy=dy, radius=radius)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f)" % (filter, dx,dy,radius)
    elif filter == "starshine":
        layer.filter(filter, dx=dx, dy=dy, radius=radius, x_scale=x_scale, x_angle=x_angle, x_width=x_width, epsilon=epsilon)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, x_scale=%.2f, x_angle=%.2f, x_width=%.2f, epsilon=%.2f)" % (filter, dx,dy,radius,x_scale,x_angle,x_width,epsilon)
    elif filter == "stretch":
        layer.filter(filter, dx=dx, dy=dy, radius=radius, angle=angle_, scale=scale_)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, angle=%.2f, scale=%.2f)" % (filter, dx,dy,radius,angle_,scale_)
    elif filter == "triangletile":
        layer.filter(filter, dx=dx, dy=dy, angle=angle_, width=width)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, angle=%.2f, width=%.2f)" % (filter, dx,dy,angle_,width)
    elif filter == "twirl":
        layer.filter(filter, dx=dx, dy=dy, radius=radius, angle=angle_)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, radius=%.2f, angle=%.2f)" % (filter, dx,dy,radius,angle_)
    elif filter == "zoomblur":
        layer.filter(filter, dx=dx, dy=dy, amount=amount)
        label = "layer.filter('%s', dx=%.2f, dy=%.2f, amount=%.2f)" % (filter, dx,dy,amount)

    elif filter == "boxblur":
        layer.filter(filter, radius=radius)
        label = "layer.filter('%s', radius=%.2f)" % (filter, radius)
    elif filter == "discblur":
        layer.filter(filter, radius=radius)
        label = "layer.filter('%s', radius=%.2f)" % (filter, radius)
    elif filter == "sharpen":
        layer.filter(filter, amount=amount)
        label = "layer.filter('%s', amount=%.2f)" % (filter, amount)
        
    elif filter == "unsharpmask":
        layer.filter(filter, radius=radius, intensity=intensity)
        label = "layer.filter('%s', radius=%.2f, intensity=%.2f)" % (filter, radius, intensity)

    # canvas.draw()
    canvas.draw(fast=False,helper=helper)
    fill(1)
    text(label, 32, 54, width=WIDTH-32)
    
var("filter", MENU, handler=handleFiltermenu, menuitems=filters)
var("apply", BUTTON, handler=handleButton)
var("helper", BOOLEAN, handler=handleParameter)

var("dx", NUMBER, min=-100, max=600, default=0, handler= handleParameter)
var("dy", NUMBER, min=-100, max=600, default=0, handler= handleParameter)

var("amount", NUMBER, min=0, max=100, default=20, handler= handleParameter)
var("angle_", NUMBER, min=0, max=360, default=0, handler= handleParameter)
var("radius", NUMBER, min=0, max=400, default=30, handler= handleParameter)
var("noise", NUMBER, min=0.0, max=2.0, default=0.02, handler= handleParameter)
var("sharpness", NUMBER, min=0.0, max=2.0, default=1.0, handler= handleParameter)
var("scale_", NUMBER, min=0.0, max=100.0, default=1.0, handler= handleParameter)
var("width", NUMBER, min=0, max=200, default=100, handler= handleParameter)

var("tilt", NUMBER, min=0, max=150, default=90, handler= handleParameter)
var("count", NUMBER, min=0, max=100, default=10, handler= handleParameter)

var("dx0", NUMBER, min=-100, max=100, default=0, handler= handleParameter)
var("dy0", NUMBER, min=-100, max=100, default=50, handler= handleParameter)
var("dz0", NUMBER, min=-100, max=100, default=0, handler= handleParameter)

var("dx1", NUMBER, min=-100, max=100, default=50, handler= handleParameter)
var("dy1", NUMBER, min=-100, max=100, default=70, handler= handleParameter)

var("dx2", NUMBER, min=-100, max=100, default=50, handler= handleParameter)
var("dy2", NUMBER, min=-100, max=100, default=0, handler= handleParameter)

var("dx3", NUMBER, min=-100, max=100, default=0, handler= handleParameter)
var("dy3", NUMBER, min=-100, max=100, default=0, handler= handleParameter)

var("x_scale", NUMBER, min=0, max=30, default=20, handler= handleParameter)
var("x_angle", NUMBER, min=0, max=360, default=0, handler= handleParameter)
var("x_width", NUMBER, min=0.0, max=10.0, default=0.5, handler= handleParameter)
var("epsilon", NUMBER, min=-10.0, max=10.0, default=-5.0, handler= handleParameter)

var("intensity", NUMBER, min=0.0, max=2.0, default=1.0, handler= handleParameter)
var("threshold", NUMBER, min=0.0, max=5.0, default=0.1, handler= handleParameter)

var("contrast", NUMBER, min=0, max=100, default=50, handler= handleParameter)

var("r", NUMBER, min=0.0, max=1.0, default=1.0, handler= handleParameter)
var("g", NUMBER, min=0.0, max=1.0, default=1.0, handler= handleParameter)
var("b", NUMBER, min=0.0, max=1.0, default=1.0, handler= handleParameter)
var("a", NUMBER, min=0.0, max=1.0, default=1.0, handler= handleParameter)
var("brightness", NUMBER, min=0.0, max=10.0, default=3.0, handler= handleParameter)
var("concentration", NUMBER, min=0.0, max=1.0, default=1.0, handler= handleParameter)
var("time_", NUMBER, min=0.0, max=1.0, default=0.0, handler= handleParameter)

handleButton("dummy")
