from django.apps import AppConfig
import tensorflow as tf
from collection.predict import *


class CollectionConfig(AppConfig):
    name = 'collection'

    global label, img_size
    label  = ('negative','positive')
    img_size = (224, 224)

    # Load model
    global feature_model, audio_model
    ML_PATH = "./ml/"

    feature_model_name = ML_PATH + 'feature_model.h5'
    audio_model_name = ML_PATH + "audio_model.h5"

    feature_model = tf.keras.models.load_model(feature_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)


    ''' Cough audio predict function with TF '''
    def predict_audio(image_path):
        img = audio_preprocessing(image_path, img_size)
        feature_vector = feature_model.predict(img)
        prediction = audio_model.predict(feature_vector)[0]
        idx = int(prediction.round()[0])

        return label[idx]
