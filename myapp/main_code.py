# # import the necessary packages
# import numpy as np
# import time
# import cv2
# import os
# import requests
# # Load the COCO class labels
# from myapp.models import boatTbl
#
# labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
# LABELS = open(labelsPath).read().strip().split("\n")
#
# # Initialize a list of colors to represent each possible class label
# np.random.seed(42)
# COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
#
# # Derive the paths to the YOLO weights and model configuration
# weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
# configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])
#
# # Load YOLO
# num=int(input("enter the boat id"))
# print("[INFO] loading YOLO from disk...")
# net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# ln = net.getLayerNames()
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#
# # Initialize the video stream
# vs = cv2.VideoCapture(0)
# (W, H) = (None, None)
#
# while True:
#     # Read the next frame from the stream
#     (grabbed, frame) = vs.read()
#     if not grabbed:
#         break
#
#     # If the frame dimensions are empty, grab them
#     if W is None or H is None:
#         (H, W) = frame.shape[:2]
#
#     # Construct a blob from the input frame and perform a forward pass of the YOLO object detector
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     layerOutputs = net.forward(ln)
#
#     # Initialize lists of detected bounding boxes, confidences, and class IDs
#     boxes = []
#     confidences = []
#     classIDs = []
#
#     # Loop over each of the layer outputs
#     for output in layerOutputs:
#         for detection in output:
#             scores = detection[5:]
#             classID = np.argmax(scores)
#             confidence = scores[classID]
#
#             # Filter out weak predictions
#             if confidence > 0.5:
#                 box = detection[0:4] * np.array([W, H, W, H])
#                 (centerX, centerY, width, height) = box.astype("int")
#                 x = int(centerX - (width / 2))
#                 y = int(centerY - (height / 2))
#                 boxes.append([x, y, int(width), int(height)])
#                 confidences.append(float(confidence))
#                 classIDs.append(classID)
#
#     # Apply non-maxima suppression
#     idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.5)
#
#     # Initialize human count for the current frame
#     current_human_count = 0
#
#     # Ensure at least one detection exists
#     if len(idxs) > 0:
#         for i in idxs.flatten():
#             if LABELS[classIDs[i]] == "person":
#                 current_human_count += 1  # Increment count for each detected person
#                 # Draw bounding box and label on the frame
#                 (x, y) = (boxes[i][0], boxes[i][1])
#                 (w, h) = (boxes[i][2], boxes[i][3])
#                 color = [int(c) for c in COLORS[classIDs[i]]]
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
#                 cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#
#
#     # Display the count of detected persons in the current frame
#     cv2.putText(frame, f"Detected Humans: {current_human_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
#     print("Detected Humans",current_human_count)
#     ob=boatTbl.objects.get(id=num)
#     if ob.no_of_passengers<current_human_count:
#     # requests.get("http://127.0.0.1:8000/count/1/"+str(current_human_count))
#
#
#     # Show the output frame
#     cv2.imshow('video', frame)
#
#     if cv2.waitKey(33) == 27:
#         break
#
# # Release the video capture object
# print("[INFO] cleaning up...")
# vs.release()

# Import necessary packages
import numpy as np
import time
import cv2
import os
import requests
# from playsound import playsound  # Import playsound for audio alarm


# Load the COCO class labels


labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# Initialize colors for class labels
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# Load YOLO model
weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

# Load YOLO
num = int(input("Enter the boat ID: "))
print("[INFO] Loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Initialize the video stream
vs = cv2.VideoCapture(0)
(W, H) = (None, None)

while True:
    # Read the next frame from the stream
    (grabbed, frame) = vs.read()
    if not grabbed:
        break

    # Get frame dimensions
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # Process the frame for YOLO
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    # Initialize lists for bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    classIDs = []

    # Loop through layer outputs
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # Filter out weak detections
            if confidence > 0.5:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # Apply non-maxima suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.5)

    # Initialize human count
    current_human_count = 0

    # Process detected objects
    if len(idxs) > 0:
        for i in idxs.flatten():
            if LABELS[classIDs[i]] == "person":
                current_human_count += 1
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display count of detected humans
    cv2.putText(frame, f"Detected Humans: {current_human_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    print("Detected Humans:", current_human_count)
    requests.get("http://127.0.0.1:8000/count/"+str(current_human_count)+"/"+str(num))
    # Get boat details
    # ob = boatTbl.objects.get(id=num)

    # Check if the detected human count exceeds the allowed passengers
    # if ob.no_of_passengers < current_human_count:
    #     print("[ALERT] Overloaded! Playing alarm...")
    #     playsound("WhatsApp Audio 2025-02-11 at 06.16.28_806f7410.mp3")  # Play the alarm sound
    #     requests.get("http://127.0.0.1:8000/count/1/"+str(current_human_count))

    # Show the output frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(33) == 27:
        break

# Cleanup
print("[INFO] Cleaning up...")
vs.release()
cv2.destroyAllWindows()
