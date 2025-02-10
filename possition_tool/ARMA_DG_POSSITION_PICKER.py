import tkinter as tk
import tkinter.messagebox 
import threading
from time import sleep
from pyautogui import screenshot
import numpy as np
import cv2
import pytesseract

# Using OCR requires you to install it and set teh correct path to the exe.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

exitFlag = False

def find_region(image):
    r = cv2.selectROI("select the area", image)
    cv2.destroyAllWindows()
    return(r)


def store_pos(x,y):
    """
    Store the location 
    (Here i just print the result. Add your code Here to 
    save the possitions to CSV or any other format)
    """
    print('Stored: %8.2f  %8.2f'%(x,y))

# Clean the text read from OCR because some numbers may we read as letters
def clean_pos_text(pos):
    allowed = '0123456789.'
    new = ''
    for c in pos:
        if(c in allowed):
            new+=c
        elif(c=='o' or c=='O'):
            new+='0'
        elif(c=='i' or c=='I'):
            new+='1'
        elif(c=='s' or c=='S'):
            new+='5'
        elif(c=='z' or c=='Z'):
            new+='2'
        elif(c=='A'):
            new+=4
    return new

def background_task():
    global root,exitFlag
    _screenshot = np.array(screenshot())
    update_status("black", "X Region")
    xRegion = find_region(_screenshot)
    update_status("black", "Y Region")
    yRegion = find_region(_screenshot)

    validRange = [3,4,5,6,7]
    posStableCnt = 1 
    xPrev = 0
    yPrev = 0
    while(not exitFlag):
        sleep(0.2)
        xIm   = np.array(screenshot(region=xRegion))
        yIm   = np.array(screenshot(region=yRegion))
        xTxt  = pytesseract.image_to_string(xIm)
        yTxt = pytesseract.image_to_string(yIm)
        x = float(clean_pos_text(xTxt))
        y = float(clean_pos_text(yTxt))
        if(xPrev == x and yPrev == y):
            posStableCnt+=1
            if(posStableCnt in validRange):
                color='green'
            elif(posStableCnt< min(validRange)):
                color='red'
            else:
                color='gray14'
        else:
            if(posStableCnt in validRange):
                store_pos(x,y)
            xPrev= x ; yPrev= y
            posStableCnt =1
            color='OrangeRed4'

        update_status(color, str(x)+'\n'+str(y))

# Function to start the background task when a button is pressed
def start_background_task():
    global bg_thread
    # Start the background task in a new thread
    threading.Thread(target=background_task, daemon=True).start()
    start_button.config(state="disabled")

def on_quit():
    global exitFlag,bg_thread
    exitFlag = True
    print("Waiting for thread to close")
    sleep(1)
    root.destroy()

def update_status(color, message):
    # Update the indicator color
    indicator.config(bg=color)
    # Update the text message
    message_label.config(text=message)
    root.update()

# Create the main window
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_quit)
root.title("Status Window")
root.geometry("400x140")
#root.resizable(False, False)
start_button = tk.Button(root, height=8, width=10, text="Start", command=start_background_task)
start_button.grid(row=0, column=0, padx=2)
indicator = tk.Canvas(root, width=120, height=120, bg="gray", bd=0, highlightthickness=0)
indicator.grid(row=0, column=1, padx=5)
message_label = tk.Label(root, text="Waiting for action...", font=("Arial", 14))
message_label.grid(row=0, column=2)
tkinter.messagebox.showinfo("ARMA3 Location tool",  "Set the game in wondowed mode and place it at the upper left corner of the screen. \
This wil allow you to see the tool gui at the same time. Set the GUI size in video Options to large for better accuracy in image to text convertion")

root.mainloop()