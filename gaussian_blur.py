from PIL import Image, ImageFilter

def apply_gaussian_blur(image, radius):
    """
    Apply Gaussian blur to an image.

    :param image: PIL Image object to be blurred
    :param radius: Radius for Gaussian blur
    :return: Blurred PIL Image object
    """
    return image.filter(ImageFilter.GaussianBlur(radius=radius))
