import cv2
import numpy as np

# Opens the Video file
cap= cv2.VideoCapture('capture.mp4')
i=0
ret, frame_prev = cap.read()
cv2.imwrite('original/ss0.png',frame_prev)
i=1
while(cap.isOpened()):
    ret, frame_cur = cap.read()
    if ret == False:
        break
    diff = cv2.absdiff(frame_prev,frame_cur)
    mean_diff = np.mean(diff)
    if mean_diff > 3:
        cv2.imwrite('original/ss'+str(i)+'.png',frame_cur)
        frame_prev = frame_cur
    i+=1

cap.release()
cv2.destroyAllWindows()
