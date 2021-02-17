import time
import pyautogui
import cv2 as cv
import numpy as np


def find_item(item):
    img_rgb = cv.imread(goto_inventory())
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    w, h = item.shape[::-1]

    res = cv.matchTemplate(img_gray, item, cv.TM_CCOEFF_NORMED)
    threshold = 0.80
    loc = np.where(res >= threshold)

    coords = []
    for pt in zip(*loc[::-1]):
        coords.append((pt[0] + w // 2, pt[1] + h // 2))

    return coords


def goto_inventory():
    # Press main menu button
    # Press character button
    # Take screenshot and return image
    return "./images/inventory.png"


def click_all(points):
    for pt in points:
        pyautogui.moveTo(pt[0], pt[1])
        print("click")
        time.sleep(.5)


if __name__ == '__main__':
    salewa = cv.imread('./images/salewa.png', 0)
    click_all(find_item(salewa))
    # print(f"{point[0]}, {point[1]}")
