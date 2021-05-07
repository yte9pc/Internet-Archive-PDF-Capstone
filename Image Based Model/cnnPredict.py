import re
import os
import pandas as pd
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

def chunk(files, nChunks):
    # Loop over the list of files in n chunks
    for i in range(0, len(files), nChunks):
        # yield the current n-sized chunk to the calling function
        yield files[i: i + nChunks]

def predict(payload):
    print("[INFO] Loading Model")
    pathToModel = 'SavedModel/VGG16_V4'
    loaded_model = tf.keras.models.load_model(pathToModel)
    
    images_path = []
    file_name = []
    prediction = []
    for img in payload:
        images_path.append(img.split('/')[-1])
        file_name.append(re.sub('\-\d.png', '.pdf', img.split('/')[-1].replace('#', '/')))
        img = tf.keras.preprocessing.image.load_img(img, target_size = (256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        score = loaded_model.predict(img_array)
        prediction.append(score[0].argmax())
        
    return pd.DataFrame({'ImagePath' : images_path, 'FilePath' : file_name, 'Prediction' : prediction})

def getPrediction(payload):
    # display the process ID for debugging
    print("[INFO] starting process {}".format(payload["id"]))
   
    # loop over the image paths
    result = predict(payload["input_paths"])
    
    # Save pdf to images
    print("[INFO] process {} saving predictions".format(payload["id"]))
    result.to_pickle(payload["output_path"] + ".pkl")