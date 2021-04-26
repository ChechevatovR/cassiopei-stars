from PIL import Image

def dividers(n: int) -> list:
    res = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            res += [i]
            if i * i != n:
                res += [n // i]
        i += 1
    return sorted(res)


with Image.open('12.png') as im:
    for height in dividers(400000):
        width = 400000 // height
        res = Image.frombytes('RGB', (width, height), im.tobytes())
        res.save(f'12-{width}.png')

# Откроем картинку
# Посмотрим её размеры
# Переберём все варианты размеров по делителям
# Сохраним все, посмотрим и выберем вручную
# Перепечатываем флаг, запоминаем правльную ширину (400)
