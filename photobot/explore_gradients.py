size(960, 1200)


pb = ximport("photobot")
reload(pb)

pbh = ximport("pbhelpers")
label = pbh.label

c = pb.canvas(WIDTH, HEIGHT)

c.fill((210, 210, 10))


# the gradients

# SOLID
grad1idx = c.gradient(pb.SOLID, 180, 180)
c.layers[grad1idx].translate(10, 10)
label("SOLID", 10, 10)

# LINEAR
grad2idx = c.gradient(pb.LINEAR, 180, 180)
c.layers[grad2idx].translate(200, 10)
label("LINEAR", 200, 10)

# RADIAL
grad3idx = c.gradient(pb.RADIAL, 180, 180)
c.layers[grad3idx].translate(390, 10)
label("RADIAL", 390, 10)

# DIAMOND
grad4idx = c.gradient(pb.DIAMOND, 180, 180)
c.layers[grad4idx].translate(580, 10)
label("DIAMOND", 580, 10)

# SINE (from 0 to 180)
grad5idx = c.gradient(pb.SINE, 180, 180)
c.layers[grad5idx].translate(10, 200)
label("SINE 0..180", 10, 200)

# COSINE (from 0 to 90)
grad6idx = c.gradient(pb.COSINE, 180, 180)
c.layers[grad6idx].translate(200, 200)
label("COSINE 0..90", 200, 200)

# ROUNDRECT (with radius arg)
grad7idx = c.gradient(pb.ROUNDRECT, 180, 180, radius=72, radius2=18)
c.layers[grad7idx].translate(390, 200)
label("ROUNDRECT", 390, 200)

# RADIALCOSINE
grad8idx = c.gradient(pb.RADIALCOSINE, 180, 180)
c.layers[grad8idx].translate(580, 200)
label("RADIALCOSINE", 580, 200)

# QUAD
grad8idx = c.gradient(pb.QUAD, 180, 180, radius=36, radius2=9)
c.layers[grad8idx].translate(770, 200)
label("QUAD", 770, 200)


# the gradients masked with itself
# 
gx, xy = 180, 180
# SOLID
grad1idx = c.gradient(pb.SOLID , gx, xy)
mask = c.gradient(pb.SOLID, gx, xy)
c.layers[mask].mask()
c.layers[grad1idx].translate(10, 390)


# LINEAR
grad2idx = c.gradient(pb.LINEAR, gx, xy)
mask = c.gradient(pb.LINEAR, gx, xy)
c.layers[mask].mask()
c.layers[grad2idx].translate(200, 390)


# RADIAL
# you want to have the RADIAL gradient inverted
grad3idx = c.gradient(pb.RADIAL, gx, xy, radius=36)
c.layers[grad3idx].invert()
mask = c.gradient(pb.RADIAL, gx, xy)
c.layers[mask].invert()
c.layers[mask].mask()
c.layers[grad3idx].translate(390, 390)


# DIAMOND
grad4idx = c.gradient(pb.DIAMOND, gx, xy)
mask = c.gradient(pb.DIAMOND, gx, xy)
c.layers[mask].mask()
c.layers[grad4idx].translate(580, 390)


# SINE 0..180
grad5idx = c.gradient(pb.SINE, gx, xy)
mask = c.gradient(pb.SINE, gx, xy)
c.layers[mask].mask()
c.layers[grad5idx].translate(10, 580)


# COSINE 0..90
grad6idx = c.gradient(pb.COSINE, gx, xy)
mask = c.gradient(pb.COSINE, gx, xy)
c.layers[mask].mask()
c.layers[grad6idx].translate(200, 580)


# ROUNDRECT 
grad7idx = c.gradient(pb.ROUNDRECT, gx, xy, radius=72, radius2=9)
mask = c.gradient(pb.ROUNDRECT, gx, xy, radius=72, radius2=9)
c.layers[mask].mask()
c.layers[grad7idx].translate(390, 580)


# RADIALCOSINE
grad8idx = c.gradient(pb.RADIALCOSINE, gx, xy)
mask = c.gradient(pb.RADIALCOSINE, gx, xy)
c.layers[mask].mask()
c.layers[grad8idx].translate(580, 580)

# QUAD
grad9idx = c.gradient(pb.QUAD, gx, xy, radius=36, radius2=9)
mask = c.gradient(pb.QUAD, gx, xy, radius=36, radius2=9)
c.layers[mask].mask()
c.layers[grad9idx].translate(770, 580)




# COSINE 0..90
grad6idx = c.gradient(pb.COSINE, gx, xy)
mask = c.gradient(pb.COSINE, gx, xy)
c.layers[mask].mask()
c.layers[grad6idx].translate(100, 800)
c.layers[grad6idx].rotate(45)


# RADIALCOSINE

grad8idx = c.gradient(pb.RADIALCOSINE, gx*2, xy)
mask = c.gradient(pb.RADIALCOSINE, gx*2, xy)
c.layers[mask].mask()
c.layers[grad8idx].translate(390, 770)


# QUAD
grad9idx = c.gradient(pb.QUAD, gx*2, xy)
mask = c.gradient(pb.QUAD, gx*2, xy)
c.layers[mask].mask()
c.layers[grad9idx].translate(390, 960)



c.draw(1, 1)

# put labels on top
canvas._grobs.reverse()
