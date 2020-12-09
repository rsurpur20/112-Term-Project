#################################################
# Term Project
#
# Your name: Roshni Surpur
# Your andrew id: rsurpur
################################################
import cv2
import numpy as np
import pyautogui 
import time
from cmu_112_graphics import *

#this is a cv2 function necessary for the trackbars
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
        areaMax=2000
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        lastLeftPupilArea=0
        thickness=2

        for cnt in self.contours:
            area = cv2.contourArea(cnt) #gets the area of each contour
            
            #detecting shapes: 
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
        areaMin=200
        areaMax=3000
        font= cv2.FONT_HERSHEY_COMPLEX_SMALL
        thickness=2

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


    app.movingEyesFeature=False
    app.clickscrollingFeature=False
    app.movingEyesFeatureUpandDown=False
    app.showLiveFeed=True
    app.screenx,app.screeny=pyautogui.size()
    app.originalLeftArea=0
    app.originalrightArea=0
    app.originalLeftEyecx=0
    app.originalLeftEyecy=0
    app.originalRightEyecx=0
    app.originalRightEyecy=0
    app.currleftBlink=False
    app.currrightBlink=False
    app.eyesClosed=False
    app.currentlyCalibrating=True
    app.startLeft=0
    app.startRight=0

    app.startDisengage=0
    app.currX=app.screenx//2
    app.currY=app.screeny//2
    app.delta=10 #how much you want to move the mouse by

def timerFired(app):
    #trackbars:
    cv2.namedWindow("Trackbars for Eye")
    cv2.createTrackbar("LH", "Trackbars for Eye", 0,180, nothing)
    cv2.createTrackbar("LS", "Trackbars for Eye", 0,255, nothing)
    cv2.createTrackbar("LV", "Trackbars for Eye", 0,255, nothing)

    cv2.namedWindow("Trackbars for Pupil")
    cv2.createTrackbar("LH", "Trackbars for Pupil", 0,180, nothing)
    cv2.createTrackbar("LS", "Trackbars for Pupil", 0,255, nothing)
    cv2.createTrackbar("LV", "Trackbars for Pupil", 0,255, nothing)
    
    _, frame= app.cap.read() #gets live video feed

    #gets info from trackbars
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

    #adjusts to only capture eyes
    leftFrame=frame[250:310,500:600]
    frameHeight=310-250
    frameWidth=600-500
    rightFrame=frame[250:310,600:700]
    eyeFrame = frame[250:310,500:700]

    #creating instances of my pupil and eye classes
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

    #hide calibration trackbars:
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
 
    mouseMoving(app)
    clickandScroll(app)
    checkdisengage(app)
    

def checkdisengage(app):

    if not app.currentlyCalibrating:

        if app.leftPupil.area<=0 and app.rightPupil.area<=0: #both eyes are closed
            app.delta=0
            if not app.eyesClosed:
                app.startDisengage=time.time()
                app.eyesClosed=not app.eyesClosed
        else:app.delta=5
        # print(app.eyesClosed,time.time()-app.startDisengage)
        if app.eyesClosed and 2<time.time()-app.startDisengage<4: #if both eyes closed for 2-4 seconds, then toggle mouse moving features
            if app.leftPupil.area<=0 and app.rightPupil.area<=0: #if closed eyes
                app.movingEyesFeature=not app.movingEyesFeature
                app.movingEyesFeatureUpandDown=not app.movingEyesFeatureUpandDown
                print("switched!")
                app.eyesClosed=False
            else:
                app.startDisengage=time.time()
                app.eyesClosed=False

        if app.eyesClosed and 7<time.time()-app.startDisengage<10: # if time between 7-10, then disengage
            if app.leftPupil.area<=0 and app.rightPupil.area<=0: #if closed eyes
                app.movingEyesFeature=False
                app.movingEyesFeatureUpandDown=False
                app.clickscrollingFeature=False
                print("disengage!")
            else:
                app.startDisengage=time.time()
                app.eyesClosed=False
                print("didn't disengage")

        
#MOUSE MOVING START *************************************************************
def mouseMoving(app):
    negibibledistance=0 #change if you want to account for error
    if app.movingEyesFeature: #left and right feature

        #detect if pupils is in the left part of both eyes by finding relative positions of center of pupils
        if app.originalLeftEyecx-app.leftPupil.cx<negibibledistance and app.originalRightEyecx-app.rightPupil.cx<negibibledistance:
            print("looking left")
            app.currX-=app.delta
        #detect if pupils is in the right part of both eyes by finding relative positions of center of pupils
        elif app.originalLeftEyecx-app.leftPupil.cx>negibibledistance and app.originalRightEyecx-app.rightPupil.cx>negibibledistance:
            print("looking right")
            app.currX+=app.delta
        checkLegality(app)
        #move mouse:
        pyautogui.moveTo(app.currX, app.currY)

    if app.movingEyesFeatureUpandDown: #up and down feature
       
        #detect if pupils is in the upper part of both eyes by finding relative positions of center of pupils
        if app.leftEye.cy-app.leftPupil.cy>negibibledistance and app.rightEye.cy-app.rightPupil.cy>negibibledistance:
            print("looking up")
            app.currY-=app.delta
        
        #detect if pupils is in the upper part of both eyes by finding relative positions of center of pupils
        elif app.leftEye.cy-app.leftPupil.cy<negibibledistance and app.rightEye.cy-app.rightPupil.cy<negibibledistance:
            print("looking down")
            app.currY+=app.delta
        checkLegality(app)
        #move mouse:
        pyautogui.moveTo(app.currX, app.currY) 

def checkLegality(app):
    if app.currX-app.delta<0:
        app.currX=30
    elif app.currX-app.delta>app.screenx:
        app.currX=app.screenx-30
    elif app.currY-app.delta>app.screeny:
        app.currY=app.screeny-30
    elif app.currY-app.delta<0:
        app.currY=30

#MOUSE MOVING END *************************************************************
def redrawAll(app,canvas):
    instructions="""
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
        canvas.create_text(app.width//2, 270, text="How to Calibrate!",font='Arial 15 bold')

        start=275
        y=0
        for line in instructions.splitlines():
            canvas.create_text(app.width//2, start+y, text=line.strip())
            y += 20
        functionstart=24
        
    else:
        start=app.height//2
        functionstart=13
    start=40
    spacing=20
    canvas.create_text(app.width//2,start,text="Welcome to Mouseless!", font='Arial 26 bold')
    canvas.create_text(app.width//2,start+spacing,text="How this works:",font='Arial 15 bold')
    canvas.create_text(app.width//2,start+2*spacing,text="Step 1: Calibrate your eyes. Press 'd' when you are done calibrating.")
    canvas.create_text(app.width//2,start+3*spacing,text="Step 2: Press '1' to be able to click and scroll around")
    canvas.create_text(app.width//2,start+4*spacing,text="Step 2: Press '2' to be able to move left and right")
    canvas.create_text(app.width//2,start+5*spacing,text="Step 2: Press '3' to be able to move up and down")
    #current modes
    canvas.create_rectangle(app.width//2-120,start+7*spacing-10,app.width//2+120, start+10*spacing+10)
    canvas.create_text(app.width//2,start+7*spacing,text=f"Calibration Mode: %s" %("On" if app.currentlyCalibrating else "Off"),font='Arial 12 bold',fill=f"%s" %("green" if app.currentlyCalibrating else "black"))
    canvas.create_text(app.width//2,start+8*spacing,text=f"Clicking and Scrolling Mode: %s" %("On" if app.clickscrollingFeature else "Off"),font='Arial 12 bold',fill=f"%s" %("green" if app.clickscrollingFeature else "black"))
    canvas.create_text(app.width//2,start+9*spacing,text=f"Mouse Moving Mode (Left and Right): %s" %("On" if app.movingEyesFeature else "Off"),font='Arial 12 bold',fill=f"%s" %("green" if app.movingEyesFeature else "black"))
    canvas.create_text(app.width//2,start+10*spacing,text=f"Mouse Moving Mode (Up and Down): %s" %("On" if app.movingEyesFeatureUpandDown else "Off"),font='Arial 12 bold',fill=f"%s" %("green" if app.movingEyesFeatureUpandDown else "black"))

    canvas.create_text(app.width//2, start+functionstart*spacing, text="Functions",font='Arial 15 bold')
    functions="""closing left eye 2-4 sec is        left click
    closing right eye 2-4 sec is       right click
    closing left eye 4-7 sec is        up scroll
    closing right eye 4-7 sec is       down scroll
    closing both eye 7-10 sec is       disengage"""
    i=functionstart+2
    y=start+(functionstart+1)*spacing
    for line in functions.splitlines():
        canvas.create_text(app.width//2, y, text=line.strip())
        canvas.create_line(app.width//2-140,start+i*spacing-10,app.width//2+140, start+i*spacing-10)
        y+=spacing
        i+=1
        # closing both eyes 2-4 seconds      toggles mouse moving modes
    canvas.create_text(app.width//2+10, 650, text="closing both eyes 2-4 sec is      toggles mouse \n                                                     moving modes")
#CLICK AND SCROLL START *************************************************************
def clickandScroll(app):
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
#CLICK AND SCROLL END *************************************************************

#KEY PRESSED START *************************************************************
def keyPressed(app,event):
    if event.key=="2" and not app.movingEyesFeatureUpandDown: #left and right
        app.movingEyesFeature=not app.movingEyesFeature
        app.originalLeftEyecx=app.leftEye.cx
        app.originalLeftEyecy=app.leftEye.cx
        app.originalRightEyecx=app.rightEye.cx
        app.originalRightEyecy=app.rightEye.cy


    if event.key=="1": #clicks and scrolls
        app.originalLeftArea=app.leftPupil.area
        app.originalrightArea=app.rightPupil.area
        app.clickscrollingFeature= not app.clickscrollingFeature

    if event.key=="d": #calibration
        app.currentlyCalibrating=not app.currentlyCalibrating

    if event.key=="3" and not app.movingEyesFeature: #up and down
        app.movingEyesFeatureUpandDown= not app.movingEyesFeatureUpandDown
 
#KEY PRESSED END ***************************************************************


    

runApp(width=490, height=675)