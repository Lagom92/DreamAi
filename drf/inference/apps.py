from django.apps import AppConfig
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
# import librosa
from inference.ml import Seg_modules

class InferenceConfig(AppConfig):
    name = 'inference'

    # Load DL model
    print("--------------  LOAD MODEL  --------------")
    # ML_PATH = "/home/u00u654hgv0t5GGDLF357/workspace/drf/inference/ml/"
    ML_PATH = "./inference/ml/"

    # cxr_model_name = ML_PATH + 'covid_model_best_2class.h5'
    # cxr_feature_model_name = ML_PATH + 'feature_model299.h5'
    seg_model_name = ML_PATH + 'seg_model.h5'
    cxr_feature_model_name = ML_PATH + 'CXR_DenseNet_FP16_saved_model'
    cxr_model_name = ML_PATH + 'CXR_C2C_FP16_saved_model'

    audio_model_name = ML_PATH + "efficientnet_audio_380.h5"
    audio_feature_model_name = ML_PATH +"efficientnet_feature_380.h5"

    global cxr_model, cxr_feature_model, audio_model, audio_feature_model, seg_model

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': Seg_modules.dice_coef_loss,'dice_coef':Seg_modules.dice_coef})
    cxr_feature_model = tf.keras.models.load_model(cxr_feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)

    audio_model = tf.keras.models.load_model(audio_model_name)
    audio_feature_model = tf.keras.models.load_model((audio_feature_model_name),custom_objects={'KerasLayer':hub.KerasLayer})

    # CXR image predict function
    def predict_CXR(image_path):
        img_size=(224,224)
        label_list = ('negative','positive')

        cropped_image = Seg_modules.get_cropped_image(image_path, seg_model)
    
        img = tf.keras.preprocessing.image.array_to_img(cropped_image)
        img = img.resize(img_size)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        cropped_img = tf.constant(img)
            
        signature_keys = list(cxr_feature_model.signatures.keys())
        infer = cxr_feature_model.signatures[signature_keys[0]]
        
        pred = infer(cropped_img)

        key = list(pred.keys())[0]
        val = pred[key]
        
        signature_keys = list(cxr_model.signatures.keys())
        inference = cxr_model.signatures[signature_keys[0]]
        
        prediction = inference(val)
        
        key = list(prediction.keys())[0]
        value = prediction[key].numpy()[0]
        
        idx = int(np.round(value))
        label = label_list[idx]
            
        return label

        # label  = ['COVID','non-COVID']
        # img_size = (299, 299)
        # img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
        # img = tf.keras.preprocessing.image.img_to_array(img)
        # img = img / 255.0
        # img = np.expand_dims(img, axis=0)
        # feature_vector = cxr_feature_model.predict(img)
        # prediction = cxr_model.predict(feature_vector)
        # idx = int(np.round(prediction)[0])

        # return label[idx]

    # Cough audio predict function
    # def predict_audio(image_path):
    #     label_lst = ['negative','positive']
    #     img_size = (380, 380)
    #     img = cv2.imread(image_path)
    #     img = cv2.resize(img, dsize=img_size)
    #     img = img / 255.0
    #     img = np.expand_dims(img, axis=0)
    #     feature_vector = audio_feature_model.predict(img)
    #     pred = audio_model.predict(feature_vector)[0]
    #     top_predict = pred.argmax()

    #     return label_lst[top_predict]