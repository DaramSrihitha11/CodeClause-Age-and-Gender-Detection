# -*- coding: utf-8 -*-
"""Age and Gender ditection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eT8q4W064WZXrASq9_39EYgWiXnpX6mJ

# Age and Gender Detection
BY : SRIHITHA DARAM
# Summary :
Age and gender detection typically involves training a deep learning model on a large dataset of annotated images and then using the trained model to predict age and gender from new images. Here is a general summary of the process:

1. Import Libraries: In Google Colab, the required libraries such as TensorFlow, Keras, and OpenCV are imported. These libraries provide the necessary tools for building and training deep learning models, as well as performing image processing tasks.

2. Dataset Preparation: A labeled dataset of images is required for training the age and gender detection model. The dataset needs to be preprocessed, which may involve resizing the images, normalizing pixel values, and splitting the dataset into training and validation sets.

3. Model Architecture: The deep learning model architecture needs to be defined. This typically involves selecting a suitable pre-trained model, such as VGGNet or ResNet, and adding custom layers on top for age and gender prediction. The model is compiled with appropriate loss functions and optimization algorithms.

4. Training: The model is trained using the prepared dataset. This involves feeding the training images into the model, computing the loss, and adjusting the model's weights through backpropagation and gradient descent. The training process continues for multiple epochs until the model achieves satisfactory accuracy on the training data.

5. Evaluation: The trained model is evaluated using the validation set. The model's performance metrics, such as accuracy and loss, are calculated to assess its generalization capabilities.

6. Testing: Once the model is trained and evaluated, it can be used to predict age and gender on new images. The model is applied to test images or a live video stream, and the predicted age and gender labels are obtained.

7. Post-processing and Visualization: The predicted age and gender labels can be post-processed and visualized on the images. This typically involves adding text overlays or bounding boxes around faces, along with the predicted labels.

8. Deployment: The trained model can be deployed to various applications or platforms. In the case of Google Colab, the model can be saved and used for further inference or integrated into other projects.

It's important to note that the specific implementation details may vary depending on the chosen deep learning framework, dataset, and model architecture. The above summary provides a general overview of the steps involved in age and gender detection.
"""

!gdown https://drive.google.com/uc?id=1_aDScOvBeBLCn_iv0oxSO8X1ySQpSbIS

!unzip modelNweight.zip

#import libraries

import cv2 as cv
from google.colab.patches import cv2_imshow 
import math 
import time

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

faceProto = "modelNweight/opencv_face_detector.pbtxt"
faceModel = "modelNweight/opencv_face_detector_uint8.pb"

ageProto = "modelNweight/age_deploy.prototxt"
ageModel = "modelNweight/age_net.caffemodel"

genderProto = "modelNweight/gender_deploy.prototxt"
genderModel = "modelNweight/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load network
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

padding = 20

def age_gender_detector(frame):
    # Read frame
    t = time.time()
    frameFace, bboxes = getFaceBox(faceNet, frame)
    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        label = "{},{}".format(gender, age)
        cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
    return frameFace

input = cv.imread("habib.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("kim.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("chil.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("puja.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("purnima.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("trump.jpg")
output = age_gender_detector(input)
cv2_imshow(output)

input = cv.imread("rayhan.jpg")
output = age_gender_detector(input)
cv2_imshow(output)