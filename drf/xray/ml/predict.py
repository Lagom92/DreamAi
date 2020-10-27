import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np

def predict_CXR(image_path):
    model_name = r'C:\Users\kimji\ai-school\DreamAi\drf\xray\ml\covid_model_best_2class.h5'
    feature_model_name = r'C:\Users\kimji\ai-school\DreamAi\drf\xray\ml\feature_model299.h5'

    model = tf.keras.models.load_model(model_name)
    feature_model = tf.keras.models.load_model(feature_model_name)
 
    img_size = (299, 299)
    img = keras.preprocessing.image.load_img(image_path, target_size=img_size)
    img = keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    feature_vector = feature_model.predict(img)

    prediction = model.predict(feature_vector)

    label  = ['COVID','non-COVID']

    if prediction <= 0.5:
        predict = 0
    else:
        predict = 1

    return label[predict]
