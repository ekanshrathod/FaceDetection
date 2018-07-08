import urllib
import cv2
import numpy as np
import sqlite3

detector=cv2.CascadeClassifier('Classifier/haarcascade_frontalface_default.xml');
url='http://10.102.36.217:8080/shot.jpg'

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="select * from people where id="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="update people set name='"+srt(Name)+"' where id="+srt(Id)
    else:
        cmd="insert into people(id,name) values("+str(Id)+",'"+str(Name)+"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()

id=raw_input('enter user id')
name=raw_input('enter your name')
insertOrUpdate(id,name)
sampleNum=0
while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        #incrementing sample number
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x-50,y-50),(x+w+50,y+h+50),(0,255,0),2)
        
    # all the opencv processing is done here

    cv2.imshow('face',img)
    cv2.waitKey(100)
    if sampleNum>20:
        break
cv2.destroyAllWindows()
