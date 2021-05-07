# USAGE python extract.py --i imagePath -o outputPath
from metaText import metaData
from metaText import chunk
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

def payload(imagePaths, chunkedPaths):
    # Initialize the list of payloads
    payloads = []
    # Loop over each chunk
    for (i, imagePaths) in enumerate(chunkedPaths):
        # The path of output file
        outputPath = os.path.sep.join([args["output"], "proc_{}".format(i)])
        # Dictionary containing chunk number, imagePaths, and output path
        data = {
            "id": i,
            "input_paths": imagePaths,
            "output_path": outputPath
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
    payloads = payload(allPDFPaths, chunkedPaths)
    return procs, payloads

def missingValues(final):
    # cleaning missing data
    for j in ['numPages', 'format', 'height', 'width', 'size', 'textLength']:
        final[j].fillna(-1, inplace = True)
        
    for i in ['title', 'author', 'subject', 'creator', 'producer']:
        final[i] = (final[i].isnull()).astype('int')
        
    final['languageCode'] = final['language'].astype('category').cat.codes
    final['label'] = final.filePath.str.split('/').str[-2].map({'fatcat_longtail_lang': 1, 'fatcat_pdf': 1, 'gwb_random_pdf' : 0, 'longtail_crawl_pdf' : 1})
    return final

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
        
    print("[INFO] saving final dataset")
    final = missingValues(final)
    final.to_pickle(os.path.sep.join([outputPath, fileName]))

    
if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True, type=str,
        help="path to input directory of pdfs")
    ap.add_argument("-o", "--output", required=True, type=str,
        help="path to output directory to store csv")
    ap.add_argument("-f", "--filename", required=True, type=str,
        help="file name to save as")
    ap.add_argument("-p", "--procs", type=int, default=-1,
        help="# of processes to spin up")
    args = vars(ap.parse_args())
    
    procs, payloads = initalizer(args["directory"], args["procs"], args["output"])
    
    #Construct and launch the processing pool
    print("[INFO] launching pool using {} processes...".format(procs))
    pool = Pool(processes=procs) # Generates n numbers
    pool.map(metaData, payloads)

    # close the pool and wait for all processes to finish
    print("[INFO] waiting for processes to finish...")
    pool.close()
    pool.join()
    
    print("[INFO] multiprocessing complete")
    mergePickle(args["output"], args["filename"])  