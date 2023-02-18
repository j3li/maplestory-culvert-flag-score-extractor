from flask import Flask, render_template, request, redirect
import os
import cv2
import numpy as np
import PIL
from PIL import Image
from pytesseract import pytesseract
import glob
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from werkzeug.utils import secure_filename

app = Flask(__name__)
upload_folder = "uploads/"
app.config['UPLOAD_FOLDER'] = upload_folder
@app.route("/", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        ign = request.files['ign']
        vid = request.files['vid']
        if ign.filename == '' or vid.filename == '':
            return redirect(request.url)
        ign.filename = 'ign.txt'
        vid.filename = 'vid.mp4'
        ign_filename = secure_filename(ign.filename)
        vid_filename = secure_filename(vid.filename)
        ign.save(os.path.join(app.config['UPLOAD_FOLDER'], ign_filename))
        vid.save(os.path.join(app.config['UPLOAD_FOLDER'], vid_filename))

    cap = cv2.VideoCapture('uploads/vid.mp4')
    i=0
    ret, frame_prev = cap.read()
    cv2.imwrite('uploads/images/ss0.png',frame_prev)
    i=1
    while(cap.isOpened()):
        ret, frame_cur = cap.read()
        if ret == False:
            break
        diff = cv2.absdiff(frame_prev,frame_cur)
        mean_diff = np.mean(diff)
        if mean_diff > 3:
            cv2.imwrite('uploads/images/ss'+str(i)+'.png',frame_cur)
            frame_prev = frame_cur
        i+=1

    cap.release()
    cv2.destroyAllWindows()


    path_to_tesseract = r"Tesseract-OCR/tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    # Put path to list of IGNS here
    path_to_igns = "uploads/ign.txt"

    text = ""
    i=0

    # Read list of IGNs
    igns = open(path_to_igns, "r")
    list_of_igns = igns.read()
    list_of_igns = list_of_igns.splitlines()
    # Iterating through every screenshot that was taken and performing
    # image processing to make the images easier to parse
    for x in glob.glob("uploads/images/*.png"):
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
        cv2.imwrite('uploads/extracted/processed'+str(i)+'.png', img)
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
    dupes = []

    # Extracts IGN, Culvert, and Flag Race numbers and compares parsed
    # IGN to the list of IGNs in the guild and finds the most similar match
    for x in range(0, len(array)):
        array[x] = array[x].split()
        ign = array[x][0]
        match, percent = process.extractOne(ign, list_of_igns)
        # Makes sure there are no dupes, in case multiple screenshots were taken
        # of the same set of members and IGNs match by 70%, if not then send to errors
        if match not in seen_igns and percent > 70:
            # Appends matched IGNs in format IGN Culvert Flag
            res.append([match, array[x][-2], array[x][-1]])
            seen_igns.append(match)
        # Duped IGNS
        elif match in seen_igns:
            dupes.append(array[x])
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

    # Write list of dupes to dupes.csv
    dupes_s = ""
    for x in dupes:
        dupes_s+= " ".join(x)
        dupes_s+= "\n"
    with open('dupes.csv', 'w') as f:
        f.write(dupes_s)

    return render_template('done.html')

@app.route("/", methods=['GET'])
def land():
    return render_template('main.html')

app.run(port=5000)