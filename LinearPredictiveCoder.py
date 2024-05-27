from PIL import Image
import numpy as np

class LinearPredictiveCoder:
    def __init__(self, predictor_order, prediction_coefficients):
        self.predictor_order = predictor_order
        self.prediction_coefficients = prediction_coefficients

    def encode(self, image):
        # 确保图像是灰度图
        if image.mode != 'L':
            image = image.convert('L')
        
        img_data = np.array(image)
        height, width = img_data.shape
        encoded_image = np.zeros((height, width), dtype=np.int16)

        if self.predictor_order == 1:
            encoded_image[:, 0] = img_data[:, 0]
            for y in range(height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [encoded_image[y, x-1]])
                    encoded_image[y, x] = img_data[y, x] - predicted_value
        elif self.predictor_order == 2:
            encoded_image[:, 0] = img_data[:, 0]
            encoded_image[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [encoded_image[y, x-1], encoded_image[y-1, x]])
                    encoded_image[y, x] = img_data[y, x] - predicted_value
        elif self.predictor_order == 3:
            encoded_image[:, 0] = img_data[:, 0]
            encoded_image[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [encoded_image[y, x-1], encoded_image[y-1, x], encoded_image[y-1, x-1]])
                    encoded_image[y, x] = img_data[y, x] - predicted_value
        else:
            raise ValueError("不支持的预测器阶数。请使用 1, 2 或 3。")

        # 将值剪辑到 uint8 范围内
        encoded_image = np.clip(encoded_image, 0, 255).astype(np.uint8)
        return Image.fromarray(encoded_image)

    def decode(self, image):
        # 确保图像是灰度图
        if image.mode != 'L':
            image = image.convert('L')
        
        img_data = np.array(image)
        height, width = img_data.shape
        decoded_image = np.zeros((height, width), dtype=np.int16)

        if self.predictor_order == 1:
            decoded_image[:, 0] = img_data[:, 0]
            for y in range(height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_image[y, x-1]])
                    decoded_image[y, x] = img_data[y, x] + predicted_value
        elif self.predictor_order == 2:
            decoded_image[:, 0] = img_data[:, 0]
            decoded_image[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_image[y, x-1], decoded_image[y-1, x]])
                    decoded_image[y, x] = img_data[y, x] + predicted_value
        elif self.predictor_order == 3:
            decoded_image[:, 0] = img_data[:, 0]
            decoded_image[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_image[y, x-1], decoded_image[y-1, x], decoded_image[y-1, x-1]])
                    decoded_image[y, x] = img_data[y, x] + predicted_value
        else:
            raise ValueError("不支持的预测器阶数。请使用 1, 2 或 3。")

        # 将值剪辑到 uint8 范围内
        decoded_image = np.clip(decoded_image, 0, 255).astype(np.uint8)
        return Image.fromarray(decoded_image)
