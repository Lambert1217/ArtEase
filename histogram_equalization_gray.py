from PIL import Image, ImageOps


def histogram_equalization_gray(image):
    # 检查图像是否为灰度图像
    if image.mode != 'L':
        return None

    # 进行直方图均衡
    equalized_image = ImageOps.equalize(image)

    return equalized_image
