import requests
import wget
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

URL = 'https://ia903003.us.archive.org/view_archive.php?archive=/29/items/web_pdf_training_sets_201906_gwb_random_pdf/gwb_random_pdf.100k_unsafe.zip'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

def getFiles(startFiles, endFiles):
    files = []
    for i in soup.find_all('tr'):
            aValue = i.find('a')
            if aValue is not None:
                url = aValue['href']
                if '.pdf' in url:
                    files.append(url.split('/')[-1])
    return files[startFiles:endFiles]

def download(baseUrl, saveLoc, l):
    os.chdir(saveLoc)
    for element in tqdm(l):
        try:
            wget.download(baseUrl+element)
        except:
            print('Error Downloading')

if __name__ == '__main__':
    baseURl = 'https://ia903003.us.archive.org/view_archive.php?archive=/29/items/web_pdf_training_sets_201906_gwb_random_pdf/gwb_random_pdf.100k_unsafe.zip&file='
    saveLoc = '/scratch/yte9pc/InternetArchive/Datasets/gwb_random_pdf/'
    #download(baseURl, saveLoc, getFiles(0, 30000))