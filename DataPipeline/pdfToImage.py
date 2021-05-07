import fitz
import pandas as pd
import numpy as np
import PyPDF2
import os
import glob
import random
from tqdm import tqdm
from iso639 import languages
from langdetect import detect
from langdetect import detect_langs
fitz.TOOLS.mupdf_display_errors(False)

def chunk(files, nChunks):
    # Loop over the list of files in n chunks
    for i in range(0, len(files), nChunks):
        # yield the current n-sized chunk to the calling function
        yield files[i: i + nChunks]

class ParsePDF:
    def __init__(self, pdfPath):
        self.pdfPath = pdfPath
        self.fileName = None
        self.doc = None
        self.numPages = None
        
    def getPageImage(self, pageNum, path):
        try:
            self.doc = fitz.open(self.pdfPath)
            if pageNum <= self.doc.pageCount:
                zoom = 2.5    # higher resolution
                mat = fitz.Matrix(zoom, zoom)
                png = self.doc.loadPage(pageNum).getPixmap(matrix = mat)  
                png.writeImage("%s-%i.png" % (os.path.sep.join([path, '#'.join(self.pdfPath.split('/')[-2:]).replace('.pdf', '')]), pageNum))
                return 'Image Saved'
        except Exception:
            return 'Error getting image'
        
def pdfToPNG(payload):
    # display the process ID for debugging
    print("[INFO] starting process {}".format(payload["id"]))
   
    # loop over the file paths
    for filePath in payload["input_paths"]:
        # using ParsePDF class converted pdf to an image
        try:
            p = ParsePDF(filePath)
            print(payload["output"])
            p.getPageImage(0, payload["output"]) 
        except Exception as e:
            print('Error')
            
    # Save pdf to images
    print("[INFO] process {} saving pdfs as images".format(payload["id"]))