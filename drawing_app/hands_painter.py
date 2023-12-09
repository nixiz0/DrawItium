import random
import cv2 
import os 
import numpy as np 
import threading
import time

from drawing_app.HandTrackingModule import HandDetector


#--- Generate Random Color ---#
# Global variables for color components
red = green = blue = 0

# Function to update random color every 3 seconds
def update_random_color():
    global red, green, blue
    while True:
        red = random.randint(10, 250)
        green = random.randint(10, 250)
        blue = random.randint(10, 250)
        time.sleep(3)

def start_draw(num_cam, width_cam, height_cam, superpos=False):
    # Start thread to update color
    color_thread = threading.Thread(target=update_random_color)
    color_thread.daemon = True # Allows the thread to terminate with the program
    color_thread.start()

    folder_path = "drawing_app/images"
    myList = os.listdir(folder_path)
    overlayList = []

    for img_path in myList:
        image = cv2.imread(f'{folder_path}/{img_path}', cv2.IMREAD_UNCHANGED)
        overlayList.append(image)
        
    header = overlayList[0]
    drawColor = (0, 0, 0)
    brushThickness = 15
    eraserThickness = 40

    cap = cv2.VideoCapture(num_cam)

    # Set the width and height of the camera screen
    cap.set(3, width_cam)  # Width
    cap.set(4, height_cam)  # Height

    detector = HandDetector(detectConf=0.85)
    xp, yp = 0, 0
    imgCanvas = np.zeros((480, 640, 3), np.uint8)

    # Create an empty image of the same size as imgCanvas
    height, width, _ = imgCanvas.shape
    blank_image = np.zeros((height, width, 3), np.uint8)
    
    while True: 
        success, img = cap.read()
        img = cv2.flip(img, 1)        
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # index & middle hand fingers
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            
            # check which fingers are up
            fingers = detector.fingersUp()
            
            # check if select or selection mode
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                # custom width & height & color of rectangle selection
                cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), drawColor, cv2.FILLED)
                if y1 < 65:
                    # check for first element
                    if 0 < x1 < 40:
                        header = overlayList[1]
                        drawColor = (red, green, blue)
                    elif 40 < x1 < 80:
                        header = overlayList[2]
                        drawColor = (42, 0, 255)
                    elif 80 < x1 < 120:
                        header = overlayList[3]
                        drawColor = (255, 136, 0)
                    elif 120 < x1 < 160:
                        header = overlayList[4]
                        drawColor = (75, 192, 7)
                    elif 310 < x1 < 360:
                        header = overlayList[5]
                        # Reset imgCanvas with empty image
                        imgCanvas = blank_image.copy()
                    elif 500 < x1 < 550:
                        header = overlayList[6]
                        brushThickness = 15
                        eraserThickness = 20
                    elif 550 < x1 < 590:
                        header = overlayList[7]
                        brushThickness = 25
                        eraserThickness = 40
                    elif 590 < x1 < 630:
                        header = overlayList[8]
                        drawColor = (0, 0, 0)
                    else:
                        header = overlayList[0]
                        drawColor = (255, 255, 255)
                
            if fingers[1]==False and fingers[2]==False:
                xp, yp = 0, 0
                
            # Drawing
            if fingers[1] and fingers[2]==False:
                cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                    
                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else: 
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp, yp = x1, y1
                
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)
        
        # Resize the image to choose to enlarge or shrink it
        desired_width = 1280
        desired_height = 480

        original_height, original_width = header.shape[:2]
        ratio = min(desired_width / original_width, desired_height / original_height)
        header_resized = cv2.resize(header, (int(original_width * ratio), int(original_height * ratio)))
        
        # Get the dimensions of the area where you want to apply the header image
        target_height, target_width = header_resized.shape[:2]
        
        # Make sure the mask has the same dimensions as the area where you want to apply the header image
        alpha_mask = header_resized[:, :, 3] / 255.0
        alpha_inv_mask = 1 - alpha_mask
        
        # Resize the mask to match the size of the target area
        alpha_mask = cv2.resize(alpha_mask, (target_width, target_height))
        alpha_inv_mask = cv2.resize(alpha_inv_mask, (target_width, target_height))
        
        # Apply mask to camera image
        mask = cv2.merge((alpha_inv_mask, alpha_inv_mask, alpha_inv_mask))
        img[0:target_height, 0:target_width] = cv2.multiply(img[0:target_height, 0:target_width], mask.astype(img.dtype))
        
        # Add the resized header image to the camera image
        img[0:target_height, 0:target_width] += (header_resized[:, :, :3] * np.dstack([alpha_mask, alpha_mask, alpha_mask])).astype('uint8')
        
        if superpos:
            # for superposition of 2 images
            img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
            cv2.imshow("Drawing Screen & Picture", img)
        else:
            cv2.imshow("Drawing Screen", img)
            cv2.imshow("Drawing Picture", imgCanvas)
        if cv2.waitKey(1) == 32:
            cap.release()
            cv2.destroyAllWindows()
            break