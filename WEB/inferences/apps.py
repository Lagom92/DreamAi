from django.apps import AppConfig
from .predict import *
import tensorflow as tf
import numpy as np

class InferencesConfig(AppConfig):
    name = 'inferences'

    global label, img_size
    img_size = (224, 224)
    label  = ('negative','positive')

    # Load model
    global seg_model, feature_model, cxr_model, multi_model
    ML_PATH = "./inferences/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'
    cxr_model_name = ML_PATH + 'cxr_model.h5'
    multi_model_name = ML_PATH + "multi_model"

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': dice_coef_loss,'dice_coef':dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)
    multi_model = tf.keras.models.load_model(multi_model_name)

    
    ''' CXR image predict function - with TF '''
    def predict_CXR(image_path):
        cropped_image = get_cropped_image(image_path, seg_model)
        img = image_preprocessing(cropped_image, img_size)
        feature_vector = feature_model.predict(img)
        prediction = cxr_model.predict(feature_vector)[0]
        val = prediction.item(0)
        idx = int(np.round(val))

        return label[idx]


    ''' CXR and cough audio predict function with TF'''
    def predict_multi(image_path, audio_mel_path):
        cropped_image = get_cropped_image(image_path, apps.seg_model)
        cxr_img = image_preprocessing(cropped_image, img_size) 
        audio_img = audio_preprocessing(audio_mel_path, img_size)
        image_feature_vector = apps.feature_model.predict(cxr_img)
        audio_feature_vector = apps.feature_model.predict(audio_img)
        prediction = apps.multi_model.predict([image_feature_vector, audio_feature_vector])[0]
        predict = int(np.round(prediction))

        return label[predict]
