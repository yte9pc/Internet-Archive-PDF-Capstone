import fitz
import pandas as pd
import numpy as np
import PyPDF2
import os
import glob
import random
from iso639 import languages
from langdetect import detect
from langdetect import detect_langs

def Files(location):
    randomFilesDF = pd.DataFrame()
    for i in location:
        pdffiles = sorted(glob.glob(i + '*.pdf'))
        pdffiles = pd.DataFrame({'filePath' : pdffiles})
        randomFilesDF = pd.concat([randomFilesDF, pdffiles])
    return randomFilesDF

class ParsePDF:
    def __init__(self, pdfPath):
        self.pdfPath = pdfPath
        self.fileName = None
        self.doc = None
        self.numPages = None
        self.toc = None
        self.metadata = None
        self.format = None
        self.parsable = None
        
    def getPageImage(self, pageNum):
        try:
            self.doc = fitz.open(self.pdfPath)
            if pageNum <= self.doc.pageCount:
                png = self.doc.loadPage(pageNum).getPixmap()
                png.writeImage("%s-%i.png" % ('#'.join(self.pdfPath.split('/')[-2:]).replace('.pdf', ''), pageNum))
                return 'Image Saved'
        except Exception:
            return 'Error getting image'
        
def pdfToPNG(PDFs):
    for pdf in PDFs:
        p = ParsePDF(pdf)
        p.getPageImage(0)
        
if __name__ == '__main__':
    os.chdir('/scratch/yte9pc/InternetArchive/Images/')
    FilesDF = Files(["/scratch/yte9pc/InternetArchive/Datasets/fatcat_longtail_lang/", 
             "/scratch/yte9pc/InternetArchive/Datasets/fatcat_pdf/",
             "/scratch/yte9pc/InternetArchive/Datasets/gwb_random_pdf/", 
             "/scratch/yte9pc/InternetArchive/Datasets/longtail_crawl_pdf/"])
    pdfToPNG(FilesDF.filePath.values)
