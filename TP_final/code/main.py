#codigo basado en https://github.com/shantnu/Webcam-Face-Detect

import cv2
import sys
import logging as log
import datetime as dt
from time import sleep


from laser import addLasers
from metrics import estimateBrightness


#tecla q for quit

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
cv2.namedWindow("Video")
anterior = 0


while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    lens = cv2.imread(".\lens.PNG", cv2.IMREAD_UNCHANGED);

    # Capture frame-by-frame
    ret, frame = video_capture.read();
    frame_h, frame_w = frame.shape[:2];


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7,minSize=(50, 50));


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2);
        roi_gray = gray[y:y + h, x:x + w]   #region of interest
        roi_color = frame[y:y + h, x:x + w]

        # si encuentra caras, encuentra ojos y también le dibuja rectangulos
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4,minSize=(50, 50));
        for (eye_x, eye_y, eye_width, eye_height) in eyes:
            cv2.rectangle(roi_color, (eye_x, eye_y), (eye_x + eye_width, eye_y + eye_height), (0, 0, 255), 2);

            if len(eyes) == 2:
                frame = addLasers(frame, x, y, frame_w, frame_h, eye_x, eye_y, eye_width, eye_height, lens);
                backgr_br = estimateBrightness(gray);
                face_br = estimateBrightness(roi_gray);
                l_half_br = estimateBrightness(gray[y:y + h, x:x + w//2]);
                r_half_br = estimateBrightness(gray[y:y + h, x + w//2:x + w]);
                print("BackGroung Brightness = "+ str(backgr_br) )
                print("Face Brightness = "+ str(face_br) )
                print("Left side Brightness = "+ str(l_half_br) )
                print("Right side Brightness = "+ str(r_half_br) )
            # estimo el brightness de la region de la cara cuando identifica un ojo
            #if len(eyes) == 2:   #si identifica una cantidad par de ojos
                #
            #




    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()