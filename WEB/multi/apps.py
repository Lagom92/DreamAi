from django.apps import AppConfig
from multi.predict import *
import tensorflow as tf
import numpy as np


class MultiConfig(AppConfig):
    name = 'multi'

    global label, img_size, seg_model, feature_model, multi_model
    label  = ('negative','positive')
    img_size = (224, 224)

    ML_PATH = "multi/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef':dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)

    multi_model = tf.keras.models.load_model(ML_PATH + "multi_model.h5")


    def predict_multi(image_path, audio_mel_path):
        cropped_image = get_cropped_image(image_path, seg_model)
        cxr_img = image_preprocessing(cropped_image, img_size)
        
        audio_img = audio_preprocessing(audio_mel_path, img_size)
        
        image_feature_vector = feature_model.predict(cxr_img)
        audio_feature_vector = feature_model.predict(audio_img)

        prediction = multi_model.predict([image_feature_vector, audio_feature_vector])[0]
        index = prediction.argmax()

        return label[index], prediction