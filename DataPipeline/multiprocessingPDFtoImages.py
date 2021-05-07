# USAGE python extract.py --i imagePath -o outputPath
from pdfToImage import pdfToPNG
from pdfToImage import chunk
from multiprocessing import Pool
from multiprocessing import cpu_count
from imutils import paths
import numpy as np
import argparse
import pickle
import os
import glob
import pandas as pd

def Files(location):
    randomFilesDF = pd.DataFrame()
    for i in location:
        pdffiles = sorted(glob.glob(i + '/' + '*.pdf'))
        pdffiles = pd.DataFrame({'filePath' : pdffiles})
        randomFilesDF = pd.concat([randomFilesDF, pdffiles])
    return randomFilesDF

def payload(pdfPaths, chunkedPaths, outputPath):
    # Initialize the list of payloads
    payloads = []
    # Loop over each chunk
    for (i, pdfPaths) in enumerate(chunkedPaths):
        # Dictionary containing chunk number, imagePaths
        data = {
            "id": i,
            "input_paths": pdfPaths,
            "output": outputPath
        }
        payloads.append(data)
    return payloads

def initalizer(pdfPaths, procs, outputPath):
    # Determine the number of concurrent processes to use
    procs = procs if procs > 0 else cpu_count()
    procIDs = list(range(0, procs))

    # Determine the number of images in each process
    print("[INFO] grabbing pdf paths...")
    files = Files([x[0] for x in os.walk(pdfPaths) if 'pdf' in x[0] or 'fat' in x[0]])
    allPDFPaths = files.filePath.values
    numPDFPerProc = len(allPDFPaths) / float(procs)
    numPDFPerProc = int(np.ceil(numPDFPerProc))
    
    # Split the image paths into n chunk
    chunkedPaths = list(chunk(allPDFPaths, numPDFPerProc))
    payloads = payload(allPDFPaths, chunkedPaths, outputPath)
    return procs, payloads
    
if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True, type=str,
        help="path to input directory of pdfs")
    ap.add_argument("-o", "--output", required=True, type=str,
        help="path to output directory to store image")
    ap.add_argument("-p", "--procs", type=int, default=-1,
        help="# of processes to spin up")
    args = vars(ap.parse_args())
    
    procs, payloads = initalizer(args["directory"], args["procs"], args["output"])
    #Construct and launch the processing pool
    print("[INFO] launching pool using {} processes...".format(procs))
    pool = Pool(processes=procs)
    pool.map(pdfToPNG, payloads)

    # close the pool and wait for all processes to finish
    print("[INFO] waiting for processes to finish...")
    pool.close()
    pool.join()
    print("[INFO] multiprocessing complete")