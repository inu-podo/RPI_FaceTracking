from multiprocessing import Process
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# Hoony, 

"""
def HorizontalServo():
    pin0 = 18
    GPIO.setup(pin0, GPIO.OUT)
    p0 = GPIO.PWM(pin0, 50)
    p0.start(_Horizontal_Default)
    print("Starting HorizontalServo...")
    
def VerticalServo():
    pin1 = 17
    GPIO.setup(pin1, GPIO.OUT)
    p1 = GPIO.PWM(pin1, 50)
    p1.start(_Vertical_Default)
    print("Starting VerticalServo...")
    
          
#9 goingleft 6 center 3 right
#7 down 8.5 center 10 up
    
def CamRight(p0, horizontalPosition):
    print("right")
    horizontalPosition += 0.3
    time.sleep(0.3)
    p0.ChangeDutyCycle(horizontalPosition)
    time.sleep(0.3)
    p0.CHangeDutyCycle(0)
    
def CamLeft(p0, horizontalPosition):
    print("left")
    horizontalPosition -= 0.3
    time.sleep(0.3)
    p0.ChangeDutyCycle(horizontalPosition)
    time.sleep(0.3)
    p0.CHangeDutyCycle(0)
    
def CamUp(p1, verticalPosition):
    print("up")
    verticalPosition += 0.3
    time.sleep(0.3)
    p1.ChangeDutyCycle(verticalPosition)
    time.sleep(0.3)
    p1.ChangeDutyCycle(0)
    
def CamDown(p1, verticalPosition):
    print("down")
    verticalPosition -= 0.3
    time.sleep(0.3)
    p1.ChangeDutyCycle(verticalPosition)
    time.sleep(0.3)
    p1.ChangeDutyCycle(0)

        
        
def CamMove(Cface):
    if Cface[0] != 0:
        #print (str(Cface[0]) + "," + str(Cface[1]))     # center of the rectangle in faceFound
        if Cface[0] < _X_Quarter:
            CamRight()
        if Cface[0] > _X - _X_Quarter:
            CamLeft()
        if Cface[1] < _Y_Quarter:
            CamUp()
        if Cface[1] > _Y - _Y_Quarter:
            CamDown()
"""
#########################################################################
            
# Resolution Size 320*240 480*320
_X = 480
_Y = 320
_X_Quarter = _X / 4
_Y_Quarter = _Y / 4

# clock unit for PWM
_Horizontal_Default = 6
_Vertical_Default = 8.5
_One_Tick = 0.1

horizontalPosition = _Horizontal_Default
verticalPosition = _Vertical_Default

face = [0, 0, 0, 0]
Cface = [0, 0]
lastface = 0

GPIO.setmode(GPIO.BCM)

pin0 = 18
GPIO.setup(pin0, GPIO.OUT)
p0 = GPIO.PWM(pin0, 50)
p0.start(_Horizontal_Default)
#p0.start(6)
print("Starting HorizontalServo...")
time.sleep(0.5)

pin1 = 17
GPIO.setup(pin1, GPIO.OUT)
p1 = GPIO.PWM(pin1, 50)
p1.start(_Vertical_Default)
#p1.start(0)
print("Starting VerticalServo...")
time.sleep(0.5)

p0.ChangeDutyCycle(0)
p1.ChangeDutyCycle(0)
time.sleep(1)

cam = cv2.VideoCapture(0)
cam.set(3, _X)
cam.set(4, _Y)
time.sleep(1)

frontalface = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
profileface = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')

#Process(target=HorizontalServo, args=()).start()
#Process(target=VerticalServo, args=()).start()

while True:
    
    faceFound = False
    
    if not faceFound:
        
        frame = cam.read()[1]

        faces = frontalface.detectMultiScale(
            frame,
            scaleFactor = 1.1,
            minNeighbors = 3,
            flags = (cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),
            maxSize = (80, 80))
    
        faceFound = True
    
    """
    if not faceFound:               # if we didnt find a face yet...
        #if lastface == 0 or lastface == 2:  # only attempt it if we didn't find a face last loop or if-
        frame = cam.read()[1]   #   THIS method was the one who found it last loop  # since the frontalface search above

        faces = profileface.detectMultiScale(
            frame,1.3,4,
            flags = (cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))

        faceFound = True
    """
    
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        Cface = [(x + w/2), (y + h/2)]
        
        if Cface[0] != 0:
            #time.sleep(1)
            print(x, y, w, h, "and ,", Cface)
        #print (str(Cface[0]) + "," + str(Cface[1]))     # center of the rectangle in faceFound
            """
            if Cface[0] < _X_Quarter:
                p0.start(0)
                horizontalPosition -= 1
                p0.ChangeDutyCycle(horizontalPosition)
                p0.stop()
                print("right")
            if Cface[0] > _X - _X_Quarter:
                horizontalPosition += _One_Tick
                CamLeft(p0, horizontalPosition)
            if Cface[1] < _Y_Quarter:
                verticalPosition += _One_Tick
                CamUp(p1, verticalPosition)
            if Cface[1] > _Y - _Y_Quarter:
                verticalPosition -= _One_Tick
                CamDown(p1, verticalPosition)
            """
            
            if Cface[0] < _X_Quarter:
                print("right")
                horizontalPosition -= 0.3
                #time.sleep(0.2)
                p0.ChangeDutyCycle(horizontalPosition)
                time.sleep(0.2)
                p0.ChangeDutyCycle(0)

            if Cface[0] > _X - _X_Quarter:
                print("left")
                horizontalPosition += 0.3
                #time.sleep(0.2)
                p0.ChangeDutyCycle(horizontalPosition)
                time.sleep(0.2)
                p0.ChangeDutyCycle(0)
                
            if Cface[1] < _Y_Quarter:
                print("up")
                verticalPosition += 0.3
                #time.sleep(0.2)
                p1.ChangeDutyCycle(verticalPosition)
                time.sleep(0.2)
                p1.ChangeDutyCycle(0)
                
            if Cface[1] > _Y - _Y_Quarter:
                print("down")
                verticalPosition -= 0.3
                #time.sleep(0.2)
                p1.ChangeDutyCycle(verticalPosition)
                time.sleep(0.2)
                p1.ChangeDutyCycle(0)
                
    cv2.imshow('frame', frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    

p0.stop()
p1.stop()
    
GPIO.cleanup()
webcam.realease()
cv2.destroyAllWindows()





