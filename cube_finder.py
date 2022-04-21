import cv2 as cv
import numpy as np



basic = cv.imread('cube1.jpg')
imageBlur = cv.GaussianBlur(basic, (7, 7), 1)
imageGray = cv.cvtColor(imageBlur, cv.COLOR_BGR2GRAY)
imageCanny = cv.Canny(imageGray, 130, 115)

kernel = np.ones((5, 5))
imageDilate = cv.dilate(imageCanny, kernel, iterations=2)
imageErode = cv.erode(imageDilate, kernel, iterations=1)

cv.imshow('cube', imageDilate)
cv.waitKey(0)

contours, hierarchy = cv.findContours(imageErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
imgContours = basic.copy()

widthOfBasic = 0
for cnt in contours:

    area = cv.contourArea(cnt)
    if area > 8000:
        cv.drawContours(imgContours, contours, -1, (0, 255, 0), 7)
        arcLeng = cv.arcLength(cnt, True)
        approximation = cv.approxPolyDP(cnt, 0.01 * arcLeng, True)
        x, y, h, w = cv.boundingRect(approximation)
        cv.rectangle(imgContours, (x, y), (x + w, y + h), (255, 0, 0), 5)
        # print(x, y, w, h)
        widthOfBasic = w


cap = cv.VideoCapture('video.mp4')
width = int(cap.get(3))
height = int(cap.get(4))


known_distance = 15.0
known_width = 5.7



def focalLengthFun(distance, width, width_in_image):
    temp = (width_in_image * distance) / width
    return temp


def distanceFun(focalLnegth, width, width_in_frame):
    temp = (width * focalLnegth) / width_in_frame
    return temp


def empty(a):
    pass



cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)
cv.createTrackbar("IterationDilate", "Parameters", 3, 10, empty)
cv.createTrackbar("IterationErode", "Parameters", 2, 10, empty)
cv.createTrackbar("Threshold1", "Parameters", 170, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 160, 255, empty)
cv.createTrackbar("Area", "Parameters", 3000, 50000, empty)

while True:
    ret, frame = cap.read()
    distance = 0
    if ret == True or False:


        IterationDilate = cv.getTrackbarPos("IterationDilate", "Parameters")
        IterationErode = cv.getTrackbarPos("IterationErode", "Parameters")
        Thresh1 = cv.getTrackbarPos("Threshold1", "Parameters")
        Thresh2 = cv.getTrackbarPos("Threshold2", "Parameters")
        Area = cv.getTrackbarPos("Area", "Parameters")

        imageBlur = cv.GaussianBlur(frame, (5, 5), 1)
        imageGray = cv.cvtColor(imageBlur, cv.COLOR_BGR2GRAY)
        imageCanny = cv.Canny(imageGray, Thresh1, Thresh2)

        kernel = np.ones((5, 5))
        imageDilate = cv.dilate(imageCanny, kernel, iterations=IterationDilate)
        imageErode = cv.erode(imageDilate, kernel, iterations=IterationErode)

        contours, hierarchy = cv.findContours(imageErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        imgContours = frame.copy()


        for cnt in contours:
            area = cv.contourArea(cnt)
            if 74 < distance < 76:
                cv.setTrackbarPos("Area", "Parameters", 3000)
            elif 64 < distance < 66:
                cv.setTrackbarPos("Area", "Parameters", 5000)
            elif 54 < distance < 56:
                cv.setTrackbarPos("Area", "Parameters", 7000)
            elif 39 < distance < 41:
                cv.setTrackbarPos("Area", "Parameters", 10000)
            elif 29 < distance < 31:
                cv.setTrackbarPos("Area", "Parameters", 15000)
            elif 23 < distance < 25:
                cv.setTrackbarPos("Area", "Parameters", 20000)
            if area > Area:

                cv.drawContours(imgContours, contours, -1, (0, 255, 0), 7)
                arcLeng = cv.arcLength(cnt, True)
                approximation = cv.approxPolyDP(cnt, 0.01 * arcLeng, True)
                x, y, h, w = cv.boundingRect(approximation)
                cv.rectangle(imgContours, (x, y), (x + w, y + h), (255, 0, 0), 5)
                # print(x, y, w, h)


                focalLength = focalLengthFun(known_distance, known_width, widthOfBasic)
                distance = distanceFun(focalLength, known_width, w)
                print(distance)



        cv.namedWindow("Image")
        cv.resizeWindow("Image", width, height)
        cv.namedWindow("contours")
        cv.resizeWindow("contours", width, height)
        cv.imshow("Image", frame)
        cv.imshow("contours", imgContours)
        cv.waitKey(50)

    else:
        break

cap.release()
cv.destroyAllWindows()
