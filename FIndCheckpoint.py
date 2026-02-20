import cv2
import mss
import numpy


def sc_record():
    mon = {"top": 400, "left": 0, "width":1920, "height":50}

    sct = mss.mss()

    while True:
        img = numpy.asarray(sct.grab(mon))
        print(find_point(img))

        cv2.imshow("title", img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


def find_point(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red1 = numpy.array([0, 30, 20])
    upper_red1 = numpy.array([15, 255, 255])
    lower_red2 = numpy.array([160, 30, 20])
    upper_red2 = numpy.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
    color_mask = cv2.bitwise_or(mask1, mask2)

    kernel = numpy.ones((5,5), numpy.uint8)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        if w > h * 1.5 and w > 520:
            return True