from PIL import Image, ImageDraw

filepath = '12.png'  # Путь до файла с картинкой
img = Image.open(filepath)  # Открываем картинку
pix = img.load()  # Выгружаем картинку в матрицу значениями которой является кортеж (R,G,B) значений
width, height = 400, 1000

new_img = Image.new("RGB", (width, height), (225, 225, 225))  # Создаём пустое изрбражение заданного размера, белого фона
draw = ImageDraw.Draw(new_img)  # Создаём холст draw на котором будем рисовать пиксели в нужном порядке
for y in range(height):
    for x in range(width):
        draw.point((x,y), pix[width * y + x, 0])
        # Рисуем на холсте в координатах (x,y) пиксель, находящийся на 400 * y + x позиции

new_img.save('solved2.png', "PNG")  # Сохраняем полученное изображение и радуемся
