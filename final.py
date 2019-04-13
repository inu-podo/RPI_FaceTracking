from multiprocessing import Process
import time
import cv2
import RPi.GPIO as GIPO
import numpy as np

# Resolution Size
_X = 480
_Y = 360
_X_Quarter = _X / 4
_Y_Quarter = _Y / 4

# clock unit for PWM
_Horizontal_Default = 7.5
_Vertical_Default = 5
_One_Tick = .1

# Setting GPIO in pi
GPIO.setmode(GPIO.BCM)

webcam = cv2.VideoCapture(-1)		# Get ready to start getting images from the webcam
webcam.set(3, _X)
webcam.set(4, _Y)
time.sleep(1)

frontalCascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')		# frontal face pattern detection
profileface = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')		# side face pattern detection

face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]		# Center of the face: a point calculated from the above variable
lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-
			# 	a left profile face, or a frontal face; rather than searching for all three every time,-
			# 	it uses this variable to remember which is last saw: and looks for that again. If it-
			# 	doesn't find it, it's set back to zero and on the next loop it will search for all three.-
			# 	This basically triples the detect time so long as the face hasn't moved much.
			
def HorizontalServo():
	pin0 = 18
	GPIO.setup(pin0, GPIO.OUT)
	p0 = GPIO.PWM(pin0, 50)
	p0.start(2.5)
	
def VerticalServo():
	pin1 = 17
	GPIO.setup(pin1, GPIO.OUT)
	p1 = GPIO.WPM(pin1, 50)
	p1.start(2.5)

Process(target=HorizontalServo, args=()).start()	# Start the subprocesses
Process(target=VerticalServo, args=()).start()
time.sleep(1)

#====================================================================================================

def CamRight(num):
	for i in range(num):
		p0.ChangeDutyCycle(_One_Tick)
def CamLeft(num):
	for i in range(num):
		p0.ChangeDutyCycle(- _One_Tick)
def CamDown(num):
	for i in range(num):
		p1.ChangeDutyCycle(_One_Tick)
def CamUp(num):
	for i in range(num):
		p1.ChangeDutyCycle(- _One_Tick)
		
#===================================================================================================


while True:

	faceFound = False	# This variable is set to true if, on THIS loop a face has already been found
				# We search for a face three diffrent ways, and if we have found one already-
				# there is no reason to keep looking.
	
	if not faceFound:
		if lastface == 0 or lastface == 1:
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			fface = frontalface.detectMultiScale(aframe,1.3, 3,
				(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
			if fface != ():			# if we found a frontal face...
				lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
				for f in fface:		# f in fface is an array with a rectangle representing a face
					faceFound = True
					face = f

					# its not necessary to loop more than one time
	if not faceFound:				# if we didnt find a face yet...
		if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
			aframe = webcam.read()[1]	# 	THIS method was the one who found it last loop	# since the frontalface search above
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			pfacer = profileface.detectMultiScale(aframe,1.3, 3,
				(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
			if pfacer != ():		# if we found a profile face...
				lastface = 2
				for f in pfacer:
					faceFound = True
					face = f

	if not faceFound:				# a final attempt
		if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
			aframe = webcam.read()[1]	#	detect right profile faces, if the cam is looking at-
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			#cv2.flip(aframe,1,aframe)	#	flip the image
			pfacel = profileface.detectMultiScale(aframe,1.3, 3,
				(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
			if pfacel != ():
				lastface = 3
				for f in pfacel:
					faceFound = True
					face = f

	if not faceFound:		# if no face was found...-
		lastface = 0		# 	the next loop needs to know
		face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop

	# will check later if its fine with just one try
	"""
	if not faceFound:
		if lastface == 0 or lastface == 1:
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			fface = frontalface.detectMultiScale(aframe,1.3, 3,
				(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
			if fface != ():			# if we found a frontal face...
				lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
				for f in fface:		# f in fface is an array with a rectangle representing a face
					faceFound = True
					face = f
	"""		
	x, y, w, h = face		# 240 180 40 40 center position in the camera
	Cface = [(x + w/2), (y + h/2)]	# we are given an x,y corner point and a width and height, we need the center
	print (str(Cface[0]) + "," + str(Cface[1]))		# center of the rectangle in faceFound

	
	# have to check 'onetick' is working well
	if Cface[0] != 0:
		if Cface[0] < _X_Quarter:
			CamLeft(_One_Tick)
		if Cface[0] > _X - _X_Quarter:
			CamRight(- _One_Tick)
		if Cface[1] < _Y_Quarter:
			CamUp(_One_Tick)
		if Cface[1] > _Y - _Y_Quarter:
			CamDown(- _One_Tick)
	
	
	
p1.stop()
p2.stop()
    
GPIO.cleanup()
webcam.realease()
cv2.destroyAllWindows()
