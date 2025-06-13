import pytesseract
from time import sleep
import pyautogui
import numpy as np
import cv2

# Using OCR requires you to install it and set teh correct path to the exe.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_region(image):
    r = cv2.selectROI("select the area", image)
    cv2.destroyAllWindows()
    return(r)

def find_color_region(image, target_color):
    mask = np.abs(image - target_color).astype('u1')
    mask = np.mean(mask,axis=2).astype('u1')
    _,mask = cv2.threshold(mask,5,255,cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)) 
    # Perform dilation
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1).astype('u1')
    
    # Find contours of the masked regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw rectangles around the found regions
    maxContour = None
    maxArea    = 50
    for contour in contours:
        if cv2.contourArea(contour) > maxArea:  # Filter out small regions
            maxArea = cv2.contourArea(contour)
            x, y, w, h = maxContour = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Show the original image with rectangles
    # cv2.imshow("Image with Color Regions", image[:,:,[2,1,0]])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return(maxContour)

def main():
    #Get a screenshot
    screenshot = np.array(pyautogui.screenshot())

    X,Y,W,H = find_region(screenshot)

    names = []
    name = ''
    i=0
    sleep(4)
    while(i < 100):
        screenshot = np.array(pyautogui.screenshot())
        crop = screenshot[Y:Y+H,X:X+W,:]
        text_region = find_color_region(crop,(0,0,0))
        if(not text_region is None):
            x,y,w,h = text_region
            tIm = crop[y:y+h,x:x+w,:]
            xTxt  = pytesseract.image_to_string(tIm)
            newname = xTxt.strip("\n").split('\n')[-1]
            if newname not in names:
                print(newname)
                names.append(newname)
        sleep(2)

if __name__ =="__main__":
    main()