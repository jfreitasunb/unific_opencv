# import the necessary packages
import numpy as np
import argparse
import cv2
import itertools
import sys
import os as _os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
bitwise_not = cv2.bitwise_not(image)
gray = cv2.cvtColor(bitwise_not, cv2.COLOR_BGR2GRAY)
# detect circles in the image

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1,10,param1=50,param2=30,minRadius=15,maxRadius=20)

screen_res = 1280, 720
scale_width = screen_res[0] / image.shape[1]
scale_height = screen_res[1] / image.shape[0]
scale = min(scale_width, scale_height)

#resized window width and height
window_width = int(image.shape[1] * scale)
window_height = int(image.shape[0] * scale)

#cv2.WINDOW_NORMAL makes the output window resizealbe
cv2.namedWindow('output', cv2.WINDOW_NORMAL)

#resize the window according to the screen resolution
cv2.resizeWindow('output', window_width, window_height)

# # ensure at least some circles were found
if circles is not None:
# 	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	circles = circles[circles[:,1].argsort()] 
 
# 	# loop over the (x, y) coordinates and radius of the circles
	inicio = circles[:3]
	final = circles[-3:]
	cabecalho = np.concatenate((inicio, final), axis=0)
	print(np.max(circles[:,1]))
	# print(np.arctan((final[1][1] - inicio[1][1])/(final[1][0] - inicio[1][0])))
	# for i in circles:
		# print(i)
	for (x, y, r) in cabecalho:
# 		# draw the circle in the output image, then draw a rectangle
# 		# corresponding to the center of the circle
		
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
# 	# show the output image
	# cv2.imshow("output", np.hstack([output]))
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()