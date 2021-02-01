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
        self.title = None
        self.author = None
        self.subject = None
        self.creator = None
        self.producer = None
        self.allText = ''
        self.pageText = ''
        self.parsable = None
    
    def getMetaData(self):
        self.fileName = self.pdfPath.split('/')[-1]
        try:
            # Open the PDF
            self.doc = fitz.open(self.pdfPath)
            self.numPages = self.doc.pageCount
            self.metadata = self.doc.metadata
            if self.numPages >= 0:
                self.png = self.doc.loadPage(0).getPixmap()
            else: 
                self.png.height = np.nan
                self.png.width = np.nan
                self.png.size = np.nan
            self.format = self.metadata.get('format')
            self.title = self.metadata.get('title')
            self.author = self.metadata.get('author')
            self.subject = self.metadata.get('subject')
            self.creator = self.metadata.get('creator')
            self.producer = self.metadata.get('producer')
            self.doc.close()
            return [self.pdfPath, self.fileName, self.numPages,
                    self.format, self.title, self.author, self.subject, self.creator, 
                    self.producer, self.png.height, self.png.width, self.png.size]
        except Exception:
            self.doc.close()
            return [self.pdfPath, self.fileName] + [np.nan] * 10
    
    def getTOC(self):
        self.doc = fitz.open(self.pdfPath)
        try:
            if not doc.getToC():
                return np.nan
            else:
                return doc.getToC()
        except Exception:
            return np.nan
        
    def getPageImage(self, pageNum):
        self.doc = fitz.open(self.pdfPath)
        try:
            if pageNum <= self.doc.pageCount:
                png = self.doc.loadPage(pageNum).getPixmap()
                png.writeImage("%s-%i.png" % (self.pdfPath.split('/')[-1].strip('.png'), pageNum))
                return 'Image Saved'
        except Exception:
            return 'Error getting image'
        
    def getImageSpecs(self, pageNum):
        self.doc = fitz.open(self.pdfPath)
        try:
            if pageNum <= self.doc.pageCount:
                png = self.doc.loadPage(pageNum).getPixmap()
                return [png.height, png.width, png.size]
        except Exception:
            return [np.nan] * 3
        
    # https://pymupdf.readthedocs.io/en/latest/vars.html#textpreserve
    def getAllText(self, opt = 'text'):
        self.doc = fitz.open(self.pdfPath)
        for i in range(0, self.doc.pageCount):
            self.allText += self.doc.loadPage(i).getText(opt, flags = fitz.TEXT_DEHYPHENATE)\
                            .replace('\n', ' ').strip() + ' '
        return self.allText
    
    def getPageText(self, pageNum, opt = 'text'):
        self.doc = fitz.open(self.pdfPath)
        try:
            if pageNum <= self.doc.pageCount:
                self.pageText = self.doc.loadPage(pageNum).getText(opt, flags = fitz.TEXT_DEHYPHENATE)\
                                .replace('\n', ' ').strip()
                return self.pageText
        except Exception:
            return self.pageText
        
def metaData(PDFs):
    metaDataDF = []
    for pdf in PDFs:
        p = ParsePDF(pdf)
        metaDataDF.append(p.getMetaData())
    metaDataDF = pd.DataFrame(data = np.array(metaDataDF),  
                columns = ['filePath', 'fileName', 'numPages', 'format', 'title', 'author', 'subject', 
                            'creator', 'producer', 'height', 'width', 'size'])
    return metaDataDF

def text(PDFs):
    text = []
    textLength = []
    lang = []
    for pdf in PDFs:
        p = ParsePDF(pdf)
        t = p.getAllText()
        text.append(t)
        textLength.append(len(t))
        try:
            lang.append(languages.get(alpha2 = detect(t)).name)
        except:
            lang.append(np.nan)
    textDF = pd.DataFrame({'filePath': pdf, 'textLength' : textLength, 'text' : text, 'language' : lang})
    return textDF

if __name__ == '__main__':
    FilesDF = Files(["/scratch/yte9pc/InternetArchive/Datasets/fatcat_longtail_lang/", 
             "/scratch/yte9pc/InternetArchive/Datasets/fatcat_pdf/",
             "/scratch/yte9pc/InternetArchive/Datasets/gwb_random_pdf/", 
             "/scratch/yte9pc/InternetArchive/Datasets/longtail_crawl_pdf/"])

    meta = metaData(FilesDF.filePath.values)
    meta.to_csv('/scratch/yte9pc/InternetArchive/Datasets/Preprocessed_Data/All Meta Data.csv')
    
    textDF = text(FilesDF.filePath.values)
    textDF.to_csv('/scratch/yte9pc/InternetArchive/Datasets/Preprocessed_Data/All Text.csv')
