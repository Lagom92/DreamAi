def get_seg_img(model_seg, img_path):
    
    # load and resize image
    test_im = cv2.resize(cv2.imread(img_path), (512,512))[:,:,0]
    # expand_dims
    test_X = np.array(test_im).reshape(1,512,512,1) 
    test = (test_X-127.0)/127.0

    # get segmented image
    pred_im = model_seg.predict(test)
    pred_im = (pred_im>0.1)
    return pred_im

# 최 외곽 사각형의 좌표를 구한다. 0~511/ 0~511
def get_boundingbox(pred_label):
    # Set boundaries only when more than 5 pixels are found to ignore very fine errors.
    cnt = 0
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
    # To avid cropping too many pixels, make the bounding box loosely.
    return top//3, 512-(512-bottom)//3, left//3, 512-(512-right)//3

def dice_coef(y_true, y_pred):
    y_true_f = keras.flatten(y_true)
    y_pred_f = keras.flatten(y_pred)
    intersection = keras.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1) / (keras.sum(y_true_f) + keras.sum(y_pred_f) + 1)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)


# Detect an CXR's lung location and crop it.
def get_cropped_image(image_path, model_seg):
    seg_img = get_seg_img(model_seg,image_path)
    t, b, l, r = get_boundingbox(seg_img[0])
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(512,512))
    original = tf.keras.preprocessing.image.img_to_array(img)
    cropped_original = original[t:b+1, l:r+1]
    
    return cropped_original