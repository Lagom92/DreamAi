import matplotlib.pyplot as plt
import librosa.display
import librosa
import tensorflow as tf
import numpy as np 
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


def audio_preprocessing(mel_path, img_size):
    img = tf.keras.preprocessing.image.load_img(mel_path, target_size=img_size)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img
