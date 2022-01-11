import cv2
import numpy as np

# get the video frames
# '0' cause webcam is used
cap = cv2.VideoCapture(0)


# nothing function to pass it through trackbar
def nothing(x):
    # It is function to do whatever you want
    pass


# Using trackbar to detect a specific color 'Red'
# open a tracking window
cv2.namedWindow("Tracking")

# set the HSV for required color "Red"
cv2.createTrackbar("LH", "Tracking", 110, 180, nothing)
cv2.createTrackbar("LS", "Tracking", 177, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 81, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 180, 180, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
    # read the frame
    _, frame = cap.read()

    # show the frame and the trackbar
    cv2.imshow('Tracking', frame)

    # converting the frame from BGR into HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # apply the changing in trackbar into the mask window
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    # put the boundaries of red color
    l_r = np.array([l_h, l_s, l_v])
    u_r = np.array([u_h, u_s, u_v])

    # pass the frame and the boundaries of red color to be masked
    mask = cv2.inRange(hsv, l_r, u_r)

    # contours around red objects
    # 1st arg is the object
    # 2nd arg contour retrieval mode, 'EXTERNAL' we interested about the exterior of the contours
    # 3rd arg contour approximation method
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # additional: we can find the number of red objects
    # print(f'number of red objects {len(contours)}')

    # Drawing a rectangle around each contour
    # Loop through each contour
    for cnt in contours:
        # find minimum fitting rectangle
        rect = cv2.minAreaRect(cnt)

        # find the box points
        box = cv2.boxPoints(rect)

        # convert the list of points into binary array
        box = np.int0(box)

        # draw the contours in the main frame
        cv2.drawContours(frame, [box], 0, (255, 0, 0), 4)

    # Using bitwise and to remove all non red objects
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
