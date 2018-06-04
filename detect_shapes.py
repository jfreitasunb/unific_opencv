# import the necessary packages
import argparse
import imutils
import cv2
import numpy as np

class ShapeDetector:
    def __init__(self):
        pass
 
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.4 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
 
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
 
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
 
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
 
        # return the name of the shape
        return shape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to the input image")
args = vars(ap.parse_args())

kernel = np.ones((5,5),np.uint8)


# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
erosion = cv2.erode(image,kernel,iterations = 1)
dilate = cv2.dilate(erosion,kernel,iterations = 1)
cv2.bitwise_not( dilate, dilate )

image = dilate

resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
bitwise_not = cv2.bitwise_not(image)
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

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

# loop over the contours

for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
    cY = int((M["m01"] / (M["m00"] + + 1e-7)) * ratio)
    shape = sd.detect(c)
 
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 2)
 
    # show the output image
    cv2.imshow("output", image)
    cv2.waitKey(0)