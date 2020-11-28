from django.apps import AppConfig
from multi.predict import *
import tensorflow as tf
import numpy as np


class MultiConfig(AppConfig):
    name = 'multi'

    global label, img_size
    label  = ('negative','positive')
    img_size = (224, 224)

    # Load model
    global seg_model, feature_model, cxr_model, audio_model, multi_model
    ML_PATH = "../collection/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'
    cxr_model_name = ML_PATH + 'cxr_model.h5'
    audio_model_name = ML_PATH + "audio_model.h5"

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef':dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)

    multi_model = tf.keras.models.load_model(ML_PATH + "multi_model")
