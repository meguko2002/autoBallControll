import cv2
import numpy as np

def color_pick(hue, image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue += 180
    hue %= 180
    range = 20
    hue_max = hue + range
    hue_min = hue - 20
    hsv_min = np.array([hue_min, 60, 60])
    hsv_max = np.array([hue_max, 255, 255])
    if hue_min < hue_max:
        mask: None = cv2.inRange(hsv, hsv_min, hsv_max)
    else:
        mask = cv2.inRange(hsv, 0, hsv_max)
        mask += cv2.inRange(hsv, hsv_min, 180)
    return mask

def detect_center_of_gravity(cnt):
    try:
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M["m00"])
        cy = int(M['m01'] / M["m00"])
        return cx, cy
    except ZeroDivisionError:
        # たまにゼロ割になってしまうケースが有るので対処
        print("ZeroDivisionError!!")


def nothing():
    pass


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image', 500,300)

# Create trackbars for color change
cv2.createTrackbar('Hue', 'image', 0, 180, nothing)

cap = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)
while (True):
    k = cv2.waitKey(1 & 0xFF)
    if k == 27:
        break
    hue = cv2.getTrackbarPos('Hue', 'image')
    # Capture frame-by-frame
    ret, frame = cap.read()
    mask = color_pick(hue, frame)
    # cv2.imshow('mask', mask)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('opening', opening)
    image, contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contours.sort(key=cv2.contourArea, reverse=True)
    print(len(contours))
    cv2.putText(frame, 'count =' + str(len(contours)), (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1,
                cv2.LINE_AA)
    if len(contours) > 0:
        # for i in range(len(contours)):
        for i in range(1):
            cv2.drawContours(frame, [contours[i]], 0, (0, 255, 0), 3)
            cx, cy = detect_center_of_gravity(contours[i])
            cv2.putText(frame, " (" + str(cx) + "," + str(cy) + ")", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 0), 1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 0), -1)
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
