import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread('pics\\1.jpg')
plt.hist(img.ravel(),256,[0,256]); plt.show()

