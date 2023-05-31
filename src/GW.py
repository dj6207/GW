import pyautogui as pya
import cv2 as cv
import numpy as np
import time
import random as rand
from windowCapture import WinCapture
from GWParser import GWParser

IMAGES_PATH = "..\Images\\"
PNG = ".png"

def matchAll(items, toleranceFactor=3 ,elapsedTime=10, threshold=0.8, debug=False, color=(0, 0, 255)):
    """
    Parameters
    image: haystack
    template: the needle that will be found in the haystack
    threshold: confidence level

    Return
    location: center coordinate of the image that will be found
              format [((X, X tolerance), (Y, Y tolerance))]
    """

    items = items[1:]
    print(items)
    itemsFound = 0


    startTime = time.time()
    for item in items:
        while True:
            capture = WinCapture()
            frame = capture.get_frame()
            image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            template = cv.imread(f"{IMAGES_PATH}{item}{PNG}", cv.IMREAD_GRAYSCALE)
            width, height = template.shape[::-1]
            match_probability = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
            match_locations = np.where(match_probability >= threshold)
            itemsFound = match_locations[0].size
            # Add the match rectangle to the screen
            locations = []
            for x, y in zip(*match_locations[::-1]):
                # Center of each image with either x and y tolerances
                locations.append(((x + width/2, width/toleranceFactor), (y + height/2, height/toleranceFactor)))
                if debug:
                    print((x + int(width/2), y + int(height/2)))
                    cv.rectangle(image, (x, y), (x + int(width/2), y + int(height/2)), color, 1)
                    cv.imwrite('debug.png', image)
            endTime = time.time()
            if (endTime - startTime > elapsedTime) or itemsFound:
                break
        if itemsFound:
            break
    return locations, itemsFound

def clickItem(x, y, xOffset, yOffset):
    tween = pya.easeInOutQuad
    currentPosition = pya.position()
    distance = distanceFormula(current=currentPosition, next=(x,y))
    if distance > 200:
        dur = rand.uniform(1, 2)
        tween = pya.easeOutElastic
    else:
        dur = rand.uniform(0.2, 0.5)
        tween = pya.easeOutBounce
    newX = x + rand.uniform(-xOffset, xOffset)
    newY = y + rand.uniform(-yOffset, yOffset)
    pya.click(x=newX, y=newY, duration=dur, tween=tween)

def distanceFormula(current, next):
    return np.sqrt(np.square(next[0] - current[0]) + np.square(next[1] - current[1]))

def moveToItem(x, y, xOffset, yOffset):
    # pya.easeInOutQuad
    # pya.easeInBounce
    # pya.easeInElastic
    # pya.easeInOutSine
    dur = rand.uniform(0.25, 2.5)
    newX = x + rand.uniform(-xOffset, xOffset)
    newY = y + rand.uniform(-yOffset, yOffset)
    print((x,y))
    pya.moveTo(x=newX, y=newY, duration=dur, tween=pya.easeInOutQuad)

def imagePreProcessing(imagePath, templatePath):
    imageRGB = cv.imread(imagePath)
    imageGRAY = cv.cvtColor(imageRGB, cv.COLOR_BGR2GRAY)
    template = cv.imread(templatePath, cv.IMREAD_GRAYSCALE)
    return imageGRAY, template

def Threo(script):
    queue = GWParser.loadQueue(script)
    while queue.qsize():
        items = queue.get()
        location, itemsFound = matchAll(items=items, elapsedTime=10,toleranceFactor=2.2 ,debug=False)
        if int(items[0]):
            try:
                x = location[0][0][0]
                y = location[0][1][0]
                xOffset = location[0][0][1]
                yOffset = location[0][1][1]
                print(f"{items} was found")
                clickItem(x, y, xOffset, yOffset)
                # moveToItem(x, y, xOffset, yOffset)
            except IndexError as e :
                print(f"{items} was not found")
                break
        else:
            if not itemsFound:
                print(f"{items} was not found")
                break
            print(f"{items} was found")

if __name__ == "__main__": 
    # Threo("..\Scripts\slime.txt")
    Threo("..\Scripts\\test.txt")