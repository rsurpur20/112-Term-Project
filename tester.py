import cv2
import numpy as np
import pyautogui 
import time
from cmu_112_graphics import *

#closing your eye 2-4 sec is click
#closing your eye 4-7 sec is scroll
#closing your eye 7-10 sec is disengage
def nothing(x):
    pass


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
        #  was 100
        areaMax=2000
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
            if areaMax>area> areaMin:
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
        #it was 200,2000
        areaMin=200
        areaMax=3000
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
            if areaMax>area> areaMin:
                self.area=area
            # frame, contour, ?, color, thickness
                cv2.drawContours(self.frame, [approx], 0 ,(0,0,0), thickness)
                # cv2.putText(self.frame, f"{area}",(x,y), font, 1, (0,0,255), thickness, cv2.LINE_AA)

                #finding the center:
                M = cv2.moments(cnt)
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    self.cx=cx
                    self.cy=cy
        self.dot=cv2.circle(self.frame, (self.cx,self.cy), 5, (255,0,0), 2)

def appStarted(app):
    app.cap = cv2.VideoCapture(0)
    app.LHEye=None
    app.LSEye=None
    app.LVEye=None
    app.LHPupil=None
    app.LSPupil=None
    app.LVPupil=None
    app.lowerPupil=None
    app.higherPupil=None

    app.lowerEye=None
    app.higherEye=None
    app.leftPupil=None
    app.rightPupil=None
    app.leftEye=None
    app.rightEye=None

    app.currX=400
    app.currY=500
    app.delta=10 #how much you want to move the mouse by

    app.movingEyesFeature=False
    app.clickscrollingFeature=False
    app.movingEyesFeatureUpandDown=False
    app.showLiveFeed=True
    app.screenx,app.screeny=pyautogui.size()
    app.originalLeftArea=0
    app.originalrightArea=0
    app.originalLeftEyecx=0
    app.originalLeftEyecy=0
    app.currleftBlink=False
    app.currrightBlink=False
    app.eyesClosed=False
    app.currentlyCalibrating=True
    app.startLeft=0
    app.startRight=0
    app.startDisengage=0

def timerFired(app):
    cv2.namedWindow("Trackbars for Eye")
    cv2.createTrackbar("LH", "Trackbars for Eye", 0,180, nothing)
    cv2.createTrackbar("LS", "Trackbars for Eye", 0,255, nothing)
    cv2.createTrackbar("LV", "Trackbars for Eye", 0,255, nothing)

    cv2.namedWindow("Trackbars for Pupil")
    cv2.createTrackbar("LH", "Trackbars for Pupil", 0,180, nothing)
    cv2.createTrackbar("LS", "Trackbars for Pupil", 0,255, nothing)
    cv2.createTrackbar("LV", "Trackbars for Pupil", 0,255, nothing)
    _, frame= app.cap.read()
    app.LHEye=cv2.getTrackbarPos("LH","Trackbars for Eye")
    app.LSEye=cv2.getTrackbarPos("LS","Trackbars for Eye")
    app.LVEye=cv2.getTrackbarPos("LV","Trackbars for Eye")
    app.LHPupil=cv2.getTrackbarPos("LH","Trackbars for Pupil")
    app.LSPupil=cv2.getTrackbarPos("LS","Trackbars for Pupil")
    app.LVPupil=cv2.getTrackbarPos("LV","Trackbars for Pupil")
    app.lowerPupil=np.array((app.LHPupil,app.LSPupil,app.LVPupil))

    app.higherPupil=np.array([180,255,255])

    app.lowerEye=np.array((app.LHEye,app.LSEye,app.LVEye))
    app.higherEye=np.array([180,255,255])

    leftFrame=frame[250:310,500:600]
    frameHeight=310-250
    frameWidth=600-500
    rightFrame=frame[250:310,600:700]
    eyeFrame = frame[250:310,500:700]

    app.leftPupil=Pupil(leftFrame, app.lowerPupil, app.higherPupil, "Left Pupil")
    app.rightPupil=Pupil(rightFrame, app.lowerPupil, app.higherPupil, "Right Pupil")
    app.leftEye=Eye(leftFrame, app.lowerEye, app.higherEye, "Left Eye")
    app.rightEye=Eye(rightFrame, app.lowerEye, app.higherEye, "Right Eye")

    #debugging:
    hsv=cv2.cvtColor(eyeFrame, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,app.lowerEye,app.higherEye)
    resize= cv2.resize(mask,(400,150),interpolation =cv2.INTER_AREA)
    maskPupils=cv2.inRange(hsv,app.lowerPupil,app.higherPupil)
    resizePupils= cv2.resize(maskPupils,(400,150),interpolation =cv2.INTER_AREA)


    app.leftPupil.finetune()
    app.rightPupil.finetune()
    app.leftEye.finetune()
    app.rightEye.finetune()

    app.leftPupil.loopContours()
    app.rightPupil.loopContours()
    app.leftEye.loopContours()
    app.rightEye.loopContours()
    

    cv2.imshow("Frame",eyeFrame)
    cv2.moveWindow("Frame", 725,30)
    cv2.moveWindow("Trackbars for Pupil", 550,200)
    cv2.moveWindow("Trackbars for Eye", 900,200)


    if not app.currentlyCalibrating:
        cv2.destroyWindow("Calibrating your Eyes")
        cv2.destroyWindow("Calibrating your Pupils")
        cv2.moveWindow("Trackbars for Pupil", 0,0)
        cv2.moveWindow("Trackbars for Eye", 0,0)
        cv2.moveWindow("Frame", 1100,0)
    else:
        cv2.moveWindow("Calibrating your Eyes", 900,430)
        cv2.moveWindow("Calibrating your Pupils", 490,430)
        cv2.imshow("Calibrating your Eyes",resize)
        cv2.imshow("Calibrating your Pupils",resizePupils)
 
    # cv2.imshow("Resize2",resize2)
    # if app.showLiveFeed:
    # cv2.imshow("left",leftFrame)
    # cv2.imshow("right",rightFrame)
        # cv2.imshow("Trackbars for Pupil")
    mouseMoving(app)
    clickandScroll(app)
    checkdisengage(app)
    

def checkdisengage(app):

    if not app.currentlyCalibrating:

        if app.leftPupil.area<=0 and app.rightPupil.area<=0: #both eyes are closed

            if not app.eyesClosed:
                app.startDisengage=time.time()
                app.eyesClosed=not app.eyesClosed
        if app.eyesClosed and 2<time.time()-app.startDisengage<4:
            if app.leftPupil.area<=0 and app.rightPupil.area<=0:
                app.movingEyesFeature=not app.movingEyesFeature
                app.movingEyesFeatureUpandDown=not app.movingEyesFeatureUpandDown
                print("switched!")
            else:
                app.startDisengage=time.time()
                app.eyesClosed=False
        if app.eyesClosed and 10<time.time()-app.startDisengage<13:
            if app.leftPupil.area<=0 and app.rightPupil.area<=0:
                app.movingEyesFeature=False
                app.clickscrollingFeature=False

            else:
                app.startDisengage=time.time()
                app.eyesClosed=False

        
            
def mouseMoving(app):
    #MOUSE MOVING START *************************************************************
    negibibledistance=0
    if app.movingEyesFeature:
        
        # app.originalLeftEyecx-app.leftPupil.cx,
        if app.originalLeftEyecx-app.leftPupil.cx<negibibledistance and app.originalRightEyecx-app.rightPupil.cx<negibibledistance:
            print("looking left")
            if app.currX-app.delta<0:
                app.currX=30
            else: app.currX-=app.delta
            
        elif app.originalLeftEyecx-app.leftPupil.cx>negibibledistance and app.originalRightEyecx-app.rightPupil.cx>negibibledistance:
            print("looking right")
            if app.currX+app.delta>app.screenx:
                app.currX=app.screenx-30
            else: app.currX+=app.delta

        pyautogui.moveTo(app.currX, app.currY) 
    if app.movingEyesFeatureUpandDown:
        if app.leftEye.cy-app.leftPupil.cy>negibibledistance or app.rightEye.cy-app.rightPupil.cy>negibibledistance:
            print("looking up")
            app.currY-=app.delta
        elif app.leftEye.cy-app.leftPupil.cy<negibibledistance or app.rightEye.cy-app.rightPupil.cy<negibibledistance:
            print("looking down")
            app.currY+=app.delta
        pyautogui.moveTo(app.currX, app.currY) 

#MOUSE MOVING END *************************************************************
def redrawAll(app,canvas):


    instructions="""
    How to calibrate!
    Step 1. Move your head so you are into the frame. 
    You can check in the "Frame" window on the top left

    Step 2. Move the trackbars. 
    One trackbar window is for calibrating your eyes, 
    the second is for calibrating your pupils. 
    You can check your calibration based on the black and 
    white version below the track bars, 
    or the contours drawn on top of your eyes.

    Step 3. Type "d" when done!
    """
    canvas.create_rectangle(0,0,app.width,app.height,fill="lightblue")
    if app.currentlyCalibrating:
        start=10
        y=150
        for line in instructions.splitlines():
            canvas.create_text(app.width//2, start+y, text=line.strip())
            y += 20
        
    else:
        start=app.height//2
    
    canvas.create_text(app.width//2,start,text="Welcome to Mouseless!")
    canvas.create_text(app.width//2,start+15,text="How this works:")
    canvas.create_text(app.width//2,start+35,text="Step 1: Calibrate your eyes. Press 'd' when you are done calibrating.")
    canvas.create_text(app.width//2,start+55,text="Step 2: Press '1' to be able to move your mouse")
    canvas.create_text(app.width//2,start+75,text="Step 2: Press '2' to be able to click and scroll around")
    #current modes
    canvas.create_text(app.width//2,start+95,text=f"Calibration Mode: %s" %("On" if app.currentlyCalibrating else "Off"))
    canvas.create_text(app.width//2,start+115,text=f"Clicking and Scrolling Mode: %s" %("On" if app.clickscrollingFeature else "Off"))
    canvas.create_text(app.width//2,start+135,text=f"Mouse Moving Mode Left and Right: %s" %("On" if app.movingEyesFeature else "Off"))
    canvas.create_text(app.width//2,start+155,text=f"Mouse Moving Mode Up and Down: %s" %("On" if app.movingEyesFeatureUpandDown else "Off"))

def clickandScroll(app):
#CLICK AND SCROLL START *************************************************************
    if app.clickscrollingFeature:

        if app.leftPupil.area<=0 and app.rightPupil.area>0: #if left eye closed
            if not app.currleftBlink: # and you weren't already blinking, 
                app.startLeft=time.time() #get the start time
                app.currleftBlink= not app.currleftBlink
        if app.currleftBlink and 2<time.time()-app.startLeft<4:
            if app.leftPupil.area>0 and app.rightPupil.area>0: #left eye open
                print("right click")
                pyautogui.rightClick(app.currX,app.currY)
                app.currleftBlink=False
        if app.currleftBlink and 4<time.time()-app.startLeft<7:
            if app.leftPupil.area<=0 and app.rightPupil.area>0: #left eye still closed
                print("right scroll") 
                pyautogui.scroll(-10)      
            else: 
                app.startLeft=time.time()
                app.currleftBlink=False

        # print(time.time())
        if app.rightPupil.area<=0 and app.leftPupil.area>0: #if right eye closed
            if not app.currrightBlink: # and you weren't already blinking, 
                app.startRight=time.time() #get the start time
                app.currrightBlink= not app.currrightBlink
        if app.currrightBlink and 2<time.time()-app.startRight<4:
            if app.rightPupil.area>0 and app.leftPupil.area>0: #right eye open
                print("left click")
                pyautogui.leftClick(app.currX,app.currY)
                app.currrightBlink=False
        if app.currrightBlink and 4<time.time()-app.startRight<7:
            if app.rightPupil.area<=0 and app.leftPupil.area>0: #right eye still closed
                print("left scroll")
                pyautogui.scroll(+10)           
            else: 
                app.startLeft=time.time()
                app.currrightBlink=False
        # if app.currleftBlink and app.currrightBlink and 7<time.time()-app.startLeft<10 and 7<time.time()-app.startRight<10:
            print("disengage!")
#CLICK AND SCROLL END *************************************************************


def keyPressed(app,event):
#KEY PRESSED START *************************************************************
    if event.key=="1" and not app.movingEyesFeatureUpandDown:
        app.movingEyesFeature=not app.movingEyesFeature
        app.currX=400
        app.currY=500
        app.originalLeftEyecx=app.leftEye.cx
        app.originalLeftEyecy=app.leftEye.cx
        app.originalRightEyecx=app.rightEye.cx
        app.originalRightEyecy=app.rightEye.cy


    if event.key=="2": #key number k
        app.originalLeftArea=app.leftPupil.area
        app.originalrightArea=app.rightPupil.area
        app.clickscrollingFeature= not app.clickscrollingFeature
    if event.key=="d":
        app.currentlyCalibrating=not app.currentlyCalibrating
    if event.key=="3" and not app.movingEyesFeature:
        app.movingEyesFeatureUpandDown= not app.movingEyesFeatureUpandDown
    # if event.key=="Down" and app.movingEyesFeature:
    #     app.currY+=app.delta
    # elif event.key=="Up" and app.movingEyesFeature:
    #     app.currY-=app.delta
#KEY PRESSED END ***************************************************************


    

runApp(width=490, height=500)