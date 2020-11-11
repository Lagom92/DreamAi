from django.apps import AppConfig
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
import librosa
import cv2

class InferenceConfig(AppConfig):
    name = 'inference'

    # Load DL model
    print("--------------  LOAD MODEL  --------------")
    # ML_PATH = "/home/u00u654hgv0t5GGDLF357/workspace/drf/inference/ml/"
    ML_PATH = "./inference/ml/"
    cxr_model_name = ML_PATH + 'covid_model_best_2class.h5'
    cxr_feature_model_name = ML_PATH + 'feature_model299.h5'
    audio_model_name = ML_PATH + "efficientnet_audio_380.h5"
    audio_feature_model_name = ML_PATH +"efficientnet_feature_380.h5"

    global cxr_model, cxr_feature_model, audio_model, audio_feature_model
    cxr_model = tf.keras.models.load_model(cxr_model_name)
    cxr_feature_model = tf.keras.models.load_model(cxr_feature_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)
    audio_feature_model = tf.keras.models.load_model((audio_feature_model_name),custom_objects={'KerasLayer':hub.KerasLayer})

    # CXR image predict function
    def predict_CXR(image_path):
        label  = ['COVID','non-COVID']
        img_size = (299, 299)
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        feature_vector = cxr_feature_model.predict(img)
        prediction = cxr_model.predict(feature_vector)
        idx = int(np.round(prediction)[0])

        return label[idx]

    # Cough audio predict function
    def predict_audio(image_path):
        label_lst = ['negative','positive']
        img_size = (380, 380)
        img = cv2.imread(image_path)
        img = cv2.resize(img, dsize=img_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        feature_vector = audio_feature_model.predict(img)
        pred = audio_model.predict(feature_vector)[0]
        top_predict = pred.argmax()

        return label_lst[top_predict]