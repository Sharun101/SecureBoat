# coding: utf-8

# In[ ]:
import os

import tensorflow as tf

import keras
from keras.engine.saving import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np

#------------------------------
# sess = tf.Session()
# keras.backend.set_session(sess)
#------------------------------
#variables
num_classes =3 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 40
epochs = 5
#------------------------------

import os, cv2, keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.engine.saving import load_model
# manipulate with numpy,load with panda
import numpy as np
# import pandas as pd

# data visualization
import cv2

def read_dataset1(path):
    data_list = []
    label_list = []

    file_path = os.path.join(path)
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
    data_list.append(res)
    # label = dirPath.split('/')[-1]

            # label_list.remove("./training")
    return (np.asarray(data_list, dtype=np.float32))
my_list = ["safe","unsafe"]
mo = load_model(r"C:\devagiri\secureboat (3)\secureboat\myapp\model1.h5")

def predict(fn):
    try:
        dataset=read_dataset1(fn)
        (mnist_row, mnist_col, mnist_color) = 48, 48, 1

        dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
        dataset/=255

        # predict probabilities for test set

        yhat_classes = mo.predict_classes(dataset, verbose=0)
        # return yhat_classes
    #
        print(yhat_classes)
        print(my_list[yhat_classes[0]])
        return my_list[yhat_classes[0]]
    except:
        return "na"
# predict(r"D:\VJEC PhD\PREDICTION\src\static\dataset\electric work safe\download.jfif")