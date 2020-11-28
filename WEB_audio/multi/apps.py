from django.apps import AppConfig
from multi.predict import *
import tensorflow as tf
import numpy as np


class MultiConfig(AppConfig):
    name = 'multi'

    global label, img_size, seg_model, feature_model, multi_model
    label  = ('negative','positive')
    img_size = (224, 224)

    ML_PATH = "./ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef':dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)

    multi_model = tf.keras.models.load_model(ML_PATH + "multi_model.h5")
