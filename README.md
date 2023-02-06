# maplestory-culvert-flag-score-extractor
Extracts guild's IGNs, Culvert, and Flag Race numbers from video of member participation status by using Tesseract OCR and Python

## STEPS
### 1. TESSERACT OCR
Install Tesseract OCR https://github.com/tesseract-ocr/tessdoc#binaries

### 2. Recording
Record a scrolling cropped video from top of the list and bottom by scrolling. Make sure the cursor doesn't show up and there are no headers or extra space, like shown below, and save it in culver-flag-parser folder. If the video isn't in HD there is a higher chance mistakes occur in numbers. Works best in 1920x1080. May need to increase resizing if it's in a lower resolution, resulting in longer runtime.

![](https://github.com/j3li/maplestory-culvert-flag-parser/blob/main/recording%20example.gif)

### 3. Running the Code
First, fill `names_list.txt` with the IGNs of everyone in the guild.

Run `screenshot.py` to generate the screenshots of every page in the video.

Run `parsing.py`. This will extract all the text from the images.

`log.txt` will have the unfiltered results of everything that gets parsed. `results.csv` will have results filtered to only have **IGN | Culvert | Flag Race**.

`errors.csv` will have IGNs that could not be matched for debugging and manual solving.

