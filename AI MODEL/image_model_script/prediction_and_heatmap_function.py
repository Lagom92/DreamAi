# import module

from keras.models import load_model
from tensorflow import keras
import tensorflow as tf
import matplotlib.cm as cm
import numpy as np 
import matplotlib.pyplot as plt
import os
from keras.applications.densenet import preprocess_input



# 이미지 전처리
def get_img_array(img_path, size):

    img = keras.preprocessing.image.load_img(img_path, target_size=size)
    array = keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array

#  히트맵 생성
def make_gradcam_heatmap(img_path, classifier_model, last_conv_layer_model):
    img_size = (224,224)
    img_array = preprocess_input(get_img_array(img_path, size=img_size))


    with tf.GradientTape() as tape:
        # Compute activations of the last conv layer and make the tape watch it
        last_conv_layer_output = last_conv_layer_model(img_array)
        tape.watch(last_conv_layer_output)
        # Compute class predictions
        preds = classifier_model(last_conv_layer_output)
        top_pred_index = tf.argmax(preds[0])
        top_class_channel = preds[:, top_pred_index]

    # This is the gradient of the top predicted class with regard to
    # the output feature map of the last conv layer
    grads = tape.gradient(top_class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    last_conv_layer_output = last_conv_layer_output.numpy()[0]
    pooled_grads = pooled_grads.numpy()
    for i in range(pooled_grads.shape[-1]):
        last_conv_layer_output[:, :, i] *= pooled_grads[i]

    # The channel-wise mean of the resulting feature map
    # is our heatmap of class activation
    heatmap = np.mean(last_conv_layer_output, axis=-1)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)

    # 보정 -- 이미지의 최 외곽부 모두 0
    a = np.vstack((np.zeros(heatmap[:2].shape),heatmap[2:-1]))
    a = np.vstack((a[:-1],np.zeros(heatmap[-1:].shape)))
    for i in a:
        i[0] = 0
        i[-1] = 0
    heatmap = a

    return heatmap

# 감마보정
# gamma correction 
def gamma_correction(img, c=1, g=2.2): 
    out = img.copy() 
    out /= 255. 
    out = (1/c * out) ** (1/g) 
    out *= 255 
    out = out.astype(np.uint8) 
    return out 

# CAM이미지 + 원본
def show_CAM(img_path, heatmap, prediction):
    # We load the original image
    img = keras.preprocessing.image.load_img(img_path)
    img = keras.preprocessing.image.img_to_array(img)

    # We rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # We use jet colormap to colorize heatmap
    jet = cm.get_cmap("Reds")

    # We use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # We create an image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)
    
    # gamma correction
    jet_heatmap = gamma_correction(jet_heatmap, g=2.2)

    # Superimpose the heatmap on original image
    # NORMAL이면 원본이미지만 반환
    if prediction =='NORMAL':
        superimposed_img = img
    else:
        superimposed_img = jet_heatmap *0.5 + img
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

    return superimposed_img

# 예측함수
# opencv의 resize에서 오류가 발생하여 keras.preprocessing.image의 함수들을 사용하였다.
def predict_CXR(image_path, model, feature_model):

    img_size = (224,224)
    # 이미지 불러오기 및 이미지 크기 조정
    img = keras.preprocessing.image.load_img(image_path, target_size=img_size)
    # 이미지를 array로 변경
    img = keras.preprocessing.image.img_to_array(img)
    # 각 픽셀값을 0과 1사이의 값으로 조정
    img = img / 255.0
    # 모델의 인풋 타입에 맞게 차원을 하나 늘림
    img = np.expand_dims(img, axis=0)
    # feature_model에서 feature 추출
    feature_vector = feature_model.predict(img)
    # 앞서 생성한 model 분류기를 통해 예측 수행
    prediction = model.predict(feature_vector)[0]
    # print(prediction)
    unique_sorted_Y = ['COVID19','NORMAL','PNEUMONIA']

    top_3_predict = prediction.argsort()[::-1][:3]
    print(top_3_predict)
    #labels에 저장 
    labels = [unique_sorted_Y[index] for index in top_3_predict]
    color = ['blue'] * 3


    # show portion
    text = []
    text = prediction[top_3_predict][::-1] * 100
    print(text)
    rects = plt.barh(range(3), text, color = color)
    plt.yticks(np.arange(3), labels[::-1], rotation=45)
    plt.xlim(0,100)

    # plt.rc('font', size=10)
    for i, rect in enumerate(rects):
        plt.text(rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(round(text[i], 1)) + '%', ha='left', va='center')
    plt.draw()
    plt.savefig('media/prediction_plot.jpg')
    plot = keras.preprocessing.image.load_img('media/prediction_plot.jpg')
    os.remove('media/prediction_plot.jpg')
    plt.clf()
    
    return labels[0], plot
