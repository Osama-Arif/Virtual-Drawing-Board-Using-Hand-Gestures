import cv2
import numpy as np
import os
import HandTrackingModule as htm
eraserThickness = 50

folderPath = "header"
myList = os.listdir(folderPath)
# print(myList)
overLayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overLayList.append(image)
# print(len(overLayList))
header = overLayList[0]
drawColor=(0, 0, 255)



cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 750)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0

board = np.zeros((720, 1280, 3), np.uint8)

while True:
    # import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # tipIds = [4, 8, 12, 16, 20]

    if len(lmList) != 0:
        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # two fingers up = selection mode
        if fingers[1] and fingers[2]:
            print("Selection Mode")
            if y1 < 125:
                if 250<x1<450:
                    header = overLayList[2]
                    drawColor = (0,0,0)

                elif 650 < x1 < 750:
                    header = overLayList[1]
                    drawColor = (255, 0, 255)
                elif 800 < x1 < 950:
                    header = overLayList[0]
                    drawColor = (0, 0, 255)
                elif 1050 < x1 < 1280:
                    header = overLayList[3]
                    drawColor = (0, 255, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), drawColor, 9)

        # index finger is up = Drawing mode
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("drawing Mode")
            if xp ==0 and yp ==0:
                xp, yp = x1, y1

            if drawColor == (0, 255, 255):
                cv2.line(img, (xp,yp), (x1,y1), drawColor, eraserThickness)
                cv2.line(board, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(board, (xp, yp), (x1, y1), drawColor, eraserThickness)

            xp, yp = x1, y1

    #setting header
    img[0:125,0:1280] = header
    img = cv2.addWeighted(img,0.5,board,0.5,0)
    cv2.imshow("Virtual Board", img)
    # cv2.imshow("Virtual Board", board)
    cv2.waitKey(1)