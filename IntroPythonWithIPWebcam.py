import urllib
import cv2
import numpy as np

detector=cv2.CascadeClassifier('Classifier/haarcascade_frontalface_default.xml');
url='http://10.11.46.231:8080/shot.jpg'

while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # all the opencv processing is done here

    cv2.imshow('face',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)
cv2.destroyAllWindows()
