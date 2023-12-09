import cv2 
import mediapipe as mp 
import time 


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectConf=0.5, trackConf=0.5):
        self.mode = mode 
        self.maxHands = maxHands
        self.detectConf = detectConf
        self.trackConf = trackConf
            
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectConf,
                                        min_tracking_confidence=self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        results = self.results
        
        # Check if the cam detect a hand
        if results.multi_hand_landmarks:
            # for hand landmark in results
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)    
        return img
    
    def findPosition(self, img, handNum=0, draw=True):
        # landmark list
        self.lmList = []
        lmList = self.lmList
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(myHand.landmark):
                # height, width, chanels
                h, w, c = img.shape
                # center x & y
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    # custom RGB, size etc
                    cv2.circle(img, (cx, cy), 8, (200, 48, 182), cv2.FILLED)
        return lmList
    
    def fingersUp(self):
        fingers = []
        tipIds = self.tipIds
        lmList = self.lmList
        
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else: 
                fingers.append(0)
        return fingers
    
    def fps(self, img, pTime, displayFPS=False):
        if displayFPS:
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'{int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 210, 0), 3)
        return img, pTime