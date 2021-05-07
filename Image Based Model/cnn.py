import joblib
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

import tensorflow as tf
from tensorflow.compat.v1.keras.backend import set_session
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

from tensorflow import keras
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.layers import GlobalAveragePooling2D


def split(img_height, img_width, batch_size, data_location):
    # Training Dataset
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_location,
      validation_split = 0.2,
      subset = "training",
      seed = 49,
      image_size= (img_height, img_width),
      batch_size = batch_size
    )
    
    # Validation Dataset
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_location,
      validation_split = 0.2,
      subset = "validation",
      seed = 49,
      image_size= (img_height, img_width),
      batch_size = batch_size
    )
     
    return train_ds, val_ds

if __name__ == "__main__":
    num_classes = 2
    img_width, img_height = 256, 256
    batch_size = 32
    data_location = '/scratch/yte9pc/InternetArchive/Images/Train/'
    train_ds, val_ds = split(img_height, img_width, batch_size, data_location)
    
    train_ds = train_ds.prefetch(buffer_size = batch_size)
    val_ds = val_ds.prefetch(buffer_size = batch_size)
    
    data_augmentation = keras.Sequential(
        [
            tf.keras.layers.experimental.preprocessing.Rescaling(scale=1./255)
        ]
    )
    
    inputs = tf.keras.layers.Input(shape=(img_width, img_height, 3))
    x = data_augmentation(inputs)
   
    # VGG
    VGG = tf.keras.applications.VGG16(weights = "imagenet", include_top=False, input_tensor=x)
    
    for layer in VGG.layers:
        layer.trainable = True
    
    # VGG V4
    avg = keras.layers.GlobalAveragePooling2D()(VGG.output)
    avg = keras.layers.BatchNormalization()(avg)
    avg = keras.layers.Dropout(0.5, name="final_dropout")(avg)
    avg = keras.layers.Flatten()(avg)
    avg = keras.layers.Dense(256, activation="relu")(avg)
    avg = keras.layers.Dropout(0.2)(avg)
    avg = keras.layers.Dense(128, activation="relu")(avg)
    
    output = keras.layers.Dense(num_classes, activation="softmax")(avg)
    model = keras.models.Model(inputs = VGG.input, outputs = output)
    
    ## VGG
    optimizer = keras.optimizers.Adam(learning_rate = 0.0001)
    model.compile(optimizer = optimizer, loss = "sparse_categorical_crossentropy", metrics=["accuracy"])
    
    
    earlyStop = keras.callbacks.EarlyStopping(patience = 5)
    reduce_lr = val(monitor = 'val_loss', factor = 0.2,
                                  patience = 3, min_lr = 0.000001)
    
    history = model.fit(train_ds,
                    validation_data = val_ds,
                    epochs = 15,
                    steps_per_epoch = 100,
                    validation_steps = 100,
                    callbacks = [earlyStop, reduce_lr],
                    workers = 40,
                    use_multiprocessing = True)
    
    tf.keras.models.save_model(
    model,
    'VGG16_V4',
    overwrite=True,
    include_optimizer=True,
    save_format = 'h5')
