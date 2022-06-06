# Python code for Multiple Color Detection 
  
import numpy as np 
import cv2 
import pypot.dynamixel
import time
import RPi.GPIO as GPIO
import signal, sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

 #suiveur de ligne devant
lineLeft=26
lineRight=1 #Pin non definie encore

kicker=23

GPIO.setup(kicker, GPIO.OUT)
GPIO.setup(lineLeft, GPIO.IN)
GPIO.setup(lineRight, GPIO.IN)

start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0  
    
# Capturing video through webcam 
webcam = cv2.VideoCapture(0) 

frame_width = int(webcam.get(3)) 
frame_height = int(webcam.get(4))
size = (frame_width, frame_height)
print(size)
#Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
#initialisation





areaProche=1000 #Seuil d'aire de detection ou l'on decide de renvoyer la balle car elle est suffisament proche
areaBalle=500 #Seuil de detection ou l'on decide qu'ue balle est presente

# ports=pypot.dynamixel.get_available_ports()
# baud=[57142, 1000000]
# 
# print("Detction des ports")
# for p in ports:
#     for b in baud:
#         with pypot.dynamixel.DxlIO(p, b) as dxl:
#             print('opened port {} with baudrate {} and detected motor ids: {}'.format(p, b, dxl.scan(range(10))))
#             
# dxl_io = pypot.dynamixel.DxlIO(ports[0])
# dxl_io.set_wheel_mode([1])
# dxl_io.set_wheel_mode([2])
# dxl_io.set_wheel_mode([3])
# dxl_io.set_wheel_mode([4])


#moteur
def stop():
    #     dxl_io.set_moving_speed({1 : power})
#     dxl_io.set_moving_speed({2 : -power})
#     dxl_io.set_moving_speed({3 : -power})
#     dxl_io.set_moving_speed({4 : power})
    pass
    
def left(timeDep=0.5, power=500): #Temps de deplacement et vitesse des moteurs
        print('Left')
#     dxl_io.set_moving_speed({1 : power})
#     dxl_io.set_moving_speed({2 : -power})
#     dxl_io.set_moving_speed({3 : -power})
#     dxl_io.set_moving_speed({4 : power})
        time.sleep(timeDep)
        stop()

def right(timeDep=0.5, power=500):
        print('Right')
#     dxl_io.set_moving_speed({1 : -power})
#     dxl_io.set_moving_speed({2 : power})
#     dxl_io.set_moving_speed({3 : power})
#     dxl_io.set_moving_speed({4 : -power})
        time.sleep(timeDep)
        stop()

        
def top(timeDep=0.5, power=500):

        print('Top')
#     dxl_io.set_moving_speed({1 : power})
#     dxl_io.set_moving_speed({2 : power})
#     dxl_io.set_moving_speed({3 : -power})
#     dxl_io.set_moving_speed({4 : -power})
        time.sleep(timeDep)
        stop()
    
def bottom(timeDep=0.5, power=500):
        print('Bottom')
#     dxl_io.set_moving_speed({1 : -power})
#     dxl_io.set_moving_speed({2 : -power})
#     dxl_io.set_moving_speed({3 : power})
#     dxl_io.set_moving_speed({4 : power})
        time.sleep(timeDep)
        stop()

def kick():
    print("Kick")
    GPIO.output(kicker)
    
def ligneCheck():        
    if not GPIO.input(lineLeft):
        right()
    if not GPIO.input(lineRight):
        left()


GPIO.add_event_detect(lineLeft, GPIO.FALLING, callback=right, bouncetime=100) #Si LineLeft active on execute la fonction right avec temps de delai de 100ms si lineLeft est detecte en continuellement
    
# Start a while loop 
while True: 
      
    # Reading the video from the 
    # webcam in image frames 
    _, imageFrame = webcam.read() 
  
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 
  
    # Set range for red color and  
    # define mask 
#     red_lower = np.array([20, 140, 220], np.uint8) 
#     red_upper = np.array([235, 235, 235], np.uint8)
    red_lower = np.array([0,125, 0], np.uint8) 
    red_upper = np.array([50, 255, 125], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

      
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernal = np.ones((5, 5), "uint8") 
      
    # For red color 
    red_mask = cv2.dilate(red_mask, kernal) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                              mask = red_mask) 
      

    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
    areaMax=0 
    for pic, contour in enumerate(contours): #On prend le plus gros contour de tous les contours
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        if area>areaMax:
            areaMax=area
        imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                    (x + w, y + h),  
                                    (0, 128, 255), 2) 
              
        cv2.putText(imageFrame, "Red Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                 (0, 0, 255)) 
       
        
    ligneCheck()
    if areaMax>areaBalle:        
        
        if x <= 320:
            left()
        else:
            right()
        if(areaMax > areaProche):
            top()
            kick()
            bottom() 
    
    # Program Termination
    #result.write(imageFrame) 
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    counter+=1
#     if (time.time() - start_time) > x :
#         print("FPS: ", counter / (time.time() - start_time))
#         counter = 0
#         start_time = time.time()
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        webcam.release() 
        result.release() 
        #cap.release()
        cv2.destroyAllWindows() 
        break
    


