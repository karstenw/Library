# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 12 image a

# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
# reload(lsys)

# color and line attributes
strokewidth( 1 )
stroke( 0 )

nofill()
# fill(1,1,0,0.2)


# the actual lsystem parameters
axiom = "-R"
rules = {"L": ("LL-R-R+L+L-R-RL+"
               "R+LLR-L+R+LL+"
               "R-LR-R-L+L+RR-"),
         "R": ("+LL-R-R+L+LR+L-"
               "RR-L-R+LRR-L-"
               "RL+L+R-R-L+L+RR")}

myangle = 90
initialangle = -90
rightangle = -myangle
leftangle = myangle

linelength = 8
depth = 2

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
