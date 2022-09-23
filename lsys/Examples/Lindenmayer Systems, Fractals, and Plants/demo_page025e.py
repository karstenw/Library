# From the book
# "Lindenmayer Systems, Fractals, and Plants"
# 
# http://algorithmicbotany.org/papers/#lsfp

# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
# reload( lsys )

# color and line attributes
strokewidth( 0.5 )
stroke( 0 )

nofill()
# fill(1,1,0,0.2)


# the actual lsystem parameters
axiom = "X"
rules = {"X": "F[+X]F[-X]+X",
         "F": "FF"}

myangle = 20
initialangle = -90
rightangle = -myangle
leftangle = myangle

linelength = 2
depth = 7

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
