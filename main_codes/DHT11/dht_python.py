import time
import serial

arduinoData = serial.Serial('com3', 9600)
time.sleep(1) 

while True:
    message = input("Your command: ")
    if message == "humidity":
        cmd = message + '\a'
        arduinoData.write(cmd.encode())
        while (arduinoData.inWaiting()==0):
            pass
        dataPacket = arduinoData.readline()  
        dataPacket=str(dataPacket,'utf-8')   
        dataPacket=dataPacket.strip('\r\n') 
        print(dataPacket)
        break
    
