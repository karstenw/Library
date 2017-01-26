# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 10 image f

# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)

# color and line attributes
strokewidth( 1 )
stroke( 0 )

nofill()
# fill(1,1,0,0.2)


# the actual lsystem parameters
axiom = "L"
rules = {"L":"L+R+",
         "R": "-L-R"}

myangle = 90
initialangle = -90
rightangle = -myangle
leftangle = myangle

linelength = 4
depth = 10

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)

