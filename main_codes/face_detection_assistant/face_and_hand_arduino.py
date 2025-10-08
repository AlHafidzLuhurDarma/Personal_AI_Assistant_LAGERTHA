import cv2
import serial
import pygame
print(cv2.__version__)

arduinoData = serial.Serial('com3', 9600)
#cmd = 'off\r'

face_cascade = cv2.CascadeClassifier(r'C:\Users\user\Documents\pythonFiles\face_detection_openCV\haar\haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

height = 360
width = 640                                                                             
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

identity_checking = True

while True:
    ignore, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if identity_checking == True:
        if faces != ():
            cmd = 'face\r'
            #x, y, widthRectangle, heightRectangle = faces[0]
            #cv2.rectangle(frame, (x,y), (x+widthRectangle, y+heightRectangle), (255, 0,0), 2)
            arduinoData.write(cmd.encode())
            identity_checking = False
            pygame.mixer.init()
            pygame.mixer.music.load('face_detected.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(1000)
        else:
            #cmd = "no face\r"
            print('no face')
            #arduinoData.write(cmd.encode())
    else:
        print("Hello!!!!!!!!")
    #print(cmd)
    #arduinoData.write(cmd.encode())
    cv2.imshow('MY CAM', frame)
    cv2.moveWindow('MY CAM', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
