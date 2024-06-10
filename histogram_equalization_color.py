import numpy as np
from PIL import Image


def histogram_equalization_color(image):
    if image.mode != 'RGB':
        return None

    # 转换为 numpy 数组
    img_array = np.array(image)

    # 转换为 HSV 色彩空间
    hsv_image = np.array(image.convert('HSV'))

    # 分离 H, S, V 分量
    h, s, v = np.split(hsv_image, 3, axis=2)
    h = h.reshape(-1)
    s = s.reshape(-1)
    v = v.reshape(-1)

    # 对 V 分量进行直方图均衡
    v_equalized = np.array(np.interp(v, (v.min(), v.max()), (0, 255)), dtype=np.uint8)

    # 合并 H, S, V 分量
    hsv_equalized = np.dstack((h.reshape(hsv_image.shape[0], hsv_image.shape[1]),
                               s.reshape(hsv_image.shape[0], hsv_image.shape[1]),
                               v_equalized.reshape(hsv_image.shape[0], hsv_image.shape[1])))

    # 转换回 RGB 色彩空间
    equalized_image = Image.fromarray(hsv_equalized, 'HSV').convert('RGB')

    return equalized_image
