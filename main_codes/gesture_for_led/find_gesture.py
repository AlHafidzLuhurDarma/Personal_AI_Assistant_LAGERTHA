import pickle
import time
import cv2
import numpy as np
import pickle

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands)
    def Marks(self,frame):
        myHands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands
def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    palmSize=((handData[0][0]-handData[9][0])**2+(handData[0][1]-handData[9][1])**2)**(1./2.)
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            distMatrix[row][column]=(((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.))/palmSize
    return distMatrix
def findError(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    return error
def findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol):
    errorArray=[]
    for i in range(0,len(gestNames),1):
        error=findError(knownGestures[i],unknownGesture,keyPoints)
        errorArray.append(error)
    errorMin=errorArray[0]
    minIndex=0
    for i in range(0,len(errorArray),1):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture='Unknown'
    return gesture

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(1)
time.sleep(5)
keyPoints=[0,4,5,9,13,17,8,12,16,20]
train=False
tol=10
trainCnt=0
with open('Satu.txt', 'rb') as f:
    Satu = pickle.load(f)
with open('Dua.txt', 'rb') as f:
    Dua = pickle.load(f)
with open('Tiga.txt', 'rb') as f:
    Tiga = pickle.load(f)
with open('Empat.txt', 'rb') as f:
    Empat = pickle.load(f)
with open('Lima.txt', 'rb') as f:
    Lima = pickle.load(f)
with open('Konfirmasi.txt', 'rb') as f:
    Konfirmasi = pickle.load(f)

knownGestures=[Satu,Dua,Tiga,Empat,Lima,Konfirmasi]
gestNames=['Satu','Dua','Tiga','Empat','Lima','Konfirmasi']
cmd = 'pass'

while True:
    ignore,  frame = cam.read()
    handData=findHands.Marks(frame)
    if train == False:
        if handData!=[]:
            unknownGesture=findDistances(handData[0])
            myGesture=findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol)
            #error=findError(knownGesture,unknownGesture,keyPoints)
            if myGesture == 'Unknown':
                myGesture = myGesture2
            myGesture2 = myGesture
            cv2.putText(frame,myGesture,(100,175),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
            cmd = myGesture + '\r'
            if myGesture == 'Konfirmasi':
                break
    for hand in handData:
        for ind in keyPoints:
            cv2.circle(frame,hand[ind],10,(255,0,255),3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()