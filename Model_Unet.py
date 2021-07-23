import os
import numpy as np
import tensorflow as tf
from tensorflow.python.ops.gen_array_ops import tile
from tqdm import tqdm
import cv2
# from data import load_data_2, tf_dataset
# from model import build_unet

H = 256
W = 256
num_classes = 3

def predition_img(x):
    title = x
    
    model = tf.keras.models.load_model("model.h5")

    ## Read image
    x = cv2.imread(x, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (W, H))
    x = x / 255.0
    x = x.astype(np.float32)

        ## Prediction
    p = model.predict(np.expand_dims(x, axis=0))[0]
    p = np.argmax(p, axis=-1)
    p = np.expand_dims(p, axis=-1)
    # p = p * (255/num_classes)
    p = p * 50
    p = p.astype(np.int32)
    p = np.concatenate([p, p, p], axis=2)

    print(title)
    # cv2.imwrite(f"results/{name}", final_image)

    return p

if __name__ == "__main__":
    predition_img("./test_img/in/cell_1.tif")