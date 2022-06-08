import sensor, time, image, math,pyb
from pyb import UART
import pyb
from machine import Pin
sensor.reset()
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.RGB565)
sensor.skip_frames(time = 2000)
def detect():
    return 0

def robot(x):
    thresholds = [(9 , 100 , -128,124,17,124),(69, 81, -34, -13, -18, -12)]
    led[x].on()
    img = sensor.snapshot()
    img.draw_cross(img.width()//2, img.height()//2 , size = 10, thickness = 2)
    #img.draw_cross(160, img.height()//2 , size = 10, thickness = 2)
    for blob in img.find_blobs([thresholds[x]], pixels_threshold=200, area_threshold=200, merge=True):
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        pos = (blob.cx() - img.width()//2, blob.cy() - img.height()//2)
        return pos
level = 0
led = [pyb.LED(1),pyb.LED(2)]
pinL = Pin("P0", Pin.OUT_PP)
pinR = Pin("P1", Pin.OUT_PP)
pinT = Pin("P2", Pin.OUT_PP)
pinB = Pin("P3", Pin.OUT_PP)

while True:
    level = detect()
    pos = robot(level)
    pinL.value(0)
    pinR.value(0)
    pinT.value(0)
    pinB.value(0)

    if pos :
        print(pos)
        if pos[0] <-5:
            print("left")
            pinL.value(1)
            pinR.value(0)
            pinT.value(0)
            pinB.value(0)

        elif pos[0] >5:
            print("Right")
            pinL.value(0)
            pinR.value(1)
            pinT.value(0)
            pinB.value(0)
        elif pos[1]<0:
            print("Top")
            pinL.value(0)
            pinR.value(0)
            pinT.value(1)
            pinB.value(0)
        else:
          print("Bottom")
          pinL.value(0)
          pinR.value(0)
          pinT.value(1)
          pinB.value(0)





        """ if pos[1]<0:

            else:
                print("Bottom right")
                pinBl.value(0)
                pinBr.value(1)
                pinTl.value(0)
                pinTr.value(0)
                pinB.value(0)
                pinT.value(0)
        if pos[0]==0 :
            if pos[1] < 0:
                pinBl.value(0)
                pinBr.value(0)
                pinTl.value(0)
                pinTr.value(0)
                pinB.value(1)
                pinT.value(0)
            else:
                pinBl.value(0)
                pinBr.value(0)
                pinTl.value(0)
                pinTr.value(0)
                pinB.value(0)
                pinT.value(1)"""
