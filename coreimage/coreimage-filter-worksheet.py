
size(800, 800)

coreimage = ximport("__init__")
# reload(coreimage)

import time
import pprint
pp=pprint.pprint

canvas = coreimage.canvas(WIDTH, HEIGHT)
canvas.append(color(0.5))
canvas.append("leaf.jpg")

l = canvas.append("lily.tif")


# remove the "# " before the l.filter lines and re-run to check a filter


# ok
# l.filter("zoomblur", dx=8, dy=-14)

# ok
# l.filter("motionblur", angle=45, radius=50)

# ok
# l.filter("noisereduction", noise=0.01, sharpness=1.0)

# ok
# l.filter("bumpdistortion", scale=0.75, dy=-35)

# ok
# l.filter("stretch", radius=90, scale=0.0, dy=-7)

# ok
# l.filter("triangletile", dx=-30, dy=-30, width=40)

# ok
# l.filter("parallelogramtile", dx=-50, dy=0, angle=10, width=100, tilt=90)

# ok
# l.filter("kaleidoscope", dx=0, dy=0, count=3)

# ok
# l.filter("circularwrap", radius=72, angle=241)

# ok
# l.filter("twirl", dx=0, dy=0, radius=150, angle=171)

# ok
# l.filter("circlesplash", dx=55, dy=80, radius=34)

# ok
# l.filter("holedistortion", dx=0, dy=-10, radius=71)

# ok
# l.filter("starshine", dx=0, dy=0, radius=25, x_scale=10, x_angle=53, x_width=0.6, epsilon=-5.0)

# ok
# l.filter("checkerboard", clr1=color(0), clr2=color(1), width=8, sharpness=1.1)

# ok
# l.filter("bloom", radius=14, intensity=0.5)

# ok
# l.filter("pixelate", scale= 7)

# ok
# l.filter("crystallize", radius=8)

# ok
# l.filter("dotscreen", dx=0, dy=0, angle=0, width=6, sharpness=0.7)

# ok
# l.filter("lighting", dx0=100, dy0=100, dz0=300, dx1=0, dy1=0, brightness=3.0, concentration=0.3, color=None, helper=False)

# ok
# l.filter("shading", radius=5, texture=None, dx=0, dy=0)

# ok
# l.filter("lineoverlay", noise=0.07, sharpness=0.31, intensity=1.0, threshold=0.1, contrast=-14)


# ok
# l.filter("pagecurl", time=0.4, radius=34, angle=275, back=None)


# ok
# l.filter("levels", r=1.0, g=1.0, b=.0, a=.5)

# ok
# l.filter("edges", intensity=1.0)

# ok
# 2017-05-21 Finally ok. The lib tried to create an infinite canvas and apply
# opacity to it. Opacity is now ignored if width + height > 20000
# l.filter("perspectivetile", dx0=0.0, dy0=50.0, dx1=50.0, dy1=70.0, dx2=50.0, dy2=0.0, dx3=0.0, dy3=0.0, helper=1)


# canvas.draw()
canvas.draw(fast=False,helper=0)
