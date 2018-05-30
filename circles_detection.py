# import the necessary packages
import numpy as np
import argparse
import cv2
import itertools
import sys
import os as _os
from PIL import Image
import time as _t

path = "/home/jfreitas/C1-imagens_180/"
files = [f for f in _os.walk(path)]
print('Number of folders:',len(files))

files.sort(key=lambda x:x[0])
#sort the files inside the folders and keep only the jpg
files = [(f[0],f[1],sorted([img for img in f[2] if img[-4:]=='.jpg'])) 
        for f in files]
nImg = sum([len(f[2]) for f in files])
print('Number of files: ',nImg)

# angulo_rotacao = np.array([])

for (dirpath, dirnames, filenames) in files :
	for filename in filenames :
            t0 = _t.time()
            pathfile = _os.path.join(dirpath,filename)
            relpathfile = _os.path.join(_os.path.relpath(dirpath,path),
                                            filename)
            image = cv2.imread(pathfile)
            output = image.copy()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
            #     # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                altura_bolhas = np.max(circles[:,1])
                
                if altura_bolhas > 2800:
                    circles = circles[circles[:,1].argsort()]
                else:
                    circles = circles[circles[:,0].argsort()]
                inicio = circles[:3]
                final = circles[-3:]
                dx = inicio[1][0] - final[0][0]
                dy = inicio[1][1] - final[0][1]
                if dx != 0:
                    angulo_rotacao = np.arctan(dy/dx)
                else:
                    angulo_rotacao = 0
                
                # if angulo_rotacao >= 1.1 and angulo_rotacao <= 1.5:
                #     image_rot = Image.open(pathfile)
                #     image_rot.rotate(180, expand=True).save(pathfile)
                t1 = _t.time()
                print(angulo_rotacao)
# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required = True, help = "Path to the image")
# args = vars(ap.parse_args())
# # load the image, clone it for output, and then convert it to grayscale
# image = cv2.imread(args["image"])
# output = image.copy()
# bitwise_not = cv2.bitwise_not(image)
# gray = cv2.cvtColor(bitwise_not, cv2.COLOR_BGR2GRAY)
# # detect circles in the image

# circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1,10,param1=50,param2=30,minRadius=15,maxRadius=20)

# screen_res = 1280, 720
# scale_width = screen_res[0] / image.shape[1]
# scale_height = screen_res[1] / image.shape[0]
# scale = min(scale_width, scale_height)

# #resized window width and height
# window_width = int(image.shape[1] * scale)
# window_height = int(image.shape[0] * scale)

# #cv2.WINDOW_NORMAL makes the output window resizealbe
# cv2.namedWindow('output', cv2.WINDOW_NORMAL)

# #resize the window according to the screen resolution
# cv2.resizeWindow('output', window_width, window_height)

# # # ensure at least some circles were found
# if circles is not None:
# #     # convert the (x, y) coordinates and radius of the circles to integers
#     circles = np.round(circles[0, :]).astype("int")
#     altura_bolhas = np.max(circles[:,1])
#     print(altura_bolhas)

#     if altura_bolhas > 2800:
#         circles = circles[circles[:,1].argsort()]
#     else:
#         circles = circles[circles[:,0].argsort()]

# #     # loop over the (x, y) coordinates and radius of the circles
#     inicio = circles[:3]
#     final = circles[-3:]
#     cabecalho = np.concatenate((inicio, final), axis=0)
#     # print(np.arctan((final[1][1] - inicio[1][1])/(final[1][0] - inicio[1][0])))
#     # for i in circles:
#         # print(i)
#     for (x, y, r) in cabecalho:
# #         # draw the circle in the output image, then draw a rectangle
# #         # corresponding to the center of the circle
        
#         cv2.circle(output, (x, y), r, (0, 255, 0), 4)
#         cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
# #     # show the output image
#     cv2.imshow("output", np.hstack([output]))
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()