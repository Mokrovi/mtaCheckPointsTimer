import cv2
import mss
import numpy


def sc_record():
	mon = {"top": 0, "left": 0, "width":1920, "height":50}

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

	mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
	mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))

	mask = cv2.bitwise_or(mask1, mask2)

	if cv2.countNonZero(mask) > 0 and check_size(mask):
		print(check_size(mask))
		print('Red is present!')
	else:
		print('Red is not present!')


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