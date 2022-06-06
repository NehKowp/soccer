# Python code for Multiple Color Detection 
  
import numpy as np 
import cv2 
import pypot.dynamixel
import time


start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0  
    
# Capturing video through webcam 
webcam = cv2.VideoCapture(0) 

frame_width = int(webcam.get(3)) 
frame_height = int(webcam.get(4))
size = (frame_width, frame_height)
#Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
#initialisation







ports=pypot.dynamixel.get_available_ports()
baud=[57142, 1000000]

print("Detction des ports")
for p in ports:
    for b in baud:
        with pypot.dynamixel.DxlIO(p, b) as dxl:
            print('opened port {} with baudrate {} and detected motor ids: {}'.format(p, b, dxl.scan(range(10))))
            
dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])
dxl_io.set_wheel_mode([2])
dxl_io.set_wheel_mode([3])
dxl_io.set_wheel_mode([4])


#moteur
def left():
    print('Left')
    dxl_io.set_moving_speed({1 : 500})
    dxl_io.set_moving_speed({2 : -500})
    dxl_io.set_moving_speed({3 : -500})
    dxl_io.set_moving_speed({4 : 500})
    time.sleep(0.5)

def right():
    print('Right')
    dxl_io.set_moving_speed({1 : -500})
    dxl_io.set_moving_speed({2 : 500})
    dxl_io.set_moving_speed({3 : 500})
    dxl_io.set_moving_speed({4 : -500})
    time.sleep(0.5)

        
def top():
    print('Top')
    dxl_io.set_moving_speed({1 : 500})
    dxl_io.set_moving_speed({2 : 500})
    dxl_io.set_moving_speed({3 : -500})
    dxl_io.set_moving_speed({4 : -500})
    time.sleep(0.5)

        
    
    
# Start a while loop 
while(1): 
      
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
    red_lower = np.array([150, 0, 0], np.uint8) 
    red_upper = np.array([200, 75, 255], np.uint8) 
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
      
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour)
        print(area)
        if(area > 500):
            x, y, w, h = cv2.boundingRect(contour)
#             print(x)
#             if x <= 210:
#                 left()
#             else:
#                 right()


            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                       (x + w, y + h),  
                                       (0, 128, 255), 2) 
              
            cv2.putText(imageFrame, "Red Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                 (0, 0, 255))     
    
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
    

