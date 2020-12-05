import cv2
import numpy as np
import pyautogui 
import time
import math
#resources used:
# https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/


#by mvp: direction oriented, right blink, finetuning (calibration that is user friendly)
#re-do storyboard (by tp2)
#tp2 is next monday- implement direction based eye tracking, right eye blinking, finetuning the contours,
#calibration, 
#goals for the night: find the center of the pupils

def nothing(x):
    pass
cap = cv2.VideoCapture(0)

class Pupil(object):
    def __init__(self, frame, lower, upper,name):
        self.frame=frame
        self.lower= lower
        self.upper=upper
        self.name=name
        self.hsv=cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask= cv2.inRange(self.hsv,self.lower,self.upper)
        self.contours, self.a = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.area=0
        self.cx=0
        self.cy=0

    def finetune(self):
        #help finetune
        thickness=9
        kernel= np.ones((thickness,thickness), np.uint8) #arrays of 1
        self.mask=cv2.erode(self.mask,kernel, iterations=5)
        self.mask = cv2.dilate(self.mask, kernel, iterations=5)

    def loopContours(self):
        ratio=0.04
        areaMin=200
        pupilAreaMin=400
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        lastArea=0
        lastLeftPupilArea=0
        thickness=2
        i=0
        # cnt=self.contours[0]
        # print(len(self.contours))
        for cnt in self.contours:
            area = cv2.contourArea(cnt) #gets the area of each contour
            
            #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
            approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
            x=approx.ravel()[0]
            y=approx.ravel()[1]
            #only draw area if pixels is greater than this num. this gets rid of noise
            if 2000>area> areaMin:
            # frame, contour, ?, color, thickness
                if 3 <len(approx)<10:
                    self.area=area
                    # location, font, thickness?, color
                    cv2.drawContours(self.frame, [approx], 0 ,(0,0,255), thickness)
                    # cv2.putText(self.frame,f"{area}", (x,y),font,1,(0,0,0))

                # #finding the center:
                M = cv2.moments(cnt)
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    # cv2.putText(self.frame,f"({cx},{cy})", (cx,cy),font,1,(0,0,0))
                    self.cx=cx
                    self.cy=cy
                
        self.dot=cv2.circle(self.frame, (self.cx,self.cy), 5, (0,255,0), 2)

class Eye(Pupil):
    def loopContours(self):
        ratio=0.04
        areaMin=200
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        lastArea=0
        lastLeftPupilArea=0
        thickness=2
        i=0
        xlst=[]
        ylst=[]
        # cnt=self.contours[0]
        for cnt in self.contours:
            area = cv2.contourArea(cnt) #gets the area of each contour
                
            #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
            approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
            x=approx.ravel()[0]
            y=approx.ravel()[1]
            #only draw area if pixels is greater than this num. this gets rid of noise
            if 2000>area> areaMin:
                self.area=area
            # frame, contour, ?, color, thickness
                cv2.drawContours(self.frame, [approx], 0 ,(0,0,0), thickness)
                #finding the center:
                M = cv2.moments(cnt)
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    # cv2.putText(self.frame,f"({cx},{cy})", (cx,cy),font,1,(0,0,0))
                    self.cx=cx
                    self.cy=cy
        self.dot=cv2.circle(self.frame, (self.cx,self.cy), 5, (255,0,0), 2)



cv2.namedWindow("Trackbars for Eye")
cv2.createTrackbar("LH", "Trackbars for Eye", 0,180, nothing)
cv2.createTrackbar("LS", "Trackbars for Eye", 0,255, nothing)
cv2.createTrackbar("LV", "Trackbars for Eye", 0,255, nothing)

cv2.namedWindow("Trackbars for Pupil")
cv2.createTrackbar("LH", "Trackbars for Pupil", 0,180, nothing)
cv2.createTrackbar("LS", "Trackbars for Pupil", 0,255, nothing)
cv2.createTrackbar("LV", "Trackbars for Pupil", 0,255, nothing)
# cv2.moveWindow("Trackbars for Pupil", 1200,500)
# cv2.moveWindow("Trackbars for Eye", 1200,800)
lastAreaLeft=0
lastAreaRight=0
lastContourList=[0]
currX=400
currY=500
delta=10
x=True
movingEyes=False
screenx,screeny=pyautogui.size()


def dist(x1,y1,x2,y2):
    return math.sqrt( ((x2-x1)**2)+((y2-y1)**2) )

def getCenters(frame,contours):
    for cnt in contours:       #finding the center:
        M = cv2.moments(cnt)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # cv2.putText(self.frame,f"({cx},{cy})", (cx,cy),font,1,(0,0,0))
            cx=cx
            cy=cy
            
    cv2.circle(frame, (cx,cy), 5, (0,255,0), 2)
    return cx, cy
lastLeftArea=0
lastRightArea=0
originalLeftArea=0
originalrightArea=0
leftBlink=False
rightBlink=False
while True:
    _, frame= cap.read()
    
    LHEye=cv2.getTrackbarPos("LH","Trackbars for Eye")
    LSEye=cv2.getTrackbarPos("LS","Trackbars for Eye")
    LVEye=cv2.getTrackbarPos("LV","Trackbars for Eye")
    LHPupil=cv2.getTrackbarPos("LH","Trackbars for Pupil")
    LSPupil=cv2.getTrackbarPos("LS","Trackbars for Pupil")
    LVPupil=cv2.getTrackbarPos("LV","Trackbars for Pupil")
    lowerPupil=np.array((LHPupil,LSPupil,LVPupil))
    # lowerPupil=np.array((0,0,60))
    higherPupil=np.array([180,255,255])
    # [4,87,82]
    #[0,89,62]
    #[0,88,103]
    lowerEye=np.array((LHEye,LSEye,LVEye))
    # lowerEye=np.array([0,89,74])
    higherEye=np.array([180,255,255])

    leftFrame=frame[250:310,500:600]
    frameHeight=310-250
    frameWidth=600-500
    rightFrame=frame[250:310,600:700]
    eyeFrame = frame[250:310,500:700]

    leftPupil=Pupil(leftFrame, lowerPupil, higherPupil, "Left Pupil")
    rightPupil=Pupil(rightFrame, lowerPupil, higherPupil, "Right Pupil")
    leftEye=Eye(leftFrame, lowerEye, higherEye, "Left Eye")
    rightEye=Eye(rightFrame, lowerEye, higherEye, "Right Eye")

    #debugging:
    hsv=cv2.cvtColor(eyeFrame, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lowerEye,higherEye)
    resize= cv2.resize(mask,(400,150),interpolation =cv2.INTER_AREA)

    lefthsv=cv2.cvtColor(leftFrame, cv2.COLOR_BGR2HSV)
    mask1=cv2.inRange(lefthsv,lowerPupil,higherPupil)
    resize1= cv2.resize(mask1,(400,150),interpolation =cv2.INTER_AREA)

    righthsv=cv2.cvtColor(rightFrame, cv2.COLOR_BGR2HSV)
    mask2=cv2.inRange(righthsv,lowerPupil,higherPupil)
    resize2= cv2.resize(mask2,(400,150),interpolation =cv2.INTER_AREA)

    leftPupil.finetune()
    rightPupil.finetune()
    leftEye.finetune()
    rightEye.finetune()

    leftPupil.loopContours()
    rightPupil.loopContours()
    leftEye.loopContours()
    rightEye.loopContours()
    

    cv2.namedWindow("Frame")
    cv2.namedWindow("Resize")
    cv2.namedWindow("Resize1")
    cv2.namedWindow("left")
    cv2.namedWindow("right")
    cv2.moveWindow("Frame", 20,30)
    cv2.resizeWindow('Frame', 300,300)
    cv2.moveWindow("Resize", 300,30)
    cv2.moveWindow("Resize1", 700,30)
    cv2.moveWindow("left", 40,500)
    cv2.moveWindow("right", 350,500)
    cv2.imshow("Frame",frame)
    cv2.imshow("Resize",resize)
    cv2.imshow("Resize1",resize1)
    cv2.imshow("Resize2",resize2)
    cv2.imshow("left",leftFrame)
    cv2.imshow("right",rightFrame)

    lastAreaLeft=leftEye.area

    # areaMin=200

    # if 2000>lastAreaLeft> areaMin and leftEye.area<.5*lastAreaLeft:
    #     print("LeftBlink")

    if movingEyes:

        leftEyecx,leftEyecy=getCenters(leftFrame,leftEye.contours)
        rightEyecx,rightEyecy=getCenters(rightFrame,rightEye.contours)
        dLeft=dist(leftPupil.cx,leftPupil.cy,leftEye.cx,leftEye.cy)
        dRight=dist(rightPupil.cx,rightPupil.cy,rightEye.cx,rightEye.cy)
 
        # if leftEye.cx-leftPupil.cx<0:
        # # print("looking left")
        #     currX-=delta
        # else:
        #     # print("looking right")
        #     currX+=delta
        # if leftEye.cy-leftPupil.cy<0:
        # # print("looking left")
        #     currY-=delta
        # else:
        #     # print("looking right")
        #     currY+=delta
        # pyautogui.moveTo(currX, currY) 
    key=cv2.waitKey(1)
    dleftArea=leftPupil.area-lastLeftArea
    drightArea=rightPupil.area-lastRightArea
    lastLeftArea=leftPupil.area
    lastRightArea=rightPupil.area
    
    if originalrightArea>0:
        # time.sleep(.5)
        # print(leftPupil.area,rightPupil.area)
        # time.sleep(1)
        # if dleftArea<0 and drightArea>0:
        #     print("left blink")
        # if dleftArea>0 and drightArea<0:
        #     print("right blink")
        if leftPupil.area<=0 and rightPupil.area>0:
            if not leftBlink:
                startLeft=time.time()
                leftBlink= not leftBlink
            if time.time()-startLeft>1:
                print("right blink")
                leftBlink=False
        if rightPupil.area<=0 and leftPupil.area>0:
            if not rightBlink:
                startRight=time.time()
                rightBlink= not rightBlink
            if time.time()-startRight>1:
                print("left blink")
                rightBlink=False
    #if it is too less, video will be very fast and if it is too high, 
    # video will be slow (Well, that is how you can display videos in slow motion).
    #  25 milliseconds will be OK in normal cases.
    if key==27: #escape key
        break

    if key==53: #key number 5
        movingEyes=not movingEyes
        currX=400
        currY=500

    if key==107:
        # print(originalLeftArea,originalrightArea)
        originalLeftArea=leftPupil.area
        originalrightArea=rightPupil.area
        print("original:")
        print(originalLeftArea,originalrightArea)




cap.release()
cv2.destroyAllWindows()