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
from main_frame import MainFrame , Getdata
import mysql.connector

wildcard = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
         "All files (*.*)|*.*"

# 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

# Tập dữ liệu training
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/DoAnTotNghiep/TuoiTran.github.io/winform_python/recognizer/trainingData.yml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
font = cv2.FONT_HERSHEY_DUPLEX

# truy xuat id trong db
def getProfile(id):

    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')
    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
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
# thêm dữ liệu vào bảng timekeeping
def add(id, id_name, date, start_time,end_time):

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
    cusror = conn.cursor()

    cusror.execute("SELECT * FROM Timekeeping WHERE id_name="+ str(id_name))
    result = cusror.fetchall()
    
    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
        # thêm dữ liệu mới
        cusror.execute("INSERT INTO Timekeeping(id_name, date, start_time, end_time) VALUES("+ str(id_name) + ",'"+ str(date)+ "', '"+ str(start_time)+"','"+ str(end_time)+"')")
        print('add_employee')
        
    else :
        # so sánh ngày, id trong data  với ngày , id xuất hiện để thêm vào data 
        print(str(date))
        print(str(x[2]))
        print(str(id_name))
        print(str(x[1]))
        if ((str(date) != str(x[2]) and str(id_name) == str(x[1]) )):          
            print('add')
            cusror.execute("INSERT INTO Timekeeping(id_name, date, start_time, end_time) VALUES( "+str(id_name)+",'"+ str(date)+"','"+ str(start_time)+"','"+ str(end_time)+"')" )
            
        # cập nhật lại end_time khi người đó đã có trong dư liệu vào ngày hôm đó
        else :
            cusror.execute("UPDATE Timekeeping SET  end_time='" + str(end_time) + "' WHERE id_name=" + str(id_name) + " and id="+ str(x[0]) )
            print('update')
    conn.commit()
    conn.close()

# tạo dữ liệu mới vào employee
def InsertUpdateData(id, name, gender, dateofbirth, phonenumber, position, salary):
    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
    cusror = conn.cursor()
    cusror.execute("SELECT * FROM employee WHERE id="+ str(id))
    result = cusror.fetchall()
    
    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
       cusror.execute("INSERT INTO employee(id, name, gender, dateofbirth, phonenumber, position, salary) VALUES("+ str(id) + ",'"+str(name)+"','"+str(gender)+"','"+str(dateofbirth)+"','"+str(phonenumber)+"' ,'"+str(position)+"', '"+str(salary)+"')")
    else:
       cusror.execute("UPDATE employees SET name='" + str(name) + "', gender='" + str(gender) + "' , dateofbirth='" + str(dateofbirth) + "', phonenumber='" + str(phonenumber) + "' , position ='"+str(position)+"' salary ='"+str(salary)+"' WHERE id="+str(id))
    # result.execute(query)
    conn.commit()
    conn.close()

# hàm training
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
        processed_img = cv2.resize(faceNp, (120, 120))
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
    def m_menuItem_exitOnMenuSelection( self, event ):
        cap.release()
        cv2.destroyAllWindows()
        dialog.Destroy()
        self.Destroy()

    def m_menuItem_aboutOnMenuSelection( self, event ):
        wx.MessageBox("Chọn Run để thực hiện chạy chương trình phát hiện khuôn mặt và ghi lại thông tin, nếu chưa có dữ liệu vui lòng chọn Create rồi thực hiện Train.")

    # xử lí lưu data về
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

                if confidence < 100:
                    profile = getProfile(id)
                    if(profile != None):

                        cv2.putText(frame_gray, "" +str(id), (x, y + h + 30), font, 1, (255 ,0 , 0), 1)
                        cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (255 ,0 , 0), 1)
                        
                        now = datetime.now()
                        dt_string_day = now.strftime("%m/%d/%Y")
                        start_time = now.strftime("%H:%M:%S")
                        end_time = now.strftime("%H:%M:%S")

                        # cv2.putText(frame_gray, "" +str(confidence), (x, y), font, 1, (255 ,0 , 0), 2)
                        if index >  15 :
                            
                            add(str(profile[0]),str(id), str(dt_string_day),  str(start_time), str(end_time) ) 
                            cv2.putText(frame_gray, "Done !", (x+190, y+100), font, 1, (255, 0, 0), 2)
                            time.sleep(1)                           
                            index = 0
                else:
                    cv2.putText(frame_gray, "Unknow", (x + 10, y + h + 30), font, 1, (255 ,0 , 0), 1)
            

            cv2.namedWindow('processed',cv2.WINDOW_AUTOSIZE)
            processed_img = cv2.resize(frame_gray, (360, 240))
            cv2.imshow('processed', processed_img)
            if(cv2.waitKey(100) == ord('q')):
                break
         
        cv2.destroyAllWindows()
    #  training data
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
    # tạo mới dữ liệu
    def m_sdbSizerOnOKButtonClick(self, event):
        id = self.id_textCtrl.GetLineText(0)
        name = self.name_textCtrl.GetLineText(0)
        gender = self.gender_textCtrl.GetLineText(0)
        dateofbirth = self.date_textCtrl.GetLineText(0)
        phonenumber = self.phone_textCtrl.GetLineText(0)
        position = self.position_textCtrl.GetLineText(0)
        salary = self.salary_textCtrl.GetLineText(0)

        if id == "" and name == "" and gender =="" and dateofbirth=="" and phonenumber == "" and position == "" and salary == "":
            wx.MessageBox("err !")
        else:
            InsertUpdateData(id, name, gender, dateofbirth, phonenumber, position, salary)
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
                if  sampleNum > 19 :
                    cv2.destroyAllWindows()
                    wx.MessageBox("successful !")
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

