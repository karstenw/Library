colors = ximport("colors")

nshades = 20

clr = colors.color( choice( list(colors.named_colors.keys()) ) )
print( clr.name )
fill(0)
fontsize( 18 )
text( str(clr.name), 20, 20 )
x = 40
y = 60
for shade in colors.shades:
    fill(0)
    fontsize(14)
    text(str(shade), x, y-5)
    snapshot = shade.colors(clr, nshades)
    snapshot.swatch(x, 60)
    y = 60
    x += 50

# print( colors.shade_opposite( colors.bright) )
