from django.apps import AppConfig
import tensorflow as tf
import numpy as np

class XrayConfig(AppConfig):
    name = 'xray'

    # Load DL model
    print("**************** load model ********************")
    ML_PATH = "/home/u00u654hgv0t5GGDLF357/workspace/drf/xray/ml/"
    model_name = ML_PATH + 'covid_model_best_2class.h5'
    feature_model_name = ML_PATH + 'feature_model299.h5'

    global model, feature_model
    model = tf.keras.models.load_model(model_name)
    feature_model = tf.keras.models.load_model(feature_model_name)

    # CXR image predict function
    def predict_CXR(image_path):

        img_size = (299, 299)
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        feature_vector = feature_model.predict(img)

        prediction = model.predict(feature_vector)

        label  = ['COVID','non-COVID']

        if prediction <= 0.5:
            predict = 0
        else:
            predict = 1

        return label[predict]
