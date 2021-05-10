import datetime
import time
import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
from roipoly import RoiPoly, MultiRoi
from matplotlib import pyplot as plt
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import pickle
import paho.mqtt.client as mqtt
import uuid
import signal

def selectRegion(img, img_flattened, img_dims, imgsize):
    fig = plt.figure() # Show the image
    plt.imshow(img)
    plt.title("left click: line segment         right click or double click: close region")

    rois = MultiRoi()
    
    all_masks = []
    for name, roi in rois.rois.items():
        all_masks.append(roi.get_mask(img_flattened))

    if not all_masks:
        print("Nothing selected")
        return None

    roi_total_mask = np.clip(sum(all_masks), 0, 1)
    print("Looks good? [(y)es | (n)o]")
    
    roi_full_mask = roi_total_mask.reshape(*img_dims)
    masked_img = roi_full_mask.reshape(*img_dims, 1) * img
    plt.imshow(masked_img)
    plt.title('Masked image')
    plt.show(block=False)
    plt.pause(1)

    answer = input()

    while answer not in ['y', 'n']:
        print("Please enter [y|n]:")
        answer = input()

    if answer == 'n':
        plt.close()
        return None

    plt.close()
    return roi_full_mask

# vs = cv2.VideoCapture(1)

vs = cv2.VideoCapture("tram.mov")

my_filter = KalmanFilter(dim_x=4, dim_z=2)
my_filter.x = np.array([0., 0.02, 100., -0.02]) #tram1pos, tram1vel, tram2pos, tram2vel
my_filter.F = np.array([[1.,1.,0.,0.], #state transition table for tram 1 and tram 2
                        [0.,1.,0.,0.],
                        [0.,0.,1.,1.],
                        [0.,0.,0.,1.]])
my_filter.H = np.array([[1.,0.,0.,0.], [0.,0.,1.,0.]])    # Measurement function - only positional values
my_filter.P *= 1000.                 # covariance matrix
my_filter.R = 5                      # state uncertainty
my_filter.Q = Q_discrete_white_noise(dim=4, dt=0.1, var=0.13)

tram_positions = [0, 100] 
sensor = np.array([[tp] for tp in tram_positions])

video_tram_section = (55,80) #where does the video capture movement in relation to entire tramline (0,100)
mask_section = [0, 0]

firstFrame = None
mask = None

########  MQTT  ########
topic = 'IDD/nani/trams'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)
client.loop_start()
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)
signal.signal(signal.SIGINT, handler)
########################

i = 0
while True:
    i = (i + 1)%4 #for spinner

    frame = vs.read()
    frame = frame[1]
    text = "No tram"
    
    if frame is None:
        break

    frame = imutils.resize(frame, width=1080)[:960,:]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    #Initializing background frame and region mask for subtraction  
    if firstFrame is None:
        firstFrame = gray
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_flattened = np.sum(img, axis = -1) # for roipoly img xy dimensions
        img_dims = img_flattened.shape
        imgsize = img_dims[0] * img_dims[1]
        mask = selectRegion(img, img_flattened, img_dims, imgsize)
        # pickle.dump(mask, open("live_re.gion", "wb"))
        
        mask = pickle.load(open("re.gion", "rb"))
        # mask = pickle.load(open("live_re.gion", "rb"))

        if mask is not None:
            mask = mask.astype('uint8')
            firstFrame = (firstFrame * mask).astype('uint8')
            cols = np.any(mask, axis=0)
            cmin, cmax = np.where(cols)[0][[0, -1]]
            mask_section = [cmin, cmax]
        else:
            mask_section = [0, frame.shape[0]]
        continue
    
    if mask is not None:
        gray = (gray * mask).astype('uint8')
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    kernel = np.ones((7, 7),np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    kernel = np.ones((10, 10),np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=3)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    observed_trams = []
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 300 or cv2.contourArea(c) > 3000:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        observed_trams.append([((x + w/2) - mask_section[0])*100/(mask_section[1] - mask_section[0]), cv2.contourArea(c)])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Tram Detected!"
    
    # print()
    # print(observed_trams)
    num_observed_trams = len(observed_trams)
    
    #Process tram readings using a kalman filter for each tram
    if num_observed_trams == 0:
        my_filter.predict()
    if observed_trams:
        if num_observed_trams == 1:
            my_filter.predict_steadystate()
        else:
            my_filter.predict()

        if num_observed_trams < 3:
            predicted_positions = my_filter.get_update()
            sensor = np.array([[predicted_positions[0][0]], [predicted_positions[0][2]]]) # initialize sensor with predicted positions
            # print(sensor)

            # if there are actual observed positions
            # see which observation is closest to which prediction and assign that observation as the actual sensor value
            diffs = np.zeros((num_observed_trams,2))
            
            for ind, tram in enumerate(observed_trams):
                diffs[ind,0] = abs(tram[0] - sensor[0])
                diffs[ind,1] = abs(tram[0] - sensor[1])
            
            # print(diffs)

            sensor_ind_sort = np.argsort(diffs, axis=-1)
            
            sensor_inds = [-1, -1]

            # print(sensor_ind_sort)

            for ot in range(num_observed_trams):
                sensor_inds[sensor_ind_sort[ot, 0]] = ot

            # print(sensor_inds)
            for sind, si in enumerate(sensor_inds):
                if si != -1:
                    sensor[sind,0] = observed_trams[si][0]

            # print(sensor)
            if num_observed_trams == 1:
                my_filter.update_steadystate(sensor)
            else:
                my_filter.batch_filter([sensor])
        
    kalman_state = my_filter.x
    # print(kalman_state)
    
    tram_positions = [kalman_state[0], kalman_state[2]]
    tram_pos_scaled = [int((tp/100)*(video_tram_section[1] - video_tram_section[0]) + video_tram_section[0]) for tp in tram_positions]
    
    ########  MQTT  ########
    client.publish(topic+"/1", f"{tram_pos_scaled[0]}")
    client.publish(topic+"/2", f"{tram_pos_scaled[1]}")
    client.publish(topic+"/busy", f"{3}")
    ########################
    
    printstr = " "
    for ti in range(100):
        if ti in tram_pos_scaled:
            # printstr += "<🚟" if kalman_state[tram_pos_scaled.index(ti)*2 + 1] < 0 else "🚟>"
            printstr += "🚟"

        else:
            printstr += "-"
    print(["\\","|","/","-"][i] + printstr, end="\r", flush = True)
    

    cv2.putText(frame, "{}".format(text), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(frame, "Tram 1: Position: {:.2f}, Velocity: {:.2f}".format(*kalman_state[0:2]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Tram 2: Position: {:.2f}, Velocity: {:.2f}".format(*kalman_state[2:4]), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "MQTT:", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(frame, "Tram1: {}".format(tram_pos_scaled[0]), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Tram2: {}".format(tram_pos_scaled[1]), (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("TramWatcher", frame)
    cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

vs.release()
cv2.destroyAllWindows()