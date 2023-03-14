

r = 500
size(r,r)
randrange = -r//2, r//2
photobot = ximport("photobot")
c = photobot.canvas(r, r)
c.layer("testimage.jpg")
c.top.opacity(85)
for i in range(2,5):
    c.layers[1].duplicate()
    c.top.opacity(15)
    c.top.distort(
            random( *randrange ), random( *randrange ),
            random( *randrange ), random( *randrange ),
            random( *randrange ), random( *randrange ),
            random( *randrange ), random( *randrange )
    )

c.draw()