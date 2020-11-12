from inference.myPredicts import audio_preprocessing, image_preprocessing
from inference import seg_modules
from django.apps import AppConfig
import tensorflow as tf
import numpy as np


class InferenceConfig(AppConfig):
    name = 'inference'

    global label, img_size
    label  = ('negative','positive')
    img_size = (224, 224)

    # Load model
    global seg_model, feature_model, cxr_model, audio_model, multi_model
    ML_PATH = "./inference/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'
    cxr_model_name = ML_PATH + 'cxr_model.h5'
    # feature_model_name = ML_PATH + 'CXR_DenseNet_FP16_saved_model'
    # cxr_model_name = ML_PATH + 'CXR_C2C_FP16_saved_model'
    audio_model_name = ML_PATH + "audio_model.h5"

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': seg_modules.dice_coef_loss,'dice_coef':seg_modules.dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)
    audio_model = tf.keras.models.load_model(audio_model_name)

    multi_model = tf.keras.models.load_model(ML_PATH + "multi_model")

    # CXR image predict function - TF-TRT
    # def predict_CXR(image_path):
    #     cropped_image = seg_modules.get_cropped_image(image_path, seg_model)
    #     img = image_preprocessing(cropped_image, img_size)

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
        cropped_image = seg_modules.get_cropped_image(image_path, seg_model)
        img = image_preprocessing(cropped_image, img_size)
        feature_vector = feature_model.predict(img)
        prediction = cxr_model.predict(feature_vector)[0]
        val = prediction.item(0)
        idx = int(np.round(val))

        return label[idx]


    # Cough audio predict function - dev
    def predict_audio(image_path):
        img = audio_preprocessing(image_path, img_size)
        feature_vector = feature_model.predict(img)
        prediction = audio_model.predict(feature_vector)[0]
        idx = int(prediction.round()[0])

        return label[idx]
