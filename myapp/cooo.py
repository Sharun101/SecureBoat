# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np

import time
import cv2
import os



from gtts import gTTS
import os


import pyttsx3

from myapp.newcnn import predict


def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    # You can experiment with different voices and rates
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Convert the text to speech and play it
    engine.say(text)
    engine.runAndWait()


labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")



font = cv2.FONT_HERSHEY_SIMPLEX



# fontScale
fontScale = 1

# Blue color in BGR
print_color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2







# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
# r"G:\yolo\yolo-object-detection\videos\airport.mp4"
# vs = cv2.VideoCapture("queda.mp4")
vs = cv2.VideoCapture(0)
writer = None
(W, H) = (None, None)



# loop over frames from the video file

listop=[]
listra=[]
counti=0
while True:

	counti=counti+1
	# read the next frame from the filenewcnn.py

	(grabbed, frame) = vs.read()


	print("==> ",counti)
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []
	pl=[]
	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > 0.5:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
		0.5)

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			color = [int(c) for c in COLORS[classIDs[i]]]

			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			if LABELS[classIDs[i]]=="person" :
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				pl.append("1")

				cropped_image = frame[ y:y + h,x:x + w]
				cv2.imwrite("sample.png",cropped_image)
				res=predict("sample.png")
				cv2.putText(frame, res, (x, y - 5),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, print_color, 2)
				if res == "unsafe":
					import winsound

					frequency = 2500  # Set Frequency To 2500 Hertz
					duration = 1000  # Set Duration To 1000 ms == 1 second
					# winsound.Beep(frequency, duration)
				# cv2.putText(frame, res, (x, y-10), font,
				# 				fontScale, color, thickness, cv2.LINE_AA)






		# iud(qry, 3)
	if len(pl)>5:
		text_to_speech("over load detected")
		text_to_speech("over load detected")
		text_to_speech("over load detected")
	cv2.imshow('video', frame)

	if cv2.waitKey(33) == 27:
		break


# release the file pointers
print("[INFO] cleaning up...")

vs.release()