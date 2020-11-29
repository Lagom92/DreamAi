import matplotlib.pyplot as plt
from multi import apps
import tensorflow as tf
import numpy as np 
import librosa.display
import librosa
import os


def get_seg_img(model_seg, image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(512,512))
    img = tf.keras.preprocessing.image.img_to_array(img)[:,:,0]
    img = np.array(img).reshape(1,512,512,1) 
    img = (img-127.0)/127.0
    pred_im = model_seg.predict(img)
    pred_im = (pred_im>0.1)
    
    return pred_im


def image_preprocessing(cropped_image, img_size):
    img = tf.keras.preprocessing.image.array_to_img(cropped_image)
    img = img.resize(img_size)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img


def get_boundingbox(pred_label):
    top, bottom, left, right, cnt = 0, 0, 0, 0, 0
    for i in range(len(pred_label)):
        if True in pred_label[i]:
            cnt += 1
        if cnt >= 5:
            top = i
            break
    cnt = 0
    for i in range(len(pred_label)-1, 0, -1):
        if True in pred_label[i]:
            cnt += 1
        if cnt >= 5:
            bottom = i
            break
    cnt = 0
    for i in range(len(pred_label)):
        if True in pred_label[:, i]:
            cnt += 1
        if cnt >= 5:
            left = i
            break
    cnt = 0       
    for i in range(len(pred_label)-1, 0, -1):
        if True in pred_label[:,i]:
            cnt += 1
        if cnt >= 5:
            right = i
            break
    return top//2, 512-(512-bottom)//2, left//2, 512-(512-right)//2


def dice_coef(y_true, y_pred):
    y_true_f = tf.keras.flatten(y_true)
    y_pred_f = tf.keras.flatten(y_pred)
    intersection = tf.keras.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1) / (tf.keras.sum(y_true_f) + tf.keras.sum(y_pred_f) + 1)


def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)


def get_cropped_image(image_path, model_seg):
    seg_img = get_seg_img(model_seg,image_path)
    t, b, l, r = get_boundingbox(seg_img[0])
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(512,512))
    original = tf.keras.preprocessing.image.img_to_array(img)
    cropped_original = original[t:b+1, l:r+1]
    
    return cropped_original


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
