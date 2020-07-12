"""import cv2
import numpy as np
import sqlite3
import os
# import mysql.connector


def insertOrUpdate(id, name, gender, dateofbirth, phonenumber):
    # conn = sqlite3.connect('/DoAnTotNghiep/TuoiTran.github.io/databaseface.db')

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    cusror = conn.cursor()
    # select dữ liệu từ database
    cusror.execute("SELECT * FROM face WHERE id="+ str(id))
    # tìm nạp các hàng từ đối tượng con trỏ  
    result = cusror.fetchall()
    # query = "SELECT * FROM face WHERE id="+ str(id)
    # cusror = conn.execute(query)
    
    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
        cusror.execute("INSERT INTO employee(id, name, gender, dateofbirth, phonenumber) VALUES("+ str(id) + ",'"+str(name)+"','"+str(gender)+"','"+str(dateofbirth)+"','"+str(phonenumber)+"')")
        
    else:
        cusror.execute("UPDATE employee SET name='" + str(name) + "', gender='" + str(gender) + "' , dateofbirth='" + str(dateofbirth) + "', phonenumber='" + str(phonenumber) + "'WHERE id="+str(id))
    # cusror.execute(query)
    conn.commit()
    conn.close()

#load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')
# m_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye_tree_eyeglasses.xml')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#insert to db
id = input("Enter your ID: ")
name = input("Enter your NAME: ")
gender = input("Enter your GENDER: ")
dateofbirth = input("Enter your DATE OF BIRTH: ")
phonenumber = input("Enter your PHONE NUMBER: ")

insertOrUpdate(id, name, gender, dateofbirth, phonenumber)

sampleNum = 0

while(True):

    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        frame_gray,
        1.1 , 4)
    # r_faces = m_face_cascade.detectMultiScale(frame, 1.1 , 4)
    for(x,y,w,h) in faces:

        # roi_gray = frame_gray[y: y+h, x: x+w]
        # roi_color = frame[y:y+h, x:x+w]

        cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (255 ,0 , 0), 2)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        
        sampleNum += 1

        cv2.imwrite('dataSet/User.' + str(id) + '.' + str(sampleNum) + '.jpg', frame_gray[y : y+h, x: x+w])
    
                    #     eyes = m_face_cascade.detectMultiScale(roi_gray)
                    #     for(ex,ey,ew,eh) in eyes:

                    #         # roi_gray = frame_gray[y: y+h, x: x+w]
                    #         cv2.rectangle(roi_color,(ex,ey),(ex+ew, ey+eh), (255 ,0 , 0), 2)
                            
                    #         if not os.path.exists('dataSet'):
                    #             os.makedirs('dataSet')
                            
                    #         sampleNum1 += 1

                    #         cv2.imwrite('dataSet/User.' + str(id) + '.r' + str(sampleNum) + '.jpg', frame_gray[y : y+h, x: x+w])
                    # resized = cv2.resize(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2))) 
    cv2.namedWindow('face',cv2.WINDOW_AUTOSIZE)
    processed_img = cv2.resize(frame_gray, (360, 240))
    cv2.imshow('face', frame_gray)
   # cv2.imshow('face', processed_img)
    cv2.waitKey(50)

    if  sampleNum > 50 :
        break
cap.release()
cv2.destroyAllWindows()
"""