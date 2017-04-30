import numpy as np
import cv2

#draws the contours for better understanding

def average(img):
	w=img.shape[0]
	h=img.shape[1]

	s=sum(sum(img)) 
	s=s/(w*h)
	return s

def showScaledImage(windowname,image):
	cv2.namedWindow(windowname,cv2.WINDOW_NORMAL)
	cv2.imshow(windowname,image)
	cv2.resizeWindow(windowname, 1200,800)

image = cv2.imread("pics\\4.jpg")

orig = image.copy()


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (5, 5), 0)
laplacian = cv2.Laplacian(gray,cv2.CV_64F)
av=average(gray)
ret,th1 = cv2.threshold(gray,av/2,255,cv2.THRESH_TOZERO)
showScaledImage("1",laplacian)
#gray=cv2.equalizeHist(gray)
laplacian=np.uint8(laplacian)
edged = cv2.Canny(gray, 10, 200)


_,cnts, _ = cv2.findContours(edged.copy(), 1, 1)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
i=0
showScaledImage("edges",edged)
for c in cnts:
	print(c.shape)
	temp=image.copy()
	cv2.drawContours(temp,cnts[i],-1,(0,255,0),20)
	showScaledImage("image"+str(i),temp)
	i=i+1
cv2.waitKey(0)

