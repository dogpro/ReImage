import random

from PIL import Image, ImageDraw
import io


def get_bytes_in_image(img_byte_array):
    return Image.open(io.BytesIO(img_byte_array))


def get_image_in_byte(data):
    img_byte_array = io.BytesIO()
    data.save(img_byte_array, format='PNG')
    return img_byte_array.getvalue()


def to_bytes(func):
    def wrapper(*args, **kwargs):
        return get_image_in_byte(func(*args, **kwargs))

    return wrapper


def from_bytes(func):
    def wrapper(data, *args):
        data = get_bytes_in_image(data)
        return func(data, *args)

    return wrapper


def get_original(data):
    draw = ImageDraw.Draw(data)
    width = data.size[0]
    height = data.size[1]
    pix = data.load()
    return draw, width, height, pix


@from_bytes
@to_bytes
def grayscale(data):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            A = (r + g + b) // 3
            draw.point((i, j), (A, A, A))
    return data


@from_bytes
@to_bytes
def sepia(data, percent):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            a = S + percent * 2
            b = S + percent
            c = S
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    return data


@from_bytes
@to_bytes
def negative(data):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))
    return data


@from_bytes
@to_bytes
def threshold(data, percent):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = a + b + c
            if S > (((255 + percent) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))
    return data


@from_bytes
@to_bytes
def noises(data, percent):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            rand = random.randint(-percent, percent)
            a = pix[i, j][0] + rand
            b = pix[i, j][1] + rand
            c = pix[i, j][2] + rand
            if a < 0:
                a = 0
            if b < 0:
                b = 0
            if c < 0:
                c = 0
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    return data


@from_bytes
@to_bytes
def brightness(data, percent):
    draw, width, height, pix = get_original(data)
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0] + percent
            b = pix[i, j][1] + percent
            c = pix[i, j][2] + percent
            if a < 0:
                a = 0
            if b < 0:
                b = 0
            if c < 0:
                c = 0
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    return data


@from_bytes
@to_bytes
def flip_vertical(data):
    return data.transpose(Image.FLIP_LEFT_RIGHT)


@from_bytes
@to_bytes
def flip_horizontal(data):
    return data.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)


@from_bytes
@to_bytes
def rotate(data, percent):
    return data.rotate(percent)


@from_bytes
@to_bytes
def crop(data, box):
    return data.crop(box)


# with open("1.png", 'rb') as f:
#     imgByteArr = f.read()
#
# image = crop(imgByteArr, [0, 0, 100, 100])
#
# image2 = Image.open(io.BytesIO(image))
# image2.save("2.png")
