# From the book
# "Lindenmayer Systems, Fractals, and Plants"
# 
# http://algorithmicbotany.org/papers/#lsfp

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
axiom = "F"
rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}

myangle = 22.5
initialangle = -90
rightangle = myangle
leftangle = -myangle

linelength = 4
depth = 4

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
