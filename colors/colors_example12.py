colors = ximport("colors")

c = colors.theme( name="sky", top=3)

for col in c:
    print( col.name, col )
    
# c.bloom(400,400)
c.swarm(200,400)
c.swatch(400,200)
