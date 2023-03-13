# maplestory culvert & flag extractor

![](https://github.com/j3li/maplestory-culvert-flag-score-extractor/blob/main/cfscore.png)

Extracts IGNs, Culvert, and Flag Race scores from video of member participation status by using **Tesseract OCR** and **Python** 
## STEPS
### 1. INSTALLING TESSERACT OCR
**Option 1:** Download [Teseract OCR with tessdata_best already installed](https://www.dropbox.com/s/2m97m85bl8wsb18/Tesseract-OCR.zip?dl=0) and unzip into **maplestory-culvert-flag-score-extractor** folder.

**Option 2**: Download [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) and [tessdata_best](https://github.com/tesseract-ocr/tessdata_best). Put tessdata_best files into tessdata. Then change line 50 in `app.py` to 
```python
path_to_tesseract = r"PATH/TO/YOUR/tesseract.exe"
```

### 2. Recording IGNs and Video
Create a `.txt` file with the IGNs of everyone in the guild.

Record a scrolling cropped `.mp4` video from top of the list and bottom by scrolling. Make sure the cursor doesn't show up and there are no headers or extra space, like shown below. If the video isn't in HD there is a higher chance mistakes occur in numbers. Works best in 1920x1080. May need to increase resizing if it's in a lower resolution, resulting in longer runtime.

(You can scroll a lot faster than the gif. Shorter video = shorter procesing time.)

![](https://github.com/j3li/maplestory-culvert-flag-parser/blob/main/recording%20example.gif)

### 3. Running the Code
Navigate to **maplestory-culvert-flag-score-extractor** and run `python app.py` in terminal and open the website at `http://127.0.0.1:5000`. Upload the IGNs list and the recording.

`log.txt` will have the unfiltered results of everything extracted. `results.csv` will have results filtered to only have **IGN | Culvert | Flag Race**.

`errors.csv` will have IGNs that could not be matched for debugging and manual solving.

