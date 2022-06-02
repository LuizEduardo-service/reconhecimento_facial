import cv2
import time
import numpy as np


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
while True:
    success, img = cap.read()

    # taxa de quadros
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # insere dentro da imagem os dados do fps
    cv2.putText(
        img,
        f'FPS: {int(fps)}',
        (40, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 0, 255),
        3,
    )

    cv2.imshow('img', img)
    cv2.waitKey(1)
