import cv2
import numpy as np
import glob
import random
import os

# Load Yolo
net = cv2.dnn.readNetFromDarknet("yolov3_testing.cfg","yolov3_custom_last.weights")

# Name custom object
classes = ["Resistor","ceramic capacitor","diode","IC","electrolytic_capacitor"]

# Images path
images_path = glob.glob("/home/akesh/Desktop/FYP/YOLO/CompDataset/IMG_20220302_162049.jpg")




layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
cnt = 1
random.shuffle(images_path)
# loop through all the images
for img_path in images_path:
    # Loading image
    img = cv2.imread(img_path)
    #img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                #print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    Boxes = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 5)
            cv2.putText(img, label, (x, y + 30), font, 5, color, 5)
            box = [x,y,w,h]
            Boxes.append(box)
    with open('test.npy', 'wb') as f:
        np.save(f, np.array(Boxes))
    w,h,c = img.shape
    #print("h",h)
    #print("w",w)
    scale = 0.5
    img = cv2.resize(img, (int(h*scale),int(w*scale)), interpolation= cv2.INTER_LINEAR)
    cv2.imshow("Image", img)
    os.chdir("/home/akesh/Desktop/FYP/YOLO/det")
    cv2.imwrite("res.jpg",img)
    
    #key = cv2.waitKey(0)

cv2.destroyAllWindows()
