import numpy as np
from PIL import Image
def color_to_gray(image):
    if not image:
        return None

    if image.mode != 'RGB':
        return None

    # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的灰度图像
    gray_image = Image.new("L", (width, height))

    # 获取图像的像素数据
    pixels = image.load()
    gray_pixels = gray_image.load()

    # 计算灰度值并设置到新的灰度图像中
    for y in range(height):
        for x in range(width):
            # 获取像素的RGB值
            r, g, b = pixels[x, y]
            # 计算灰度值
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            # 设置灰度图像的像素值
            gray_pixels[x, y] = luminance

    return gray_image
