import numpy as np
import cv2


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



def findScreenContour(cnts):
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4:
			screenCnt = approx
			break
	return screenCnt




#get the transform matrix for a 4 points 
def transformMatrix(cnt):
	inp=np.zeros((4,2))
	for i in range(cnt.shape[0]):
		inp[i]=np.reshape(cnt[i],(2,))
	inp=np.float32(inp)
	
	#ordered points in rect
	#get the center of the 4 points and compare each point with it.
	cenx=0
	ceny=0;
	for i in range(4):
		cenx=cenx+inp[i,0]
		ceny=ceny+inp[i,1]
	cenx=cenx/4
	ceny=ceny/4
	
	rect=np.zeros((4,2))
	for i in range(4):
		if inp[i,0] <cenx and inp[i,1]< ceny:
			rect[0]=inp[i]
		if inp[i,0]>= cenx and inp[i,1] >= ceny:
			rect[2]=inp[i]
		if inp[i,0]>= cenx and inp[i,1] < ceny:
			rect[3]=inp[i]
		if inp[i,0]< cenx and inp[i,1] >= ceny:
			rect[1]=inp[i]
	rect=np.float32(rect)	
	
	output=np.float32([[0,0],[0,800],[1200,800],[1200,0]])

	M = cv2.getPerspectiveTransform(rect,output)
	return M


def runall():
	for i in range(1,18):
		print("pics\\"+str(int(i))+".jpg")
		image = cv2.imread("pics\\"+str(int(i))+".jpg")
		dst,_=process(image)
		cv2.imwrite("output\\"+str(i)+".jpg",dst)



def testDisplay(k):
	image=cv2.imread("pics\\"+str(int(k))+".jpg")

	dst,cnt=process(image)

	#showScaledImage("edged",edged)
	cv2.drawContours(image,cnt,-1,(0,255,0),30)
	showScaledImage("contours",image)
	showScaledImage("screen",dst)

	cv2.waitKey(0)


def process(image):
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	av=average(gray)
	ret,gray = cv2.threshold(gray,av/2,255,cv2.THRESH_TOZERO)

	gray = cv2.GaussianBlur(gray, (5, 5), 0)

	#eualize histogram does not help much.
	#gray=cv2.equalizeHist(gray)
	edged = cv2.Canny(gray, 75, 200)
	_,cnts, _ = cv2.findContours(edged.copy(), 1, 2)
	cnt=findScreenContour(cnts)
	tm=transformMatrix(cnt)
	#use original image, not the blurred one
	dst=cv2.warpPerspective(orig,tm,(1200,800))
	return dst,cnt


runall()










