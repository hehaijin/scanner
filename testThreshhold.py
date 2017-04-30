import cv2
import numpy as np
from matplotlib import pyplot as plt


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

image = cv2.imread("pics\\5.jpg")

orig = image.copy()


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

av=average(gray)
ret,th1 = cv2.threshold(gray,av/2,255,cv2.THRESH_TOZERO)



showScaledImage("threshhold", th1)


 
cv2.waitKey(0)

