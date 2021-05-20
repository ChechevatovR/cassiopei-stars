from PIL import Image, ImageDraw

filepath = '13.png'
img = Image.open(filepath)
pix = img.load()
width, height = 400, 1000

new_img = Image.new("RGB", (width, height), (225, 225, 225))
draw = ImageDraw.Draw(new_img)
for y in range(height):
    for x in range(width):
        draw.point((x,y), pix[width*y+x, 0])

# Код выше -- решение первого плёночного фотоаппарата

pix = new_img.load()   # Выгружаем полученную картинку в матрицу с цветами
# Заполняем нулями массив shift, в котором будем хранить положение красного пикселя для каждой строки
shift = [0 for i in range(height)]
for y in range(height):
    x = 0  # Перебираем x от 0 до 400, пока не встретим красный пиксель (255, 0, 0)
    while x < width and (pix[x, y][0] != 255 or pix[x, y][1] != 0 or pix[x, y][2] != 0):
        x += 1
    else:
        shift[y] = x - 1  # Встретив такой пиксель записываем x в shift

# Сзодаём новое изображение для рисования размером 400х1000
new_img2 = Image.new("RGB", (width, height), (225, 225, 225))
draw2 = ImageDraw.Draw(new_img2)
for y in range(height):
    for x in range(width):
        # Для каждой строки делаем циклический сдвиг на shift[i] где i номер строки
        draw2.point((x, y), pix[(x + shift[y]) % width, y])

new_img2.save("13-solution.png", "PNG")  # Сохраняем
