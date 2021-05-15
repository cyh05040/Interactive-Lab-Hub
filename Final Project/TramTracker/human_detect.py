# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/
# David edited some stuff

import numpy as np
import cv2
import sys
import paho.mqtt.client as mqtt
import uuid
import signal
# Load a model imported from Tensorflow
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

img = None
webCam = False

# topic = "IDD/nani/tramstations"
# def on_connect(client, userdata, flags, rc):
#     print(f"connected with result code {rc}")
#     client.subscribe(topic)
# client = mqtt.Client(str(uuid.uuid1()))
# client.tls_set()
# client.username_pw_set('idd', 'device@theFarm')
# client.on_connect = on_connect
# client.connect(
#     'farlab.infosci.cornell.edu',
#     port=8883)
# client.loop_start()
# def handler(signum, frame):
#     print('exit gracefully')
#     client.loop_stop()
#     exit (0)
# signal.signal(signal.SIGINT, handler)

if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
    #   cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")


while(True):
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape

    # Use the given image as input, which needs to be blob(s).
    tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

    # Runs a forward pass to compute the net output
    networkOutput = tensorflowNet.forward()
    person = 0
    # Loop on the outputs
    for detection in networkOutput[0,0]:
        score = float(detection[2])
        classes = int(detection[0])
        # print(detection)
        if score > 0.7 and classes == 0:
            # print(detection)
            person += 1
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows

            #draw a red rectangle around detected objects
            cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), thickness=2)
    cv2.putText(img, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255), 2)
    # client.publish(topic+"/1", str(person))
    if webCam:
        if sys.argv[-1] == "noWindow":
           print("Finished a frame")
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()