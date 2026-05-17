size(1440, 1024)

colormode(HSB)
nofill()

myhue = 0.5

for i in range( 400 ):
    c = color( myhue, random(0.5), random(0.5,1.0))
    stroke(c)
    strokewidth( random( 5, 64 ))
    radius = random(200)
    circle( random(WIDTH), random(HEIGHT), radius, radius )

    