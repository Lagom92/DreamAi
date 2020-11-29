import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
import cv2
import numpy as np
from .prediction_and_heatmap_function import get_img_array,make_gradcam_heatmap,gamma_correction,show_CAM,predict_CXR

#진균
def inception_resnt_predict_CXR_and_heatmap(image_path):
    model_path = r'boards\ml\inception_Resnet_model299_best.h5'
    feature_model_path = r'boards\ml\Inception_Resnet_feature_model299.h5'

    model = load_model(model_path)
    feature_model = load_model(feature_model_path)

    prediction, plot = predict_CXR(image_path, model, feature_model)

    heatmap = make_gradcam_heatmap(image_path, model, feature_model)

    cam_image = show_CAM(image_path, heatmap, prediction)

    return prediction, cam_image, plot

