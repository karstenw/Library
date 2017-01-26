# size(128, 128)

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
reload(lsys)

# color and line attributes
strokewidth( 0.5 )
stroke( 0 )

nofill()
# fill(1,1,0,0.2)


# the actual lsystem parameters
axiom = "-P"
rules = {"P": "PFPF+QFQ+FPFP-FQF-PFP-FQ+F+QF-PFP-FQFQFQ+",
         "Q": "-PFPFPF+QFQ+FP-F-PF+QFQ+FPF+QFQF-PFP-FQFQ"}

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
s.drawlsystem(inset=0)
