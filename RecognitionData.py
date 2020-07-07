import cv2
import numpy as np
import os
import sqlite3
from PIL import Image
import time
import datetime as dt
import csv
import pandas as pd
from datetime import datetime, timedelta
# import mysql.connector

#training nhận diện khuôn mặt và các thư viên hỗ trợ

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')
# m_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye_tree_eyeglasses.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('/DoAnTotNghiep/TuoiTran.github.io/recognizer/trainingData.yml')

# truy xuất id trong db

def getProfile(id):
    conn = sqlite3.connect('/DoAnTotNghiep/TuoiTran.github.io/databaseface.db')
    # conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    # cusror = conn.cursor()
    query = "SELECT * FROM face WHERE id="+ str(id)
    cusror = conn.execute(query)

    # select dữ liệu từ database
    # cusror.execute("SELECT * FROM face WHERE id="+ str(id))
    # result = cusror.fetchall()

    profile = None

    for x in cusror:
        profile = x
   
    conn.close()
    return profile

def add(id, date, name, start_time, gender, dateofbirth, phonenumber):

    conn = sqlite3.connect('/DoAnTotNghiep/TuoiTran.github.io/databaseface.db')

    # conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    # cusror = conn.cursor()

    query = "SELECT * FROM Timekeeping WHERE id="+ str(id)
    cusror = conn.execute(query)

    # select dữ liệu từ database
    # cusror.execute("SELECT * FROM Timekeeping WHERE id="+ str(id))

    # tìm nạp các hàng từ đối tượng con trỏ  
    # result = cusror.fetchall()
    with open('output.csv','w+') as out_csv_file:
        csv_out = csv.writer(out_csv_file)                        
        csv_out.writerow([d[0] for d in cusror.description])

        isRecorExist = 0 
        for x in cusror:
            csv_out.writerow(x)
            isRecorExist = 1
        if(isRecorExist == 0):
            query = "INSERT INTO Timekeeping(id, date, name, start_time, gender, dateofbirth, phonenumber) VALUES("+ str(id) + ",'"+ str(date)+"','"+ str(name)+"', '"+ str(start_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')"
            
            print('add')

        else :
            # lấy data từ bảng timepeeking lên để so sánh với dữ liệu hiện tại
            query = "SELECT * FROM Timekeeping where id="+str(id)
            conn.row_factory = sqlite3.Row
            cusror = conn.execute(query)
            rows = cusror.fetchall()
            for row in rows:
                print ((row["date"] , row["id"]))
                print("autoID",row["autoID"])
                print("id=",str(id))
                if (str(id) != row["id"]):
                    query = "INSERT INTO Timekeeping( id, date, name, start_time, gender, dateofbirth, phonenumber) VALUES("+str(id)+",'"+ str(date)+"', '"+ str(name)+"', '"+ str(start_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')"   
                    print('addupdate')
    cusror.execute(query)
    conn.commit()
    conn.close()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) 

font = cv2.FONT_HERSHEY_DUPLEX
index = 0
while(True):
    index += 1
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        frame_gray,
        1.1 , 4)
    # r_faces = m_face_cascade.detectMultiScale(frame, 1.1 , 4)
    print(faces)
    
    for(x,y,w,h) in faces:
        # org
        #org = (x, y)
        cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (43, 41 ,182), 2)
        #cv2.putText(frame_gray, 'Tuoi', org , font, fontScale ,color, thickness, cv2.LINE_AA)

        roi_gray = frame_gray[y: y+h, x: x+w]
        id, confidence =  recognizer.predict(roi_gray)

        if confidence < 60:
            profile = getProfile(id)
            if(profile != None):

                now = datetime.now()
                dt_string_day = now.strftime("%m/%d/%Y")
                start_time = now.strftime("%H:%M:%S")
                
                # cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (43, 41 ,182), 2)
                cv2.putText(frame_gray, "" +str(id), (x, y + h + 30), font, 1, (43, 41 ,182), 1)
                cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (43, 41 ,182), 1)
                # cv2.putText(frame_gray, "" +str(day), (x, y), font, 1, (43, 41 ,182), 2)
                # 2s se lưu dữ liệu 1 lần
                if index >  20 :
                    add(str(id), str(dt_string_day) , str(profile[1]), str(start_time), str(profile[2]) ,str(profile[3]) , str(profile[4]) )
                    index = 0
        else:
            cv2.putText(frame_gray, "no Data", (x + 10, y + h + 30), font, 1, (43, 41 ,182), 1)
    

    cv2.namedWindow('processed',cv2.WINDOW_AUTOSIZE)
    processed_img = cv2.resize(frame_gray, (360, 240))
    cv2.imshow('processed', processed_img)
    if(cv2.waitKey(100) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()









