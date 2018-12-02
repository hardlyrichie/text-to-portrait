import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from helpers import fetch_image

print('Enter Name:')
name = raw_input()

fetch_image(name)

for i in range(10):
    # READING IMAGE
    img = cv.imread('images/' + name + '/' + name + '_' + str(i) + '.jpg',0)
    height, width = img.shape[:2]

    # CANNY EDGE DETECTION
    # edges	=	cv.Canny(	image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]	)
    edges = cv.Canny(img, 100, 200)

    # GET XY COORDINATES
    indices = np.where(edges != [0])
    coordinates = zip(indices[0], indices[1])

    # print(coordinates)

    print(width, height)

    # Create a black image of original image height and width
    draw_img = np.zeros((height, width, 3), np.uint8)

    # WHy is the coordinates reflected over y = x axis
    # DRAW POINTS
    for x, y in coordinates:
        cv.line(draw_img, (y, x), (y+1, x+1), (255,255,255), 2)

    plt.imshow(draw_img, cmap = 'gray', interpolation = 'bicubic')
    plt.show()