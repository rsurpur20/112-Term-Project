import cv2
import numpy as np


def nothing(x):
    pass

cap = cv2.VideoCapture(0) # 0 represents which camera it is taking from

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("LH", "Trackbars", 0,180, nothing)
# cv2.createTrackbar("LS", "Trackbars", 0,255, nothing)
# cv2.createTrackbar("LV", "Trackbars", 0,255, nothing)
# cv2.createTrackbar("UP", "Trackbars", 180,180, nothing)
# cv2.createTrackbar("US", "Trackbars", 255,255, nothing)
# cv2.createTrackbar("UV", "Trackbars", 255,255, nothing)

while True:
    _, frame= cap.read()
    
    # returns a bool (True/False). 
    # If frame is read correctly, it will be True. 
    # So you can check end of the video by checking this return value
    leftFrame=frame[250:310,450:600]
    rightFrame=frame[250:310,600:750]
    eyeFrame = frame[250:310,450:750]
    # cv2.imshow('Video', eyeFrame)

    hsv=cv2.cvtColor(eyeFrame, cv2.COLOR_BGR2HSV)
    hsvLeft=cv2.cvtColor(leftFrame, cv2.COLOR_BGR2HSV)
    hsvRight=cv2.cvtColor(rightFrame, cv2.COLOR_BGR2HSV)
    #Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
    # LH=cv2.getTrackbarPos("LH","Trackbars")
    # LS=cv2.getTrackbarPos("LS","Trackbars")
    # LV=cv2.getTrackbarPos("LV","Trackbars")
    # UH=cv2.getTrackbarPos("UH","Trackbars")
    # US=cv2.getTrackbarPos("US","Trackbars")
    # UV=cv2.getTrackbarPos("UV","Trackbars")
    # (LH,LS,LV):
    #1,63,88
    #2,79,48
    lowerEye=np.array([2,79,48])
    higherEye=np.array([180,255,255])
    lowerPupil=np.array((0,0,74))
    higherPupil=np.array([180,255,255])
    thickness=2
    maskLeft = cv2.inRange(hsvLeft,lowerEye,higherEye)
    maskRight = cv2.inRange(hsvRight,lowerEye,higherEye)
    maskPupilLeft= cv2.inRange(hsvLeft,lowerPupil,higherPupil)
    maskPupilRight= cv2.inRange(hsvRight,lowerPupil,higherPupil)

    mask=cv2.inRange(hsv,lowerEye,higherEye)

    #help finetune
    kernel= np.ones((thickness,thickness), np.uint8)
    maskLeft=cv2.erode(maskLeft,kernel)
    maskRight=cv2.erode(maskRight,kernel)
    maskPupilLeft=cv2.erode(maskPupilLeft,kernel)
    maskPupilRight=cv2.erode(maskPupilRight,kernel)

    resize= cv2.resize(mask,(400,150),interpolation =cv2.INTER_AREA)

#contours!
    # cv2.findContours()
    contoursLeft, a = cv2.findContours(maskLeft, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursRight, b = cv2.findContours(maskRight, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursPupilLeft, c= cv2.findContours(maskPupilLeft, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursPupilRight, c= cv2.findContours(maskPupilRight, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#.06, 75`
    ratio=0.04
    areaMin=1000
    pupilAreaMin=400
    font= cv2.FONT_HERSHEY_COMPLEX_SMALL
    lastArea=0
    lastLeftPupilArea=0
    i=0
#LEFT---------------------------------------------------------------------------
    for cnt in contoursLeft:
        areaLeft = cv2.contourArea(cnt) #gets the area of each contour
        #ratio
        # ratio=0.02
        #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
        approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        #only draw area if pixels is greater than this num. this gets rid of noise
        # areaMin=9
        if areaLeft> areaMin:
        # frame, contour, ?, color, thickness
            cv2.drawContours(leftFrame, [approx], 0 ,(0,0,0), thickness)
            # if 3 <len(approx)<10:
                # location, font, thickness?, color
                # cv2.putText(leftFrame,f"{areaLeft}", (x,y),font,1,(0,0,0))
            #blink detection
            # if areaLeft<.3*lastArea:

            #     print(f"{i} Left Blink!")
                
            # lastAreaLeft=areaLeft
        #len(approx) <-- gives you the number of sides of the detected object

#RIGHT--------------------------------------------------------------------------
    for cnt in contoursRight:
        areaRight = cv2.contourArea(cnt) #gets the area of each contour
        #ratio
        # ratio=0.02
        #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
        approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        #only draw area if pixels is greater than this num. this gets rid of noise
        # areaMin=9
        if areaRight> areaMin:
        # frame, contour, ?, color, thickness
            cv2.drawContours(rightFrame, [approx], 0 ,(0,0,0), thickness)
            # if 3 <len(approx)<10:
                # location, font, thickness?, color
                # cv2.putText(rightFrame,"Right Eye", (x,y),font,1,(0,0,0))
        #len(approx) <-- gives you the number of sides of the detected object
#LEFT PUPIL--------------------------------------------------------------------------
    for cnt in contoursPupilLeft:
        areaPupil = cv2.contourArea(cnt) #gets the area of each contour
        #ratio
        # ratio=0.02
        #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
        approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        #only draw area if pixels is greater than this num. this gets rid of noise
        # areaMin=9
        if 1000> areaPupil> pupilAreaMin:
        # frame, contour, ?, color, thickness
            cv2.drawContours(leftFrame, [approx], 0 ,(255,0,0), thickness)
            # if 3 <len(approx)<10:
                # location, font, thickness?, color
            print(int(areaPupil))
            cv2.putText(leftFrame,f"{int(areaPupil)}", (x,y),font,1,(255,0,0))
        else:
            print("ELSEEEEE")
        if 1000>lastLeftPupilArea>pupilAreaMin and areaPupil<=10:
        #     i+=1
            print(f"Left Blink {int(areaPupil)} {int(lastLeftPupilArea)}")
        #len(approx) <-- gives you the number of sides of the detected object
        lastLeftPupilArea=areaPupil
#RIGHT PUPIL--------------------------------------------------------------------------
    for cnt in contoursPupilRight:
        areaPupil = cv2.contourArea(cnt) #gets the area of each contour
        #ratio
        # ratio=0.02
        #detecting shapes: (we use true to show that we are working with closed polygons) video had true true
        approx= cv2.approxPolyDP(cnt,ratio*cv2.arcLength(cnt, False),False)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        #only draw area if pixels is greater than this num. this gets rid of noise
        # areaMin=9
        if areaPupil> pupilAreaMin:
        # frame, contour, ?, color, thickness
            cv2.drawContours(rightFrame, [approx], 0 ,(255,0,0), thickness)
            if 3 <len(approx)<10:
                # location, font, thickness?, color
                cv2.putText(rightFrame,f"{areaPupil}", (x,y),font,1,(255,0,0))
        #len(approx) <-- gives you the number of sides of the detected object

    cv2.imshow("Frame",frame)
    cv2.imshow('Left', leftFrame)
    cv2.imshow('right', rightFrame)
    cv2.imshow('pupil', eyeFrame)
    cv2.imshow("Resize",resize)

    key=cv2.waitKey(1)
    #if it is too less, video will be very fast and if it is too high, 
    # video will be slow (Well, that is how you can display videos in slow motion).
    #  25 milliseconds will be OK in normal cases.
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()