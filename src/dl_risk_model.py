import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

class DeepRiskModel:
    def __init__(self):
        self.model = tf.keras.Sequential([
            layers.Dense(16, activation='relu', input_shape=(5,)),
            layers.Dense(8, activation='relu'),
            layers.Dense(3, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

    def train(self, X, y):
        self.model.fit(X, y, epochs=5, verbose=0)

    def predict(self, features):
        pred = self.model.predict(np.array(features), verbose=0)
        return {0: "LOW", 1: "MEDIUM", 2: "HIGH"}[np.argmax(pred)]