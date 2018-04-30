import RPi.GPIO as GPIO
import time
import urllib
import cv2

import numpy as np
np.set_printoptions(threshold=np.nan)

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 50)


GPIO.output(TRIG, False)

path='color_img.png'

noofcolors=3
countofcolors=[0]*(noofcolors)

def move_servo(color):
	p.start(7.5)
	if color==0:
		p.ChangeDutyCycle(7.5)
		time.sleep(1)
	
	if color==1:
		p.ChangeDutyCycle(2.5)
		time.sleep(1)
	
	if color==2:
		p.ChangeDutyCycle(12.5)
		time.sleep(1)

	senddata(color)

def takephoto():
  url='http://192.168.43.1:8080/photo.jpg'
  imgResp=urllib.urlopen(url)
  imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
  img=cv2.imdecode(imgNp,-1)
  #cv2.imshow('test',img)
  cv2.imwrite(path, img)
#  cv2.imwrite('color_img.png', img)

def senddata(colorindx):
  countofcolors[colorindx]+=1
  data=urllib.urlopen("https://api.thingspeak.com/update?api_key=0VDF8Y4EXQT87C1N&field"+str(colorindx+1)+"="+str(countofcolors[colorindx]));
  

def scanphoto(path):
	# load the image
	image = cv2.imread(path)



	# define the list of boundaries
	boundaries = [
		([17, 15, 100], [50, 56, 200]),
		([128,0,0],[255,105,97]),
		([0, 128, 0], [178, 236, 93])]

	#colors

	colors=["Red","Blue","Green"]

	#Pixel track
	numpixels=[]

	count=0
	# loop over the boundaries
	for (lower, upper) in boundaries:
		print(count)
		count=count+1
		
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
	 
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
		print(output.shape)
		print(np.count_nonzero(output))
		numpixels.append(np.count_nonzero(output))
		#print(output)
		#np.savetxt('test.out'+str(count), output, delimiter=',')
		# show the images
		#cv2.imshow("images", np.hstack([image, output]))
		#cv2.waitKey(0)
	print(numpixels)
	print(len(numpixels))
	valindx=numpixels.index(max(numpixels))
	print(colors[valindx],"is the dominating color")
	move_servo(valindx)


while 1==1:
	GPIO.output(TRIG, False)
	print( "Waiting For Sensor To Settle")
	time.sleep(2)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print ("Distance:",distance,"cm")

	if distance<=15:
		print( "object detected !!.Write your function here")
		takephoto()
		scanphoto(path)



GPIO.cleanup()
