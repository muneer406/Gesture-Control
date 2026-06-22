import cv2
import os
 
path = input("Picture path: ")
img = cv2.imread(f'Family photos/{path}.jpg') #Path of an image
faceCascade = cv2.CascadeClassifier('haarcascade\harrcascade_frontalface_default.xml')
faces = faceCascade.detectMultiScale(img,1.1,10)
 
directory = os.getcwd()+'\\Extracted Photos'
 
try:
    os.mkdir(directory)
except FileExistsError as fee:
    print('Exception Occured: ',fee)
os.chdir(directory)

for (x, y, w, h) in faces:
    FaceImg = img[y:y+h,x:x+w]
    # To save an image on disk
    filename = f'Extracted Photos/Face {path}.jpg'
    cv2.imwrite(filename,FaceImg)