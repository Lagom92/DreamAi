from inferences import apps
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np 
import librosa.display
import librosa
import os
import matplotlib.cm as cm



def dice_coef(y_true, y_pred):
    y_true_f = tf.keras.flatten(y_true)
    y_pred_f = tf.keras.flatten(y_pred)
    intersection = tf.keras.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1) / (tf.keras.sum(y_true_f) + tf.keras.sum(y_pred_f) + 1)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)

def image_preprocessing(cropped_image, img_size):
    img = tf.keras.preprocessing.image.array_to_img(cropped_image)
    img = img.resize(img_size)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


#  히트맵 생성
def make_gradcam_heatmap(cropped_image , classifier_model, last_conv_layer_model, img_size):
    img_array = image_preprocessing(cropped_image,img_size)

    with tf.GradientTape() as tape:
        last_conv_layer_output = last_conv_layer_model(img_array)
        tape.watch(last_conv_layer_output)
        preds = classifier_model(last_conv_layer_output)
        top_pred_index = tf.argmax(preds[0])
        top_class_channel = preds[:, top_pred_index]
        
    grads = tape.gradient(top_class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output.numpy()[0]
    pooled_grads = pooled_grads.numpy()
    for i in range(pooled_grads.shape[-1]):
        last_conv_layer_output[:, :, i] *= pooled_grads[i]

    heatmap = np.mean(last_conv_layer_output, axis=-1)

    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)

    return heatmap


# CAM이미지 + 원본
def show_CAM(cropped_image, heatmap, prediction, boundary, threshold=180):
    img = tf.keras.preprocessing.image.img_to_array(cropped_image)
    t,b,l,r = boundary    
    heatmap = np.uint8(255 * heatmap)
    
    heatmap[np.where(heatmap < 120)] = 0

    jet = cm.get_cmap("Reds")

    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = tf.keras.preprocessing.image.img_to_array(jet_heatmap)
    
    idx = np.where(jet_heatmap.mean(axis=2) > threshold)
    jet_heatmap[idx] = np.array([255,255,255])

    superimposed_img = jet_heatmap

    if prediction =='negative':
        superimposed_img[:,:] = [255,255,255]

    superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img)
    
    return superimposed_img

# 여러개의 heatmap 이미지를 얻는다.
def make_multi_heatmaps(cropped_image, original, original_512, heatmap, prediction, boundary, iterator=10):
    cam_list = []
    interval = 150 // iterator
    for threshold in range(50, 201, interval):
        cam_image = show_CAM(cropped_image , heatmap, prediction, boundary, threshold)
        original_size_heatmap = get_original_size_heatmap(cam_image, original, original_512, boundary)
        
        get_transparent_img(original_size_heatmap, f"media/heat/pngCXR_{threshold}.png")
        cam_list.append(original_size_heatmap)

    return cam_list


def predict_CXR(cropped_image , model, feature_model,img_size):
    img = image_preprocessing(cropped_image,img_size)
    
    feature_vector = feature_model.predict(img)

    prediction = model.predict(feature_vector)[0]
    index = prediction.argmax()
    label_name = ['negative','positive']

    label = label_name[index] 
    
    return label, prediction


def get_transparent_img(original_size_heatmap, image_name):
    img = original_size_heatmap.convert("RGBA")
    datas = img.getdata()

    newData = []
    cutOff = 255
 
    for item in datas:
        if item[0] >= cutOff and item[1] >= cutOff and item[2] >= cutOff:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    if not os.path.isdir('./media/heat'):
        os.mkdir('./media/heat')
    img.save(image_name, "PNG") 


def get_seg_img(model_seg, original_512):
    test_im = tf.keras.preprocessing.image.img_to_array(original_512)[:,:,0]
    test_X = np.array(test_im).reshape(1,512,512,1) 
    test = (test_X-127.0)/127.0

    pred_im = model_seg.predict(test)
    pred_im = (pred_im>0.1)

    return pred_im


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


def get_cropped_image(original_512, model_seg):
    seg_img = get_seg_img(model_seg, original_512)
    t, b, l, r = get_boundingbox(seg_img[0])
    original = tf.keras.preprocessing.image.img_to_array(original_512)
    cropped_original = original[t:b+1, l:r+1]
    
    return cropped_original, (t,b,l,r)


def get_original_size_heatmap(cam_image, original, original_512, boundary):
    t,b,l,r = boundary
    original = tf.keras.preprocessing.image.img_to_array(original)
    cam_image = tf.keras.preprocessing.image.img_to_array(cam_image)
    original_512 = tf.keras.preprocessing.image.img_to_array(original_512)
    original_512[:,:] = [255,255,255]

    original_512[t:b+1, l:r+1] = cam_image

    original_size_heatmap = tf.keras.preprocessing.image.array_to_img(original_512)
    original_size_heatmap = original_size_heatmap.resize((original.shape[1], original.shape[0]))
    
    return original_size_heatmap


