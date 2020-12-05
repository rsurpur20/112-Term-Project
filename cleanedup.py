import cv2
import numpy as np
import pyautogui 
import time
# from cmu_112_graphics import *
# import basic_graphics

#resources used:
# https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/




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
        pupilAreaMin=200 #was 400
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        lastLeftPupilArea=0
        thickness=2

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

                # #finding the center:
                M = cv2.moments(cnt)
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    self.cx=cx
                    self.cy=cy
                
        self.dot=cv2.circle(self.frame, (self.cx,self.cy), 5, (0,255,0), 2)

class Eye(Pupil):
    def loopContours(self):
        ratio=0.04
        areaMin=200
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        thickness=2
        i=0
        xlst=[]
        ylst=[]
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

currX=400
currY=500
delta=10
movingEyesFeature=False
clickscrollingFeature=False
showInstructionsFeature=True
step1Feature=False
screenx,screeny=pyautogui.size()



originalLeftArea=0
originalrightArea=0
currleftBlink=False
currrightBlink=False

step1 = cv2.imread('step.jpg')
step1 = cv2.resize(step1, (500, 500)) 
while True:
    _, frame= cap.read()
    if showInstructionsFeature:
        cv2.imshow("Step 1", step1) 
    # if step1Feature:
    LHEye=cv2.getTrackbarPos("LH","Trackbars for Eye")
    LSEye=cv2.getTrackbarPos("LS","Trackbars for Eye")
    LVEye=cv2.getTrackbarPos("LV","Trackbars for Eye")
    LHPupil=cv2.getTrackbarPos("LH","Trackbars for Pupil")
    LSPupil=cv2.getTrackbarPos("LS","Trackbars for Pupil")
    LVPupil=cv2.getTrackbarPos("LV","Trackbars for Pupil")
    lowerPupil=np.array((LHPupil,LSPupil,LVPupil))
    higherPupil=np.array([180,255,255])
    # [4,87,82]
    #[0,89,62]
    #[0,88,103]
    lowerEye=np.array((LHEye,LSEye,LVEye))
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


#MOUSE MOVING START *************************************************************
    if movingEyesFeature:
        negibibledistance=0
        if originalLeftEyecx-leftPupil.cx<negibibledistance and originalRightEyecx-rightPupil.cx<negibibledistance:
            print("looking left")
            if currX-delta<0:
                currX=30
            else: currX-=delta
            
        elif originalLeftEyecx-leftPupil.cx>negibibledistance and originalRightEyecx-rightPupil.cx>negibibledistance:
            print("looking right")
            if currX+delta>screenx:
                currX=screenx-30
            else: currX+=delta
        elif leftEye.cy-leftPupil.cy>negibibledistance and rightEye.cy-rightPupil.cy>negibibledistance:
            print("looking up")
            currY-=delta
        elif leftEye.cy-leftPupil.cy<negibibledistance and rightEye.cy-rightPupil.cy<negibibledistance:
            print("looking down")
            currY+=delta

#MOUSE MOVING END *************************************************************

#CLICK AND SCROLL START *************************************************************

    if clickscrollingFeature:

        if leftPupil.area<=0 and rightPupil.area>0: #if left eye closed
            if not currleftBlink: # and you weren't already blinking, 
                startLeft=time.time() #get the start time
                currleftBlink= not currleftBlink
        if currleftBlink and 1<time.time()-startLeft<3:
            if leftPupil.area>0 and rightPupil.area>0: #left eye open
                print("right click")
                currleftBlink=False
        if currleftBlink and time.time()-startLeft>3:
            if leftPupil.area<=0 and rightPupil.area>0: #left eye still closed
                print("right scroll")       
            else: 
                startLeft=time.time()
                currleftBlink=False

        if rightPupil.area<=0 and leftPupil.area>0: #if right eye closed
            if not currrightBlink: # and you weren't already blinking, 
                startRight=time.time() #get the start time
                currrightBlink= not currrightBlink
        if currrightBlink and 1<time.time()-startRight<3:
            if rightPupil.area>0 and leftPupil.area>0: #right eye open
                print("left click")
                currrightBlink=False
        if currrightBlink and time.time()-startRight>3:
            if rightPupil.area<=0 and leftPupil.area>0: #right eye still closed
                print("left scroll")       
            else: 
                startLeft=time.time()
                currrightBlink=False
#CLICK AND SCROLL END *************************************************************
#KEY PRESSED START *************************************************************
    key=cv2.waitKey(1)
    #if it is too less, video will be very fast and if it is too high, 
    # video will be slow (Well, that is how you can display videos in slow motion).
    #  25 milliseconds will be OK in normal cases.
    if key==27: #escape key
        break

    if key==53: #key number 5
        movingEyesFeature=not movingEyesFeature
        currX=400
        currY=500
        originalLeftEyecx=leftEye.cx
        originalLeftEyecy=leftEye.cx
        originalRightEyecx=rightEye.cx
        originalRightEyecy=rightEye.cy
    if key==107: #key number k
        originalLeftArea=leftPupil.area
        originalrightArea=rightPupil.area
        clickscrollingFeature= not clickscrollingFeature

#KEY PRESSED END ***************************************************************




cap.release()
cv2.destroyAllWindows()