size(530, 530)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 9

try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)

strokewidth( 1.0 )
stroke( 0 )
nofill()

import pprint
pp = pprint.pprint

axiom = "F-F-F-F"
rules = {"F":"F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", "f":"ffffff"}

ang = 90
linelength = 8
depth = 2

s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
s.walk(120, 120, 0, drawit=True)

b = s.boundingBox
print "Bounding Box:", b
