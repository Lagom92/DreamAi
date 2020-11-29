from django.apps import AppConfig
import tensorflow as tf
from collection.predict import audio_preprocessing


class CollectionConfig(AppConfig):
    name = 'collection'

    global label, img_size, feature_model, audio_model
    label  = ('negative','positive')
    img_size = (380, 240)
    
    ML_PATH = "collection/ml/"

    feature_model_name = ML_PATH + 'audio_feature_model.h5'
    audio_model_name = ML_PATH + "audio_model.h5"

    feature_model = tf.keras.models.load_model(feature_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)


    ''' Cough audio predict function with TF '''
    def predict_audio(image_path):
        img = audio_preprocessing(image_path, img_size)

        feature_vector = feature_model.predict(img)
        prediction = audio_model.predict(feature_vector)[0]

        idx = prediction.argmax()

        return label[idx], prediction
