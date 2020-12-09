#################################################
# Term Project
#
# Your name: Roshni Surpur
# Your andrew id: rsurpur
################################################


1. A short description of the project's name and what it does. This may be taken from your design docs.
Mouseless: A program to control your computer with your eyes. You can left click with a left blink and right
click with a right blink. You can also move your eyes to scroll. You can calibrate so that any user can use this.

2. How to run the project. For example, which file the user should run in an editor. If your project uses data/source files, also describe how the user should set those up. Which libraries you're using that need to be installed, if any. If you can include the library in the submission, that is preferred.

in terminal locate the file "main.py" and run using "python3 main.py"

The fourdirections.py file contains the same project with a modification: there is only one mouse moving mode and you can move up, down, left, and right in that mode without a separation between the two. Due to the complexity of fine-tuning the up and down direction to work alongside left and right, I decide to make main.py which has two different mouse moving features: up and down, left and right. You can close your eyes for 2-4 seconds to toggle between these modes. 

Note: when you run it you might get errors like “TypeError: MouseMotionEvent() takes no arguments” and “TypeError: 'int' object is not callable.” Those can be disregarded because they come from doing illegal things (like sliding too fast or not clicking properly) in the trackbacks. This won’t hinder the running of the program and can be ignored

you will need pyautogui with "pip3 install pyautogui"  more info here: https://pyautogui.readthedocs.io/en/latest/install.html
you will also need opencv  "pip3 install opencv" more info here: https://pypi.org/project/opencv-python/
if you are on a mac, you need to allow camera access for vscode and terminal (system preferences --> security and privacy --> camera access --> check terminal and vscode) and (system preferences --> security and privacy --> automation --> check terminal and vscode). if vscode, isn't an option, then you're set. 
you need to import time library 
also the numpy library "pip3 install numpy" more info here: https://numpy.org/install/


3.A list of any shortcut commands that exist. Shortcut commands can be used to demonstrate specific features by skipping forward in a game or loading sample data. They're useful for when you're testing your code too!

How to use this program:
main.py:
closing left eye 2-4 sec is left click
closing right eye 2-4 sec is right click
closing left eye 4-7 sec is up scroll
closing right eye 4-7 sec is down scroll
closing both eye 7-10 sec is disengage
Closing both eyes 2-4 seconds toggles between up/down and right/left modes

fourdirections.py:
closing left eye 2-4 sec is left click
closing right eye 2-4 sec is right click
closing left eye 4-7 sec is up scroll
closing right eye 4-7 sec is down scroll
closing both eye 7-10 sec is disengage

4. bibliography:
heavily inspiried by Jaime Romero's Winking Mouse project https://www.youtube.com/watch?v=roLX33rS0B0&feature=youtu.be 
https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/ <-- referenced to figure out opencv and contours
https://pyautogui.readthedocs.io/en/latest/ <-- referenced for pyautogui methods 
https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/ <-- helpful to get center of contour 
https://stackoverflow.com/questions/22399257/finding-the-center-of-a-contour-using-opencv-and-visual-c <-- helpful to get center of contour
https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html <-- helpful to get center of contour 