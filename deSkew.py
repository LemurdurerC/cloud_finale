# import the necessary packages
import math
import os
import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

IMAGES = 'dataset2/Receipts/'



def deskewPrism(_img):
    image = io.imread(_img)
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)

def display_avant_apres(_original):
    plt.subplot(1, 2, 1)
    plt.imshow(io.imread(_original))
    plt.show()

    plt.subplot(1, 2, 2)
    plt.imshow(deskewPrism(_original))
    plt.show()
    cv2.waitKey(0)

def deskew1(image):

    # image = cv2.imread(filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # otherangle = compute_skew(filename)
    # print("otherangle: ", otherangle)
    # print("angle: ", angle)

    # angle = otherangle

    if angle < -45:
        angle = -(90 + angle)
        # print("angle < -45: ", angle)
    elif abs(angle) > 0:
        # print("angle > -45: ", angle)
        angle = - angle + 90

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # M2 = cv2.getRotationMatrix2D(center, otherangle, 1.0)
    # rotated2 = cv2.warpAffine(image2, M2, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
    #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # cv2.putText(rotated2, "Angle: {:.2f} degrees".format(otherangle),
    #             (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # show the output image
    # print("[INFO] angle: {:.3f}".format(angle))
    # cv2.imshow("Input", image)
    # cv2.imshow("Rotated", rotated)
    # cv2.imshow("Rotated2", rotated2)
    # cv2.waitKey(0)

    return rotated

def correctSize(image):

    height = image.shape[1]
    width = image.shape[0]

    print("before height, width ", height, width)

    coef = 0
    if width < 1000 or height < 1000:
        if width < height:
            coef = 1000 / width
        else:
            coef = 1000 / height
        if coef > 2:
            # print("coef: ---", coef)
            coef = 2
        # print("changing size: -------- ", coef)

        image = cv2.resize(image, (int(height * coef), int(width * coef)), interpolation=cv2.INTER_AREA)

    return image




def compute_skew(file_name):
    # load in grayscale:
    src = cv2.imread(file_name, 0)
    height, width = src.shape[0:2]

    # invert the colors of our image:
    cv2.bitwise_not(src, src)

    # Hough transform:
    minLineLength = width / 2.0
    maxLineGap = 20
    lines = cv2.HoughLinesP(src, 1, np.pi / 180, 100, minLineLength, maxLineGap)

    # calculate the angle between each line and the horizontal line:
    angle = 0.0
    nb_lines = len(lines)
    print("nombre de lignes: ", nb_lines)

    for line in lines:
        angle += math.atan2(line[0][3] * 1.0 - line[0][1] * 1.0, line[0][2] * 1.0 - line[0][0] * 1.0);

    angle /= nb_lines * 1.0
    # print("angle: ", angle)

    # print("angle 2 : ", angle * 180.0 / np.pi)

    return angle * 180 / np.pi
    # return angle


if __name__ == '__main__':

    for image in os.listdir(IMAGES):
        display_avant_apres(IMAGES + image)
        deskew1(IMAGES + image)

    # # deskew("torcido.jpg")
    # display_avant_apres("torcido.jpg")