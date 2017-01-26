# size(530, 530)

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
strokewidth( 0.5 )
stroke( 0 )

nofill()
# fill(1,1,0,0.2)


# the actual lsystem parameters
axiom = "F-F-F-F"
rules = {"F":"F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF",
         "f":"ffffff"}

myangle = 90
initialangle = myangle
rightangle = -myangle
leftangle = myangle

linelength = 8
depth = 2

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=4)
