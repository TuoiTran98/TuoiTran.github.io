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

import wx
#import mysql
from main_frame import MainFrame , Getdata
import mysql.connector
wildcard = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
         "All files (*.*)|*.*"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/DoAnTotNghiep/TuoiTran.github.io/recognizer/trainingData.yml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360) 
font = cv2.FONT_HERSHEY_DUPLEX

# truy xuat id trong db
def getProfile(id):

    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')
    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    cusror = conn.cursor()
    # query = "SELECT * FROM face WHERE id="+ str(id)
    # cusror = conn.execute(query)

    # select database
    cusror.execute("SELECT * FROM employee WHERE id="+ str(id))
    result = cusror.fetchall()

    profile = None

    for x in result:
        profile = x
    conn.close()
    return profile
def add(id_name, date, name, start_time, gender, dateofbirth, phonenumber):

    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    cusror = conn.cursor()

    # query = "SELECT * FROM Timekeeping WHERE id="+ str(id)
    # cusror = conn.execute(query)

    # select  database
    cusror.execute("SELECT * FROM Timekeeping WHERE id_name="+ str(id_name))
    result = cusror.fetchall()

    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
        cusror.execute("INSERT INTO Timekeeping(id_name, date, name, start_time, gender, dateofbirth, phonenumber) VALUES("+ str(id_name) + ",'"+ str(date)+"','"+ str(name)+"', '"+ str(start_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')")
        print('add')
        
    else :
        cusror.execute("INSERT INTO Timekeeping( id_name, date, name, start_time, gender, dateofbirth, phonenumber) VALUES("+str(id_name)+",'"+ str(date)+"', '"+ str(name)+"', '"+ str(start_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')")            
        print('addupdate')  
    # result.execute(query)
    conn.commit()
    conn.close()

def InsertUpdateData(id, name, gender, dateofbirth, phonenumber):
    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="facedetection")
    cusror = conn.cursor()
    # select database
    cusror.execute("SELECT * FROM employee WHERE id="+ str(id))
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
    # result.execute(query)
    conn.commit()
    conn.close()

def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceimg = Image.open(imagePath).convert('L')

        faceNp = np.array(faceimg, 'uint8')
        print(faceNp)


        Id =int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(Id)

        cv2.namedWindow('Training',cv2.WINDOW_AUTOSIZE)
        processed_img = cv2.resize(faceNp, (120, 80))
        cv2.imshow('Training', processed_img)

        if(cv2.waitKey(100) == ord('q')):
            break

    return faces, IDs

class frame(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)
    def mainframeOnClose( self, event ):
        cap.release()
        cv2.destroyAllWindows()
        dialog.Destroy()
        self.Destroy()
    def m_button_runOnButtonClick(self, event):
        index  = 0
        while(True):
            index += 1
            ret, frame = cap.read()
            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                frame_gray,
                1.1 , 4)

            print(faces)
            
            for(x,y,w,h) in faces:
                cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (255 ,0 , 0), 2)
                roi_gray = frame_gray[y: y+h, x: x+w]
                id, confidence =  recognizer.predict(roi_gray)

                if confidence < 60:
                    profile = getProfile(id)
                    if(profile != None):

                        now = datetime.now()
                        dt_string_day = now.strftime("%m/%d/%Y")
                        start_time = now.strftime("%H:%M:%S")
                        
                        # cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (43, 41 ,182), 2)
                        cv2.putText(frame_gray, "" +str(id), (x, y + h + 30), font, 1, (255 ,0 , 0), 1)
                        cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (255 ,0 , 0), 1)
                        cv2.putText(frame_gray, "" +str(confidence), (x, y), font, 1, (255 ,0 , 0), 2)
                        if index >  20 :
                            add(str(id), str(dt_string_day) , str(profile[1]), str(start_time), str(profile[2]) ,str(profile[3]) , str(profile[4]) )
                            index = 0
                        # cv2.putText(frame_gray, "Successful !", (x, y), font, 1, (43, 41 ,182), 1)
                else:
                    cv2.putText(frame_gray, "Unknow", (x + 10, y + h + 30), font, 1, (255 ,0 , 0), 1)
            

            cv2.namedWindow('processed',cv2.WINDOW_AUTOSIZE)
            processed_img = cv2.resize(frame_gray, (360, 240))
            cv2.imshow('processed', processed_img)
            if(cv2.waitKey(100) == ord('q')):
                break
         
        cv2.destroyAllWindows()
 
    def m_button_train_datasetOnButtonClick( self, event ):
        path = 'dataSet'
        getImageWithID(path)

        faces, Ids = getImageWithID(path)
        recognizer.train(faces, np.array(Ids))
        if not os.path.exists('recognizer'):
            os.makedirs('recognizer')
        recognizer.save('recognizer/trainingData.yml')
        cv2.destroyAllWindows        
    def m_button_create_datasetOnButtonClick( self, event ):
        dialog.Show()

class getdata(Getdata):
    def __init__(self, parent):
        Getdata.__init__(self, parent)
    def m_sdbSizerOnCancelButtonClick( self, event ):
        event.Skip()
    def m_sdbSizerOnOKButtonClick(self, event):
        id = self.id_textCtrl.GetLineText(0)
        name = self.name_textCtrl.GetLineText(0)
        gender = self.gender_textCtrl.GetLineText(0)
        dateofbirth = self.date_textCtrl.GetLineText(0)
        phonenumber = self.phone_textCtrl.GetLineText(0)

        if id == "" and name == "" and gender =="" and dateofbirth=="" and phonenumber == "":
            wx.MessageBox("err !")
        else:
            InsertUpdateData(id, name, gender, dateofbirth, phonenumber)
            sampleNum =0
            while(True):

                ret, frame = cap.read()
                frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(
                    frame_gray,
                    1.1 , 4)
                for(x,y,w,h) in faces:
                    cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (255 ,0 , 0), 2)

                    if not os.path.exists('dataSet'):
                        os.makedirs('dataSet')
                    
                    sampleNum += 1

                    cv2.imwrite('dataSet/User.' + str(id) + '.' + str(sampleNum) + '.jpg', frame_gray[y : y+h, x: x+w])
                cv2.namedWindow('face',cv2.WINDOW_AUTOSIZE)
                processed_img = cv2.resize(frame_gray, (120, 80))
                cv2.imshow('face', frame_gray)

                cv2.waitKey(100)
                if  sampleNum > 50 :
                    cv2.destroyAllWindows()
                    wx.MessageBox("Successul !")
                    break
app = wx.App()
#-------------------------------
frame = frame(None)
dialog = getdata(None)
#-------------------------------
frame.Show()
#-------------------------------
app.MainLoop()
print('OK')

