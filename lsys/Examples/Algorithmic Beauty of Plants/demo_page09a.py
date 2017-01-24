size(530, 530)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 9

# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)

# color and line attributes
strokewidth( 1.0 )
stroke( 0 )
nofill()

# the actual parameters
axiom = "F-F-F-F"
rules = {"F":"F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}

ang = 90
linelength = 8
depth = 2


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)

s.generate()
s.walk(120, 120, 0, drawit=True)

print s.boundingBox
