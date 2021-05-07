# USAGE ! python multiprocessingCNNPredict.py -d "path to png files" -o "path to save result" -f "resultName.csv"
import os
import pickle
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf

from datetime import datetime
from multiprocessing import Pool
from multiprocessing import cpu_count

from cnnPredict import chunk
from cnnPredict import getPrediction

def payload(imagePath, chunkedPaths, outputPath):
    # Initialize the list of payloads
    payloads = []
    # Loop over each chunk
    for (i, imagePath) in enumerate(chunkedPaths):
        outputPath = os.path.sep.join([args["output"], "result_{}".format(i)])
        # Dictionary containing chunk number, imagePaths
        data = {
            "id": i,
            "input_paths": imagePath,
            "output_path": outputPath
        }
        payloads.append(data)
    return payloads

def initalizer(imagesPaths, procs, outputPath):
    # Determine the number of concurrent processes to use
    procs = procs if procs > 0 else cpu_count()
    procIDs = list(range(0, procs))

    # Determine the number of images in each process
    print("[INFO] grabbing image paths...")
    allImagesPaths = [os.path.join(imagesPaths, img) for img in os.listdir(imagesPaths)]
    print(len(allImagesPaths))
    numImagesPerProc = len(allImagesPaths) / float(procs)
    numImagesPerProc = int(np.ceil(numImagesPerProc))
    
    # Split the image paths into n chunk
    chunkedPaths = list(chunk(allImagesPaths, numImagesPerProc))
    payloads = payload(allImagesPaths, chunkedPaths, outputPath)
    return procs, payloads

def mergePickle(outputPath, fileName):
    # Finds all pickled files
    pickle = [i for i in os.listdir(outputPath) if i.endswith('pkl')]
    
    print("[INFO] merging all pickled files")
    # Concatenate files by rows
    for i in range(len(pickle)):
        
        if i == 0:
            final = pd.read_pickle(os.path.sep.join([outputPath, pickle[i]]))
        else:
            new = pd.read_pickle(os.path.sep.join([outputPath, pickle[i]]))
            final = pd.concat([final, new])
            
    print("[INFO] removing all pickled files")      
    # Remove pickled csv        
    for i in pickle:
        os.remove(os.path.sep.join([outputPath, i]))
        
    print("[INFO] saving final result")
    final.to_csv(os.path.sep.join([outputPath, datetime.now().strftime("%h%d%Y_%I:%M_") + fileName ]), index = False)

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True, type=str,
        help="path to input directory of pngs")
    ap.add_argument("-o", "--output", required=True, type=str,
        help="path to output directory to store csv")
    ap.add_argument("-f", "--filename", required=True, type=str,
        help="file name to save as")
    ap.add_argument("-p", "--procs", type=int, default=-1,
        help="# of processes to spin up")
    args = vars(ap.parse_args())
    
    procs, payloads = initalizer(args["directory"], args["procs"], args["output"])
#     print("[INFO] Loading Model")
#     pathToModel = 'VGG16_V4'
#     loaded_model = tf.keras.models.load_model(pathToModel)
    
    #Construct and launch the processing pool
    print("[INFO] launching pool using {} processes...".format(procs))
    pool = Pool(processes=procs)
    pool.map(getPrediction, payloads)

    # close the pool and wait for all processes to finish
    print("[INFO] waiting for processes to finish...")
    pool.close()
    pool.join()
    print("[INFO] multiprocessing complete")
    mergePickle(args["output"], args["filename"])
