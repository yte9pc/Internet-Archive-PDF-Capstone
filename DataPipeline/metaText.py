import fitz
import pandas as pd
import numpy as np
import PyPDF2
import os
import glob
import random
import sqlite3
from tqdm import tqdm
from iso639 import languages
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory

from googletrans import Translator
from google_trans_new import google_translator  
from deep_translator import GoogleTranslator
from deep_translator import MyMemoryTranslator

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
                
            if 'pdf' in self.metadata.get('format').lower():
                self.format = 1
            elif len(self.metadata.get('format')) == 0:
                self.format = -1
            
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
            try:
                self.doc.close()
            except Exception:
                return [self.pdfPath, self.fileName] + [np.nan] * 10
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
        try:
            self.doc = fitz.open(self.pdfPath)
            for i in range(0, self.doc.pageCount):
                self.allText += self.doc.loadPage(i).getText(opt, flags = fitz.TEXT_DEHYPHENATE)\
                                .replace('\n', ' ').strip() + ' '
        except Exception:
            return self.allText
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

        

def searchFor(text, src):
    DetectorFactory.seed = 0
    
    struct = ['abstract', 'introduction', 'conclusion', 'reference', 'table of content']
    content = ['thesis', 'research', 'statistic', 'analyze', 'analysis', 'result', 'table', 
                   'investigation', 'explain', 'theory', 'study', 'paper', 'data', 'perform', 
                   'performance', 'hypothesis', 'discussion', 'experiment', 'method', 'methodology', 
                   'measurement', 'measure', 'surgery', 'average', 'survey']
    assoc = ['journal', 'association', 'assoc', 'organization', 'doi', 'university', 'school', 
                 'board', 'publish', 'author', 'publication', 'conference', 'conference proceedings', 'society']
    
    dictionaryWords = {'structure' : struct, 'content' : content, 'association' : assoc}
    typeCount = {'structure' : '', 'content' : '', 'association' : ''}
    if len(text) != 0:
        for i in dictionaryWords:
            wordTypeCount = 0
            for j in dictionaryWords[i]:
                if src == 'en':
                    wordTypeCount += text.lower().count(j)
                elif src != 'en' and src not in [np.nan]:
                    conn = sqlite3.connect('googletranslate.db')
                    findWordSQL = "Select * FROM translate where eng_word = ? and transl_iso = ?;" 
                    translateWords = pd.read_sql_query(findWordSQL, conn, params = (j, src,)).transl_word
                    for k in translateWords.values[0].split(','):
                        wordTypeCount += text.lower().count(k.strip().lower())
                        wordTypeCount += text.lower().count(j)
                else:
                    wordTypeCount += text.lower().count(j)
            typeCount[i] = wordTypeCount
    else:
        typeCount['structure'], typeCount['content'], typeCount['association'] = 0, 0, 0
        
    return typeCount['structure'], typeCount['content'], typeCount['association']

def metaData(payload):
    # display the process ID for debugging
    print("[INFO] starting process {}".format(payload["id"]))
    metaDataDF = []
    text = []
    textLength = []
    lang = []
    iso = []
    struct = []
    content = []
    assoc = []
    
    # loop over the file paths
    for filePath in payload["input_paths"]:
        # using ParsePDF class converted pdf to an image
        fitz.TOOLS.mupdf_display_errors(False)
        try:
            p = ParsePDF(filePath)
            t = p.getAllText()
            metaDataDF.append(p.getMetaData())
            text.append(t)
            textLength.append(len(t))
            
            try:
                lang.append(languages.get(alpha2 = detect(t)).name)
                src = detect(t)
                iso.append(src)
            except Exception:
                lang.append(np.nan)
                src = np.nan
                iso.append(src)
                
            try:
                s, c, a = searchFor(t, src)
                struct.append(s)
                content.append(c)
                assoc.append(a)
            except Exception as e:
                print(e)
                struct.append(-1)
                content.append(-1)
                assoc.append(-1)
                
        except Exception as e:
            print('Error')
    metaDataDF = pd.DataFrame(data = np.array(metaDataDF),  
                columns = ['filePath', 'fileName', 'numPages', 'format', 'title', 'author', 'subject', 
                            'creator', 'producer', 'height', 'width', 'size'])
    
    metaDataDF['textLength'] = textLength
    metaDataDF['text'] = text  
    metaDataDF['language'] = lang
    metaDataDF['iso'] = iso
    metaDataDF['structure'] = struct
    metaDataDF['content'] = content
    metaDataDF['association'] = assoc
    
    # Save meta csv
    print("[INFO] process {} collected meta data".format(payload["id"]))
    metaDataDF.to_pickle(payload["output_path"] + ".pkl")
