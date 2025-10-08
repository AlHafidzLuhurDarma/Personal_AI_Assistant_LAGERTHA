import openai
import datetime as dt
import requests
import pygame
import gtts
import text_parameter
from twilio.rest import Client
import cv2
import serial
import pickle
import time
import numpy as np
'''
function in order:
-Speech maker
-Weather info
'''

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

def speech_maker(text, number):
    speech = gtts.gTTS(text)
    name_file = (f"Lagertha_Voice_{number}.mp3")
    speech.save(name_file)
    return name_file
def weather_information(latitude, longitude, key):
    # main program to request weather API
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}"
    response = requests.get(url).json()

    # Information we get
    temp_kelvin = response['main']['temp']
    temp_celcius = temp_kelvin - 273.15
    temp_fahrenheit = temp_celcius * (9/5) + 32
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celcius = feels_like_kelvin - 273.15
    feels_like_fahrenheit = temp_celcius * (9/5) + 32
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    text = f"Here's the Current Weather Information    .The Temperature is {temp_celcius:.2f}°Celcius or {temp_fahrenheit:.2f}°Fahrenheit , The Humidity is {humidity}%, The Temperature Feels Like is {feels_like_celcius:.2f}°Celsius or {feels_like_fahrenheit:.2f}°Fahrenheit, The average Wind Speed is {wind_speed}m/s, and the General Weather is {description}, Sun rises at = {sunrise_time} local time ,Sun sets at = {sunset_time} local time"
    return text

def face_detection_mode(camera, detect):
    ignore, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if faces != ():
        cmd = 'face\r'
        x, y, widthRectangle, heightRectangle = faces[0]
        cv2.rectangle(frame, (x,y), (x+widthRectangle, y+heightRectangle), (255, 0,0), 2)
        detect += detect
    else:
        cmd = 'no_data\r'
    cv2.imshow('MY CAM', frame)
    cv2.moveWindow('MY CAM', 0,0)
    return detect

def lagertha_voices(file_source):
    pygame.mixer.init()
    pygame.mixer.music.load(file_source)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(10)

'''
Parameter in order:
- Arduino
- Weather
- Whatsapp
- Open-AI
- cv2 face detection and hand gesture for LED
- 
'''

#arduinoData = serial.Serial('com3', 9600)
#cmd = 'no_data\r'

#Weather parameter
lat = -7.8111057
lon = 112.0046051
api_key = "e56f335aa287e580bceb37a61532557e"

#Whatsapp parameter
account_sid = 'AC436dc8e7e32b41776d0abc4568ec406b'
auth_token = '973572e76e47ea3b23a30a942e4cabe8'
client = Client(account_sid, auth_token)

#Open AI parameter
openai.api_key = "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"
messages = []
messages.append({"role" : "system", "content" : "An AI named Lagertha that always have simple answer"})

#cv2 Parameter
face_cascade = cv2.CascadeClassifier(r'C:\Users\user\Documents\pythonFiles\face_detection_openCV\haar\haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
height = 360
width = 640
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# gesture for LED
time.sleep(5)
keyPoints=[0,4,5,9,13,17,8,12,16,20]
train=False
tol=20
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
new_gesture = 'off'
old_gesture = ''
findHands=mpHands(1)

arduinoData = serial.Serial('com3', 9600)  
cmd = 'off\r'


# General parameter
number_voice = 1
gpt = True
lagertha_interaction = False
face_detect = False

print("Lagertha is ready!!")
while True:
    if face_detect == True:
        while True:
            ignore, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            if faces != ():
                break
        cam.release()
        cv2.destroyAllWindows()
        lagertha_voices(r"C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\face_detected.mp3")
        identity_confirmation = input('')
        if identity_confirmation == 'start':
            lagertha_voices(r"C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\fingerprint_confirmation.mp3")
            face_detect = False
            gpt = True


    message = input("")
    number_voice += 1
    keyword_parameter = message.split(" ")
    lagertha_interaction, interaction_file = text_parameter.keyword(keyword_parameter)
    
    if message == 'stop':
        break
    if lagertha_interaction == True:
        gpt = False
        sound_file = interaction_file
    if "information" in keyword_parameter:
        reply = weather_information(lat, lon, api_key)
        speech_maker(reply, number_voice)
        gpt = False
    if "whatsapp" in keyword_parameter and "information" in keyword_parameter:
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=reply,
        to='whatsapp:+6281216937156'
        )
        print("The weather information you requested has been sent to your WhatsApp")
        gpt = False
    if "LED" in keyword_parameter:
        gpt = False
        message = None
        pygame.mixer.init()
        pygame.mixer.music.load("LED_gesture.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
        while True:
            ignore,  frame = cam.read()
            handData=findHands.Marks(frame)
            if train == False:
                if handData!=[]:
                    unknownGesture=findDistances(handData[0])
                    myGesture=findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol)
                    cv2.putText(frame,myGesture,(100,175),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
                    if myGesture == "Konfirmasi":
                        break
                    if myGesture == "Unknown":
                        myGesture = old_gesture
                    new_gesture = myGesture
                    cmd_gesture = new_gesture+'\a'
                    if new_gesture != old_gesture:
                        print("cmd_gesture = ",cmd_gesture)
                        arduinoData.write(cmd_gesture.encode())
                    old_gesture = new_gesture
            for hand in handData:
                for ind in keyPoints:
                    cv2.circle(frame,hand[ind],10,(255,0,255),3)
            cv2.imshow('my WEBcam', frame)
            cv2.moveWindow('my WEBcam',0,0)
        cv2.destroyAllWindows()
        sound_file = r"C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\LED_Confirmation.mp3"

    if "humidity" in keyword_parameter:
        gpt = False
        cmd = "humidity\a"
        lagertha_interaction = True
        arduinoData.write(cmd.encode())
        while (arduinoData.inWaiting()==0):
            pass
        dataPacket = arduinoData.readline()  
        dataPacket=str(dataPacket,'utf-8')   
        dataPacket=dataPacket.strip('\r\n') 
        print(dataPacket)
        humidity_speech = speech_maker(dataPacket, 99)
        sound_file = humidity_speech

    if gpt == True:
        messages.append({"role" : "user", "content" : message})
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role" : "assistant", "content": reply})
       
    # Speech
    if lagertha_interaction == False:
        print(reply)
        sound_file = speech_maker(reply, number_voice)
    lagertha_voices(sound_file)
    gpt = True
    lagertha_interaction = False