import numpy as np 
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from inference.ml import Seg_modules
from PIL import Image
import librosa
import matplotlib.pyplot as plt
from inference.apps import *
import os

# make mel-spectrogram image file
def make_wav2img(audio_path):
    y, sr = librosa.load(audio_path, sr = None)
    S = librosa.feature.melspectrogram(y, sr=22050, n_mels=128) 
    S_DB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_DB, sr=22050)
    title = audio_path.split('\\')[-1][:-4]
    image_path = './media/mel/'+ title +'.jpg'
    if not os.path.isdir('./media/mel'):
        os.mkdir('./media/mel')
    plt.savefig(image_path)
    
    return image_path

def image_preprocessing(cropped_image, img_size):
    img = tf.keras.preprocessing.image.array_to_img(cropped_image)
    img = img.resize(img_size)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img

def audio_preprocessing(mel_path, img_size):
    img = tf.keras.preprocessing.image.load_img(mel_path, target_size=img_size)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img

def predict_multiInput(image_path, audio_mel_path):
    
    img_size = (224, 224)
    label = ('negative','positive')
    
    cropped_image = Seg_modules.get_cropped_image(image_path, seg_model)
    cxr_img = image_preprocessing(cropped_image, img_size)
    
    audio_img = audio_preprocessing(audio_mel_path, img_size)
    
    image_feature_vector = feature_model.predict(cxr_img)
    audio_feature_vector = feature_model.predict(audio_img)

    prediction = multi_model.predict([image_feature_vector, audio_feature_vector])[0]

    predict = int(np.round(prediction))

    return label[predict]