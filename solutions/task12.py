from PIL import Image, ImageDraw  # Импортируем библиотеку для работы с изображениями

filepath = '12.png'         # Путь до файла с картинкой
img = Image.open(filepath)  # Открываем картинку
pix = img.load()            # Выгружаем картинку в матрицу значениями которой является кортеж (R,G,B) значений
width, height = 400, 1000

# Создаём пустое изрбражение заданного размера, белого фона
new_img = Image.new("RGB", (width, height), (225, 225, 225))
# Создаём холст draw на котором будем рисовать пиксели в нужном порядке
draw = ImageDraw.Draw(new_img)
for y in range(height):
    for x in range(width):
        # Рисуем на холсте в координатах (x,y) пиксель, находящийся на 400 * y + x позиции
        draw.point((x,y), pix[width * y + x, 0])

new_img.save('solved2.png', "PNG")  # Сохраняем полученное изображение и радуемся
