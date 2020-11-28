from django.apps import AppConfig
from .predict import *
import tensorflow as tf
import numpy as np

class InferencesConfig(AppConfig):
    name = 'inferences'

    global label, img_size, seg_model, feature_model, cxr_model
    img_size = (224, 224)
    label  = ('negative','positive')
    ML_PATH = "./inferences/ml/"

    seg_model_name = ML_PATH + 'seg_model.h5'
    feature_model_name = ML_PATH + 'feature_model.h5'
    cxr_model_name = ML_PATH + 'cxr_model.h5'

    seg_model = tf.keras.models.load_model(seg_model_name,custom_objects={'dice_coef_loss': dice_coef_loss,'dice_coef':dice_coef})
    feature_model = tf.keras.models.load_model(feature_model_name)
    cxr_model = tf.keras.models.load_model(cxr_model_name)

    
    ''' CXR image predict function - with TF '''
    # def predict_CXR(image_path):
    #     cropped_image = get_cropped_image(image_path, seg_model)
    #     img = image_preprocessing(cropped_image, img_size)
    #     feature_vector = feature_model.predict(img)
    #     prediction = cxr_model.predict(feature_vector)[0]
    #     val = prediction.item(0)
    #     idx = int(np.round(val))

    #     return label[idx]

    def prediction_and_heatmap(image_path, model, seg_model, feature_model):
        original = tf.keras.preprocessing.image.load_img(image_path)
        original_512 = tf.keras.preprocessing.image.load_img(image_path, target_size=(512,512))
        
        cropped_image, boundary = get_cropped_image(original_512, seg_model)
        
        prediction, percent = predict_CXR(cropped_image , model, feature_model,img_size)
        
        heatmap = make_gradcam_heatmap(cropped_image, model, feature_model, img_size)
        cam_image = show_CAM(cropped_image , heatmap, prediction, boundary, 200)
        original_size_heatmap = get_original_size_heatmap(cam_image, original, original_512 , boundary)
        
        title = image_path.split('\\')[-1][:-4]
        media_path = "./media/heat/"
        heat_path = media_path + title + ".png"
        get_transparent_img(original_size_heatmap, heat_path)
        # cam_list = make_multi_heatmaps(cropped_image, original,original_512, heatmap, prediction, boundary, 10)
    
        return prediction, percent, heat_path
