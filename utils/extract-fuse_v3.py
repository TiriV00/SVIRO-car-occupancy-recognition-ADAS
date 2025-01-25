import os
from ultralytics import YOLO
import cv2
import torch
import numpy as np
from random import randint

def bbox_extractor(image_path, model):

    # read the image
    frame = cv2.imread(image_path)
    H, W, _ = frame.shape

    # inference on the model specified 
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        
        print("image counter= ", image_counter)
        if(image_counter == 0):
            front_classes.append(class_id)
        
        elif(image_counter == 1):
            rear_classes.append(class_id)

        if score > threshold:
            # draw rectangles and classes
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 2)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # save the image
    if(image_counter == 0):
        output_path = os.path.join(RESULTS_DIR, 'frontv2_out.jpg')
        cv2.imwrite(output_path, frame)
        return front_classes
    
    if(image_counter == 1):
        output_path = os.path.join(RESULTS_DIR, 'rearv2_out.jpg')
        cv2.imwrite(output_path, frame)
        return rear_classes

# image path definitions
image_front = "/hpc/home/valerio.tiri/LABORS/adas_sviro/tests/test_images/tiguan_train_imageID_1192_GT_0_1_0.png"
image_rear = "/hpc/home/valerio.tiri/LABORS/adas_sviro/tests/test_images/tiguan_train_imageID_556_GT_2_4_5.png"

# results path definition
RESULTS_DIR = '/hpc/home/valerio.tiri/LABORS/adas_sviro/tests/test_results/'

# model path definition
model_path = '/hpc/home/valerio.tiri/LABORS/adas_sviro/runs/detect/train4/weights/last.pt'
model = YOLO(model_path)

# confidence level of the prediction
threshold = 0.75

front_classes = []
rear_classes = []
image_counter= 0
front_bbox = bbox_extractor(image_front, model)
print('\nfront classes = ', front_classes)

image_counter= 1
rear_bbox = bbox_extractor(image_rear, model)
print('\nrear classes = ', rear_classes)

print("Elaboration completed, images saved in: ", RESULTS_DIR)

# found classes definition
infant = False
child = False
adult = False
object = False
airbag = False

# make flags true if the class is present in front/rear image
for element in front_classes:
    if int(element) == 1:
        infant = True
        airbag = True
    elif int(element) == 2:
        child = True
    elif int(element) == 3:
        adult = True
    elif int(element) == 4:
        object = True
    
for element in rear_classes:
    if int(element) == 1:
        infant = True
    elif int(element) == 2:
        child = True
    elif int(element) == 3:
        adult = True
    elif int(element) == 4:
        object = True

# random temperature generation (-20/50)
temperature = randint(0,70)
temperature = temperature - 20
print("\noutside temperature = ", temperature)

# actions to do
if infant and not adult and temperature < 18:
    print('\nWARNING: infant left alone! \n sound alarm activated, heating activated')

if infant and not adult and temperature > 17 and temperature < 26:
    print('\nWARNING: infant left alone! \n sound alarm activated')

if infant and not adult and temperature > 25 and temperature < 33:
    print('\nWARNING: infant left alone! \n sound alarm activated, windows automatically rolled down')

if infant and not adult and temperature > 32 :
    print('\nWARNING: infant left alone! \n sound alarm activated, A/C activated')

if child and not adult and temperature < 18:
    print('\nWARNING: child left alone! \n sound alarm activated, heating activated')

if child and not adult and temperature > 17 and temperature < 26:
    print('\nWARNING: child left alone! \n sound alarm activated')

if child and not adult and temperature > 25 and temperature < 33:
    print('\nWARNING: child left alone! \n sound alarm activated, windows automatically rolled down')

if child and not adult and temperature > 32 :
    print('\nWARNING: child left alone! \n sound alarm activated, A/C activated')

if object and not adult:
    print('\nmaybe you forgot an object in the car')

if airbag :
    print('\npassenger airbag disabled, infant is present')

print("\n//END//")