from PIL import Image
import numpy as np

class LinearPredictiveCoder:
    def __init__(self, predictor_order, prediction_coefficients):
        self.predictor_order = predictor_order
        self.prediction_coefficients = prediction_coefficients

    def encode(self, image):
        img_data = np.array(image)
        height, width = img_data.shape
        encoded_data = np.zeros((height, width))

        if self.predictor_order == 1:
            encoded_data[:, 0] = img_data[:, 0]
            for y in range(height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [img_data[y, x-1]])
                    encoded_data[y, x] = img_data[y, x] - predicted_value
        elif self.predictor_order == 2:
            encoded_data[:, 0] = img_data[:, 0]
            encoded_data[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [img_data[y, x-1], img_data[y-1, x]])
                    encoded_data[y, x] = img_data[y, x] - predicted_value
        elif self.predictor_order == 3:
            encoded_data[:, 0] = img_data[:, 0]
            encoded_data[0, :] = img_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [img_data[y, x-1], img_data[y-1, x], img_data[y-1, x-1]])
                    encoded_data[y, x] = img_data[y, x] - predicted_value
        else:
            return None
        
        return encoded_data

    def decode(self, encoded_data, image_shape):
        height, width = image_shape
        decoded_data = np.zeros((height, width))

        if self.predictor_order == 1:
            decoded_data[:, 0] = encoded_data[:, 0]
            for y in range(height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_data[y, x-1]])
                    decoded_data[y, x] = encoded_data[y, x] + predicted_value
        elif self.predictor_order == 2:
            decoded_data[:, 0] = encoded_data[:, 0]
            decoded_data[0, :] = encoded_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_data[y, x-1], decoded_data[y-1, x]])
                    decoded_data[y, x] = encoded_data[y, x] + predicted_value
        elif self.predictor_order == 3:
            decoded_data[:, 0] = encoded_data[:, 0]
            decoded_data[0, :] = encoded_data[0, :]
            for y in range(1, height):
                for x in range(1, width):
                    predicted_value = np.dot(self.prediction_coefficients, [decoded_data[y, x-1], decoded_data[y-1, x], decoded_data[y-1, x-1]])
                    decoded_data[y, x] = encoded_data[y, x] + predicted_value
        else:
            return None
        
        decoded_data_clipped = np.clip(decoded_data, 0, 255).astype(np.uint8)
        return Image.fromarray(decoded_data_clipped)
