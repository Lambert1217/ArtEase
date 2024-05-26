from PIL import Image
import numpy as np

class LinearPredictiveCoder:
    def __init__(self, predictor_order, prediction_coefficients):
        self.predictor_order = predictor_order
        self.prediction_coefficients = prediction_coefficients

    def encode(self, image):
        # 获取图像数据
        img_data = np.array(image)

        # 初始化编码后的数据列表
        encoded_data = []

        # 对图像进行线性预测编码
        for row in img_data:
            prediction_residuals = np.zeros_like(row, dtype=np.int32)
            for i in range(self.predictor_order, len(row)):
                predicted_value = np.dot(self.prediction_coefficients, row[i - self.predictor_order:i])
                prediction_residuals[i] = row[i] - predicted_value
            encoded_data.append(prediction_residuals)

        return encoded_data

    def decode(self, encoded_data, image_shape):
        # 初始化解码后的图像数据
        decoded_image = np.zeros(image_shape, dtype=np.uint8)

        # 对编码后的数据进行解码
        for i, row in enumerate(encoded_data):
            decoded_row = np.zeros_like(row, dtype=np.uint8)
            for j in range(self.predictor_order, len(row)):
                predicted_value = np.dot(self.prediction_coefficients, decoded_row[j - self.predictor_order:j])
                decoded_row[j] = row[j] + predicted_value
            # 将解码后的行数据赋值给解码后的图像的对应行
            decoded_image[i] = decoded_row

        return Image.fromarray(decoded_image)
    
