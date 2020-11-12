from django.apps import AppConfig
from inference.ml import Seg_modules
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

class InferenceConfig(AppConfig):
    name = 'inference'

    # Load model
    global seg_model, feature_model, cxr_model, audio_model, multi_model
    ML_PATH = "./inference/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'
    cxr_model_name = ML_PATH + 'cxr_model.h5'
    # feature_model_name = ML_PATH + 'CXR_DenseNet_FP16_saved_model'
    # cxr_model_name = ML_PATH + 'CXR_C2C_FP16_saved_model'
    audio_model_name = ML_PATH + "audio_model.h5"

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': Seg_modules.dice_coef_loss,'dice_coef':Seg_modules.dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)

    multi_model = tf.keras.models.load_model(ML_PATH + "multi_model")

    # CXR image predict function - TF-TRT
    # def predict_CXR(image_path):
    #     img_size=(224,224)
    #     label = ('negative','positive')
    #     cropped_image = Seg_modules.get_cropped_image(image_path, seg_model)
    #     img = tf.keras.preprocessing.image.array_to_img(cropped_image)
    #     img = img.resize(img_size)
    #     img = tf.keras.preprocessing.image.img_to_array(img)
    #     img = img / 255.0
    #     img = np.expand_dims(img, axis=0)
    #     cropped_img = tf.constant(img) 
    #     signature_keys = list(feature_model.signatures.keys())
    #     infer = feature_model.signatures[signature_keys[0]]
    #     pred = infer(cropped_img)
    #     key = list(pred.keys())[0]
    #     val = pred[key]
    #     signature_keys = list(cxr_model.signatures.keys())
    #     inference = cxr_model.signatures[signature_keys[0]]
    #     prediction = inference(val)
    #     key = list(prediction.keys())[0]
    #     value = prediction[key].numpy()[0]
    #     idx = int(np.round(value))
            
    #     return label[idx]


    # CXR image predict function - dev
    def predict_CXR(image_path):
        label  = ('negative','positive')
        img_size = (224, 224)
        cropped_image = Seg_modules.get_cropped_image(image_path, seg_model)
        img = tf.keras.preprocessing.image.array_to_img(cropped_image)
        img = img.resize(img_size)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        feature_vector = feature_model.predict(img)
        prediction = cxr_model.predict(feature_vector)[0]
        val = prediction.item(0)
        idx = int(np.round(val))

        return label[idx]

    # Cough audio predict function - dev
    def predict_audio(image_path):
        label  = ('negative','positive')
        img_size=(224,224)
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        feature_vector = feature_model.predict(img)
        prediction = audio_model.predict(feature_vector)[0]
        idx = int(prediction.round()[0])

        return label[idx]