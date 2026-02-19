import cv2
import mss
import numpy


def sc_record():
	mon = {"top": 400, "left": 0, "width":1920, "height":50}

	title = "[MSS] FPS bench"
	fps = 0
	sct = mss.mss()

	while True:
		img = numpy.asarray(sct.grab(mon))
		fps +=1
		find_point(img)

		cv2.imshow(title, img)
		if cv2.waitKey(25) & 0xFF == ord("q"):
			cv2.destroyAllWindows()
			break

	return fps


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
    
	cv2.imshow("Mask", color_mask)
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area < 100:
			continue
		x, y, w, h = cv2.boundingRect(cnt)

		if w > h * 1.5 and w > 520:
			print("detected")



def check_size(mask):
	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	for cnt in contours:
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = numpy.intp(box)
        
		edge1 = numpy.intp((box[1][0] - box[0][0], box[1][1] - box[0][1]))
		edge2 = numpy.intp((box[2][0] - box[1][0], box[2][1] - box[1][1]))
        
		len1 = cv2.norm(edge1)
		len2 = cv2.norm(edge2)
        
		if 520 < max(len1, len2):
			return True
		return False


sc_record()