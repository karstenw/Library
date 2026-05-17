colors = ximport("colors")

n = 8

# olive intense
colors.intense( colors.olive(), n=n).swatch(50, 50)

# olive neutral
colors.neutral( colors.olive(), n=n).swatch(140, 50)

# olive intense + neutral
r = colors.intense + colors.neutral
r = r(colors.olive(), n=n).swatch(230, 50)

