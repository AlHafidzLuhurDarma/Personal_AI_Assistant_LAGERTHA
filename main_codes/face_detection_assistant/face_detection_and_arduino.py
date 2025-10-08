import cv2
import serial
print(cv2.__version__)

arduinoData = serial.Serial('com3', 9600)
cmd = 'no_data\r'

face_cascade = cv2.CascadeClassifier(r'C:\Users\user\Documents\pythonFiles\face_detection_openCV\haar\haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

height = 360
width = 640                                                                             
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    ignore, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if faces != ():
        cmd = 'face\r'
        x, y, widthRectangle, heightRectangle = faces[0]
        cv2.rectangle(frame, (x,y), (x+widthRectangle, y+heightRectangle), (255, 0,0), 2)
        arduinoData.write(cmd.encode())
        while (arduinoData.inWaiting()==0):  # there's automatication from python 'in_waiting' BUT we use 'inWaiting'
            pass
        dataPacket = arduinoData.readline()  # read the data
        dataPacket=str(dataPacket,'utf-8')   # change the data type from byte to string
        dataPacket=dataPacket.strip('\r\n')  # remove the ('\r\n') or the carriage return and the new line character
        if dataPacket == "done":
            print(dataPacket)
            break
    else:
        print('no face')

    #print(cmd)
    #arduinoData.write(cmd.encode())
    cv2.imshow('MY CAM', frame)
    cv2.moveWindow('MY CAM', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

# off
# if face detected = fingerprints on with the red light
# face detection is off
# if fingerprint is correct = green light

# print("finger print is confirmed")