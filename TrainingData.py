import cv2
import numpy as np
import os
from PIL import Image


recognizer = cv2.face.LBPHFaceRecognizer_create()

path = 'dataSet'

def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceimg = Image.open(imagePath).convert('L')

        faceNp = np.array(faceimg, 'uint8')
        print(faceNp)

        # Id = int(imagePath.split('\\')[1].split('.')[1])
        Id =int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(Id)

        cv2.namedWindow('Training',cv2.WINDOW_AUTOSIZE)
        processed_img = cv2.resize(faceNp, (48, 48))
        cv2.imshow('Training', processed_img)
        #cv2.imshow('Train', faceNp)
        if(cv2.waitKey(100) == ord('q')):
            break

    return faces, IDs

faces, Ids = getImageWithID(path)

recognizer.train(faces, np.array(Ids))

if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainingData.yml')

cv2.destroyAllWindows



getImageWithID(path)