import cv2
from matplotlib import pyplot as plt
import numpy as np

#https://stackoverflow.com/questions/14243472/estimate-brightness-of-an-image-opencv

def estimateBrightness(img):
    #white image -> max brightness
    #black image -> min brightness

    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([img], [0], None, [256], [0, 254])
    plt.plot(hist)
    #plt.show()
    brightness = np.average(img[0])
    print(brightness)
    #hacer histograma


    return