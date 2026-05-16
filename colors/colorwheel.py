s = 500
s2 = int( s * 0.98 )

size( 2*s, 2*s )
background( None )

col = ximport("colors")

col.colorwheel( s, s, s2, 1, 1, 0)
