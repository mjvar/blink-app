# Blink Facial Detection for Drowsiness
# Thank you to Adrian Rosebrock, from whom this code was largely adapted.
# https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/

# Does two main things: eye tracking (blinking, etc.) for drowsiness 
# and face tracking for presence/breaks. Sends both of these data points to Flask server.

# USAGE
# python3 blink_detect.py --shape-predictor shape_predictor_68_face_landmarks.dat --webcam 1
# Note: Webcam compatibility may vary between devices. Please try changing --webcam 1 to --webcam 0/2/3/4/-1/2 etc.


# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from threading import Thread, Timer
from imutils import face_utils
import numpy as np
import requests
import argparse
import imutils
import time
import dlib
import csv
import cv2

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

def append_eye_data(drows):
	# append recorded data to user_eye_data array
	user_eye_data.append(drows)

def write_eye_data():
	# record drowsiness data at regular intervals

	global user_eye_data
	if len(user_eye_data) > 0:
		# get average of data collected over WAIT_TIME
		avg_drow = 0
		for row in user_eye_data:
			avg_drow += row
		avg_drow /= len(user_eye_data)
		print(avg_drow)

		r = requests.post("http://localhost:5000/eye_data", data={'timestamp':get_current_time(),'score':avg_drow})
		print(r.text)

	user_eye_data = []
	# Restart timer to execute again after WAIT_TIME
	timer = Timer(WAIT_TIME, write_eye_data).start()

def write_face_data():
	r = requests.post("http://localhost:5000/face_data", data={'timestamp':get_current_time()})
	print(r.text)

def get_current_time():
	t = time.localtime()
	current_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
	return current_time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to qualify as drowsy
EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 48

# consecutive frames a face must be gone to count as a break
FACE_CONSEC_FRAMES = 300

# frame counters 
EYE_COUNTER = 0
FACE_COUNTER = 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

# Time period (in seconds) over which average drowsiness is calculated
WAIT_TIME = 1
# temp array used to calculate average drowsiness over a given time
user_eye_data = []
# total eye data stored so far + in previous uses (updated on program start from total_eye_data.csv)
total_eye_data = []
# total face data stored so far + in previous uses (updated on program start from total_face_data.csv)
total_face_data = []

# Start timer for eye data
timer = Timer(WAIT_TIME, write_eye_data).start()

written = False

# loop over frames from the video stream
while True:
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	if len(rects) == 0:
		FACE_COUNTER += 1

		if FACE_COUNTER >= FACE_CONSEC_FRAMES and not written:
			print("Break detected")
			write_face_data()
			written = True
	else:
		FACE_COUNTER = 0
		written = False

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# append EAR data to temporary array user_eye_data
		append_eye_data(ear)

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (200, 80, 80), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (200, 80, 80), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			EYE_COUNTER += 1

			# if drowsiness detected
			# do something
			if EYE_COUNTER >= EYE_AR_CONSEC_FRAMES:
				# draw an alarm on the frame
				cv2.putText(frame, "Drowsiness detected.", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 220, 100), 2)

		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			EYE_COUNTER = 0
			ALARM_ON = False

		# draw the computed eye aspect ratio on the frame to help
		# with debugging and setting the correct eye aspect ratio
		# thresholds and frame counters
		cv2.putText(frame, "E.A.R.: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 220, 100), 2)
 
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
		timer.stop()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()