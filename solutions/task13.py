from PIL import Image, ImageDraw

filepath = '13.png'
img = Image.open(filepath)
pix = img.load()
width = 400
height = 1000
l = width*height

new_img = Image.new("RGB", (width,height), (225, 225, 225))
draw = ImageDraw.Draw(new_img)
for y in range(height):
    for x in range(width):
        draw.point((x,y), pix[width*y+x,0])

pix = new_img.load()
shift = [0 for i in range(height)]
for y in range(height):
    x = 0
    while x<width and (pix[x, y][0] != 255 or pix[x, y][1] != 0 or pix[x, y][2] != 0) :
        x += 1
    else:
        shift[y] = x-1
        x=0
print(shift)

new_img2 = Image.new("RGB", (width,height), (225, 225, 225))
draw2 = ImageDraw.Draw(new_img2)
for y in range(height):
    for x in range(width):
        draw2.point((x, y), pix[(x + shift[y]) % width, y])

new_img2.save("13-solution.png", "PNG")
