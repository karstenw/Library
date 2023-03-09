# From the website
#
# http://bl.ocks.org/nitaku/8b9e134ca8bae13bb470

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
# since L and R move forward in the lib they are replaced here
# with X and Y
axiom = "-Y"
rules = {"X": "XF",
         "Y": "Y+XF+XF"}

myangle = 90
initialangle = myangle
rightangle = -myangle
leftangle = myangle

linelength = 6
depth = 72

# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
