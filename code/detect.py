
from time import sleep, time
from math import floor
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO

servo_pin_x = 12
servo_pin_y = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin_x, GPIO.OUT)
GPIO.setup(servo_pin_y, GPIO.OUT)
pwmx = GPIO.PWM(servo_pin_x,50)
pwmy = GPIO.PWM(servo_pin_y,50)
duty_cycle_x = 4
duty_cycle_y = 11

IMG_WIDTH  = 1280
IMG_HEIGHT = 720

def select_target_face(faces):
	"""
	This function select the target face. The input is a non empty list of box coordinate
	(x,y,w,h). Only the biggest box (closer face) is selected and returned.
	"""

	temp_w = -1
	sel_x = 0
	sel_y = 0
	sel_w = 0
	sel_h = 0
	for (x, y, w, h) in faces:
		if w > temp_w:
			sel_x = x
			sel_y = y
			sel_w = w
			sel_h = h
	return (sel_x, sel_y, sel_w, sel_h)

def center_of_box(x, y, w, h):
	return (floor(x+h/2), floor(y+h/2))

def is_face(faces):
	"""
	This function returns True if `faces` is not empty (if at least one face
	is detected) else return False.
	"""
	return True if len(faces) != 0 else False

def diff(cx,cy):
	"""
	This function return the difference between the center of the image and
	the center of the box representing the face detected. 
	/!\ WARNING: Remind that the origin is in the left top. 
	"""
	img_cx, img_cy = floor(IMG_WIDTH/2), floor(IMG_HEIGHT/2)
	diffx = img_cx - cx
	diffy = img_cy - cy
	return (diffx, diffy)

def update_servo_x(step):
	global duty_cycle_x
	duty_cycle_x += step
	if duty_cycle_x >= 11:
		duty_cycle_x = 11
	elif duty_cycle_x <= 2:
		duty_cycle_x = 2
	return

def update_servo_y(step):
	global duty_cycle_y
	duty_cycle_y += step
	if duty_cycle_y >= 12:
		duty_cycle_y = 12
	elif duty_cycle_y <= 9:
		duty_cycle_y = 9
	return


def main():
	fr = 30
	camera = PiCamera()
	camera.resolution = (IMG_WIDTH, IMG_HEIGHT)
	camera.color_effects =(128, 128)
	camera.framerate = fr
	rawCapture = PiRGBArray(camera, size=(IMG_WIDTH,IMG_HEIGHT))
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	global duty_cycle_x
	global duty_cycle_y
	pwmx.start(duty_cycle_x)
	pwmy.start(duty_cycle_y)
	gripx = False
	gripy = False
	eps = 5
	ustep = 0.2

	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array

		faces = face_cascade.detectMultiScale(image, 1.5, 2)

		if(is_face(faces)):
			(x, y, w, h) = select_target_face(faces)
			cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
			(cx, cy) = center_of_box(x,y,w,h)
			cv2.circle(image, (cx,cy), radius=0, color=(0,0,255), thickness=5)
			cv2.arrowedLine(image, (floor(IMG_WIDTH/2), floor(IMG_HEIGHT/2)),(cx, cy), color=(0,255,0), thickness = 5)

			cv2.line(image, (int(cx+w/4+eps), int(cy-w/4-eps)), (int(cx+w/4+eps), int(cy+w/4+eps)), color=(0,255,0), thickness = 3)
			cv2.line(image, (int(cx+w/2), int(cy-w/2)), (int(cx+w/2), int(cy+w/2)), color=(0,255,0), thickness = 3)
			cv2.line(image, (int(cx-w/4-eps), int(cy-w/2)), (int(cx-w/4-eps), int(cy+w/2)), color=(0,255,0), thickness = 3)
			cv2.line(image, (int(cx-w/2), int(cy-w/4-eps)), (int(cx-w/2), int(cy+w/4+eps)), color=(0,255,0), thickness = 3)

			(diffx, diffy) = diff(cx, cy)

			if abs(diffx) <= w/4+eps:
				gripx = True

			if abs(diffx) > w/2:
				gripx = False

			if not gripx:
				if diffx <= 0 and -diffx >= w/4:
					update_servo_x(-ustep)
				elif diffx > 0 and diffx >= w/4:
					update_servo_x(ustep)

				pwmx.ChangeDutyCycle(float(duty_cycle_x))

			if abs(diffy) <= w/4+eps:
				gripy = True
			if abs(diffy) > w/2:
				gripy = False
			if not gripy:
				if diffy <= 0 and -diffy >= w/4:
					update_servo_y(-ustep)
				elif diffy > 0 and diffy >= w/4:
					update_servo_y(ustep)
				pwmy.ChangeDutyCycle(float(duty_cycle_y))

		cv2.imshow("Frames", image)
		key = cv2.waitKey(1) & 0xFF

		rawCapture.truncate(0)

		if key == ord("q"):
			break

if __name__ == '__main__':
	main()
