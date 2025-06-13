import numpy as np
import cv2 as cv
import sys
import ast


def is_contour_inside_circle(contour, center, radius):
    """
    Check if the entire contour is inside the circle.
    The contour points should be inside the circle defined by center and radius.
    """
    if(radius == 0):
        return(True)
    for point in contour:
        x, y = point[0]
        distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
        if distance > radius:
            return False
    return True

def filter_contours_in_circle(image_shape, contours, diameter):
    """
    Filter contours that are inside a circle of given diameter centered in the image.
    """
    # Get the center of the image
    center = (image_shape[1] // 2, image_shape[0] // 2)
    radius = diameter // 2  # radius is half the diameter
    
    # List to store contours that are inside the circle
    filtered_contours = []
    
    for contour in contours:
        if is_contour_inside_circle(contour, center, radius):
            filtered_contours.append(contour)
    
    return filtered_contours

def draw_circle_and_contours(image, contours, diameter):
    """
    Draw a circle on the image and the contours that are inside the circle.
    """
    # Get the center and radius
    center = (image.shape[1] // 2, image.shape[0] // 2)
    radius = diameter // 2
    
    # Make a copy of the image to draw on
    output_image = image.copy()
    
    # Draw the circle (centered in the image)
    if(radius > 0):
        cv.circle(output_image, center, radius, (0, 255, 0), 2)
    
    # Draw the contours
    cv.drawContours(output_image, contours, -1, (0, 0, 255), 2)
    
    return output_image

def get_BB_BackroundSubtraction(blank_image_paths,object_image_paths,inclussionDiameter=200,open_mask=True,showIntermediate=False):
    """
    Perform backround subtraction to find the target object
    """
    keyWaitDelay=400
    
    assert (len(blank_image_paths) == len(object_image_paths)) , "Lists of paths must have the same length!"
        
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    fgbg   = cv.createBackgroundSubtractorMOG2()

    frames = []
    for path in blank_image_paths:
        frames.append(cv.imread(path,0))
        #fgmask = fgbg.apply(cv.imread(path,0)) #[Land]
    frames = np.array(frames)
    avgFrame = np.mean(frames,axis=0).astype('u1')
    fgmask = fgbg.apply(avgFrame)
    
    if(showIntermediate):
        cv.namedWindow('BB_Gen')
        cv.moveWindow('BB_Gen', 1920,0)
        cv.imshow('BB_Gen',fgmask)
        cv.waitKey(keyWaitDelay)

    frames = []
    for path in object_image_paths:
        frames.append(cv.imread(path,0))
    frames = np.array(frames)
    avgFrame = np.mean(frames,axis=0).astype('u1')
    avgFrame = cv.imread(path,0)


    fgmask = fgbg.apply(avgFrame)
    if(open_mask):
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    if(showIntermediate):
        cv.imshow('BB_Gen',fgmask)
        cv.waitKey(keyWaitDelay)


    # Find contours
    contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours    = filter_contours_in_circle(frames[0].shape,contours,inclussionDiameter)

    if(showIntermediate and len(contours)>0):
        image = cv.imread(object_image_paths[0],1)
        image = draw_circle_and_contours(image, contours, inclussionDiameter)
        cv.imshow('BB_Gen',image)
        cv.waitKey(keyWaitDelay)

    if(len(contours)>0):
        largest_contour = sorted(contours, key=cv.contourArea,reverse = True)[0] # Get the bounding box of the largest contour
        BB = cv.boundingRect(largest_contour)
    else:
        BB=None


    if(showIntermediate and BB!=None):
        x, y, w, h = BB
        disp = cv.imread(object_image_paths[0],1)
        cv.rectangle(disp, (x, y), (x+w, y+h), (0, 255,0 ), 3)
        cv.imshow('BB_Gen',disp)
        cv.waitKey(keyWaitDelay)
        
    cv.destroyAllWindows()
    
    return BB

def get_BB_FrameDiff(blank_image_paths,object_image_paths,inclussionDiameter=200,showIntermediate=False):
    """
    Find target using image difference
    """
    keyWaitDelay=500
            
    assert (len(blank_image_paths) == len(object_image_paths)) , "Lists of paths must have the same length!"
        
    frames = []
    for path in blank_image_paths:
        frames.append(cv.imread(path,0))
        #fgmask = fgbg.apply(cv.imread(path,0)) #[Land]
    frames = np.array(frames)
    avgFrameBlank = np.mean(frames,axis=0)

    frames = []
    for path in object_image_paths:
        frames.append(cv.imread(path,0))
    frames = np.array(frames)
    avgFrame = np.mean(frames,axis=0)

    # Get image difference and mask
    mask = np.abs(avgFrameBlank-avgFrame)

    # Remap to 0-255 range
    min_val = mask.min()
    max_val = mask.max()

    remapped = 255 * (mask - min_val) / (max_val - min_val)
    mask = remapped.astype(np.uint8)
    # Show result
    if(showIntermediate):
        cv.namedWindow('Image_dfference')
        cv.moveWindow('Image_dfference', 1920,0)
        cv.imshow('Image_dfference', mask)
        cv.waitKey(keyWaitDelay)
        cv.destroyAllWindows()

    h, w = mask.shape
    x1 = w // 2 - inclussionDiameter // 2
    y1 = h // 2 - inclussionDiameter // 2
    x2 = x1 + inclussionDiameter
    y2 = y1 + inclussionDiameter

    # Extract center patch
    center_patch = mask[y1:y2, x1:x2]
    # Optionally blur the patch
    blur_patch = cv.GaussianBlur(center_patch, (5, 5), 0)
    # Compute Otsu threshold on patch
    patch_thresh_val, _ = cv.threshold(blur_patch, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Apply that threshold to the entire image
    _, mask = cv.threshold(mask, patch_thresh_val, 255, cv.THRESH_BINARY)

    # Show result
    if(showIntermediate):
        cv.namedWindow('Thresholded Image')
        cv.moveWindow('Thresholded Image', 1920,0)
        cv.imshow('Thresholded Image', mask)
        cv.waitKey(keyWaitDelay)
        cv.destroyAllWindows()

    # Find contours
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours    = filter_contours_in_circle(frames[0].shape,contours,inclussionDiameter)

    if(showIntermediate and len(contours)>0):
        image = cv.imread(object_image_paths[0],1)
        image = draw_circle_and_contours(image, contours, inclussionDiameter)
        cv.namedWindow('BB_Gen')
        cv.moveWindow('BB_Gen', 1920,0)
        cv.imshow('BB_Gen',image)
        cv.waitKey(keyWaitDelay)

    if(len(contours)>0):
        largest_contour = sorted(contours, key=cv.contourArea,reverse = True)[0] # Get the bounding box of the largest contour
        BB = cv.boundingRect(largest_contour)
    else:
        BB=None


    if(showIntermediate and BB!=None):
        x, y, w, h = BB
        disp = cv.imread(object_image_paths[0],1)
        cv.rectangle(disp, (x, y), (x+w, y+h), (0, 255,0 ), 3)
        cv.imshow('BB_Gen',disp)
        cv.waitKey(keyWaitDelay)
        
    cv.destroyAllWindows()
    
    return BB
    



if (__name__ == '__main__'):
    import glob
    pass
    # if(len(sys.argv)<4):
        # print("Too few arguments\nUse: python ARMA3_DG_BB.py \"pathToImages\" [\"blank1.png\",\"blank2.png\"] [\"object1.png\",\"object2.png\"]")
        # exit()
    # else:
        # print("SORRY, Standalone operation not yet implemented. [tt]")

    screenShotPath = str(r"C:/Users/user1/Documents/Arma 3/Screenshots/")
    object = glob.glob(screenShotPath+f'/*6-0.15*with.png')

    blank = glob.glob(screenShotPath+f'/*6-0.15*wout.png')

    x = np.array(get_BB_BackroundSubtraction(blank,object,inclussionDiameter=200,open_mask=True,showIntermediate=True))
  
