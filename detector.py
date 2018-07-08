import urllib
import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

url='http://10.164.57.139:8080/shot.jpg'
rec=cv2.createLBPHFaceRecognizer()
rec.load("recognizer/trainningData.yml")
cascadePath="Classifier/haarcascade_frontalface_default.xml"
detector=cv2.CascadeClassifier(cascadePath);
path='dataSet'

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="select * from people where id="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

id=0
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,2,1,0,2)
while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+30),font,(0,255,0))
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+60),font,(0,255,0))
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[3]),(x,y+h+90),font,(0,255,0))
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[4]),(x,y+h+120),font,(0,255,0))
        
    # all the opencv processing is done here

    cv2.imshow('face',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)
cv2.destroyAllWindows()
