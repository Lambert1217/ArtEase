
from PIL import Image


def gray_to_binary(image, threshold):
    if not image:
        return None

    if image.mode != 'L':
        return None

    # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的黑白图像
    binary_image = Image.new("1", (width, height))

    # 获取图像的像素数据
    pixels = image.load()
    binary_pixels = binary_image.load()

    # 将灰度值根据阈值转换为黑白值
    for y in range(height):
        for x in range(width):
            # 获取像素的灰度值
            luminance = pixels[x, y]
            # 根据阈值判断黑白值
            bw_value = 0 if luminance < threshold else 255
            # 设置黑白图像的像素值
            binary_pixels[x, y] = bw_value

    return binary_image

