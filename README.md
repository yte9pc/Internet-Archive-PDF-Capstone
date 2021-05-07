# Internet-Archive-PDF

## Problem Description
As new effort in our mission towards “Universal Access to All Knowledge”, the Internet Archive
is attempting to collect and provide perpetual access to the “scholarly web”: the public record of
research publications and datasets available on the world wide web, interlinked by both
hyperlinks (URLs) and citations. We have a specific focus on “long-tail” open access works
(which may be published in non-English language, outside North America or Europe, in nonSTEM disciplines, from small or informal publishers, not assigned DOIs, not archived in existing
preservation networks, etc).

Implementation and training of a fast PDF identification tool, which can score files on
their likelihood of being a research publication, and what stage of publication (eg,
abstract, manuscript, camera ready, OCR scan) the file represents. Ideally the tool would
process hundreds of millions of files and be network (as opposed to CPU) bound.

## Environment 
- Python Version 3.7.4
- Tensorflow Version 2.3.1
- Keras Version 2.4.3


## How To
### To run the text based approach follow these steps
- First run createDB.py or download googletranslate.db
  - Recommend downloading googletranslate.db
- Second run multiprocessingMetaText.py 
  - *python multiprocessingMetaText.py -d "path to input directory of pdfs" -o "path to output directory to store csv" -f "file name to save as (needs to be pkl)" -p "# of processes to use (or let the script decide)"*
    - This script will call metaText.py and create a dataset that is used for the model

### To run the image based approach follow these steps
- First run multiprocessingPDFtoImages.py
  - *python multiprocessingMetaText.py -d "path to input directory of pdfs" -o "path to output directory to store png" -p "# of processes (or let the script decide)"*
    - This script will call pdfToImage.py and create an image of the first page of each PDF
- Second if a **VGG16_V4 model does not** exist create a training data set and run cnn.py else skip this step
  - Modify line 52 to point to training set
  - *python cnn.py*
    - This will train a VGG16 model and save the model
- Third run multiprocessingCNNPredict.py
  - Modify line 15 in cnnPredict.py to point to saved model
  - *python multiprocessingCNNPredict.py -d "path to png files" -o "path to save result" -f "resultName.csv" -p "# of processes (or let the script decide)"* 
    - This script will call cnnPredict.py and return a csv file with the prediction of each PDF 
