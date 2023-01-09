# -*- coding: utf-8 -*-
import PIL
from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np
import glob
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
  
# Path to Tesseract, should install in the directory below for simplicity
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
# Put path to list of IGNS here
path_to_igns = "names_list.txt"

text = ""
i=0

# Read list of IGNs
igns = open(path_to_igns, "r")
list_of_igns = igns.read()
list_of_igns = list_of_igns.splitlines()
# Iterating through every screenshot that was taken and performing
# image processing to make the images easier to parse
for x in glob.glob("original/*.png"):
    img = cv2.imread(x)
    # Resizing and making the images bigger
    img = cv2.resize(img, None, fx=5, fy=5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying Gaussian blur
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # Using Otsu thresholding to binarize, partitions image into foreground
    # and background
    retval, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # Applying erosion
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite('parses/processed'+str(i)+'.png', img)
    i+=1
    # Extract text from the images and put it all into one string,
    # I found psm 6 to be the best at parsing the columns and 
    # putting the data into rows
    text += pytesseract.image_to_string(img, config='--psm 6 -l eng+ces+fra+spa') + "\n"

# Writes unfiltered results to log.txt
with open('log.txt', "w", encoding="utf-8") as f:
    f.write(text)

# Formatting to prepare to extract data
array = text.splitlines()

# Remove empty entries
array = list(filter(None, array))

seen_igns = []
res = []
errors = []

# Extracts IGN, Culvert, and Flag Race numbers and compares parsed
# IGN to the list of IGNs in the guild and finds the most similar match
for x in range(0, len(array)):
    array[x] = array[x].split()
    ign = array[x][0]
    match, percent = process.extractOne(ign, list_of_igns)
    # Makes sure there are no dupes, in case multiple screenshots were taken
    # of the same set of memebrs and IGNs match by 70%, if not then send to errors
    if match not in seen_igns and percent > 70:
        # Appends matched IGNs in format IGN Culvert Flag
        res.append([match, array[x][-2], array[x][-1]])
        seen_igns.append(match)
    else:    # Put IGNS that couldn't be matched into a list for debugging/manual solving
        errors.append(array[x])

# Write list of results to results.csv
results = ""
for x in res:
    results+= " ".join(x)
    results+= "\n"
results = results.replace('.', ',')
results = results.replace('1]', '0')
results = results.replace('1}', '0')
with open('results.csv', "w") as f:
    f.write(results)

# Write list of errors to errors.csv
errors_s = ""
for x in errors:
    errors_s+= " ".join(x)
    errors_s+= "\n"
with open('errors.csv', 'w') as f:
    f.write(errors_s)
