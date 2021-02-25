import time
import pyautogui
import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con


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


def windowCapture():
    w = 1600
    h = 900

    window = win32gui.FindWindow(None, 'EscapeFromTarkov')
    # window = None

    # Get the window image data
    window_dc = win32gui.GetWindowDC(window)
    dc_object = win32ui.CreateDCFromHandle(window_dc)
    cDC = dc_object.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dc_object, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (w, h), dc_object, (0, 0), win32con.SRCCOPY)

    # Save the screenshot (For debugging)
    # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    dc_object.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(window, window_dc)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img


def main():
    loop_time = 0
    while True:
        # screenshot = ImageGrab.grab()
        screenshot = windowCapture()

        cv.imshow('frame', screenshot)

        if cv.waitKey(1) == ord('q'):
            break

        print(f'FPS: { 1 / (time.time() - loop_time)}')

        loop_time = time.time()

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
