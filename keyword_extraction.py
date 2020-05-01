################################################################################
#       Run 'sh init_sner' in the terminal before running this script          #
################################################################################

import os
import PyPDF2 
import textract
from os import walk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger

################################ PDF To Text ###################################
dir_name = 'Financial Reports/29BNP PARIBAS'
dir_path = os.path.join(os.path.abspath(os.pardir), dir_name)

pdf_files = []

for (dirpath, dirnames, filenames) in walk(dir_path):
    pdf_files.extend(filenames)
    break

# change here to decide which file to loop
filename = os.path.join(dir_path, pdf_files[0])

pdfFileObj = open(filename,'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

num_pages = pdfReader.numPages
count = 0
text = ""

# To convert simple, text-based PDF files into text readable by Python
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

if text != "":
   text = text
else:
   # To convert non-trivial, scanned PDF files into text readable by Python
   text = textract.process(filename, method='tesseract', language='eng')

tokens = word_tokenize(text)

punctuations = ['(',')',';',':','[',']',',']

stop_words = stopwords.words('english')

keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
################################################################################

############################## Get All Names ###################################
model_name = 'stanford-ner/english.all.3class.distsim.crf.ser.gz'
jar_name = 'stanford-ner/stanford-ner.jar'
model_path = os.path.join(os.path.abspath(os.curdir), model_name)
jar_path = os.path.join(os.path.abspath(os.curdir), jar_name)
st = StanfordNERTagger(model_path, jar_path, encoding='utf8')

tags = st.tag(keywords)
people = [tag for tag in tags if tag[1]=='PERSON']
################################################################################
