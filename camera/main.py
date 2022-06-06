#import RPi.GPIO as GPIO
import time
import  pypot.dynamixel
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

'''pinRight=26
pinLeft=19
pinBottom=13
pinTop=6
GPIO.setup(pinRight, GPIO.IN)
GPIO.setup(pinLeft, GPIO.IN)
GPIO.setup(pinTop, GPIO.IN)
GPIO.setup(pinBottom, GPIO.IN)'''
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

while True:
    if GPIO.input(pinRight):
        print('Right')
        dxl_io.set_moving_speed({1 : -500})
        dxl_io.set_moving_speed({2 : 500})
        dxl_io.set_moving_speed({3 : 500})
        dxl_io.set_moving_speed({4 : -500})
        
    elif GPIO.input(pinLeft):
        print('Left')
        dxl_io.set_moving_speed({1 : 500})
        dxl_io.set_moving_speed({2 : -500})
        dxl_io.set_moving_speed({3 : -500})
        dxl_io.set_moving_speed({4 : 500})
    
    elif GPIO.input(pinTop):
        print('')
        dxl_io.set_moving_speed({1 : 500})
        dxl_io.set_moving_speed({2 : 500})
        dxl_io.set_moving_speed({3 : -500})
        dxl_io.set_moving_speed({4 : -500})
        
    elif GPIO.input(pinBottom):
        print('Bottom')
        dxl_io.set_moving_speed({1 : -500})
        dxl_io.set_moving_speed({2 : -500})
        dxl_io.set_moving_speed({3 : 500})
        dxl_io.set_moving_speed({4 : 500})
    
    else:
        print("Rien")
        dxl_io.set_moving_speed({1 : 0})
        dxl_io.set_moving_speed({2 : 0})
        dxl_io.set_moving_speed({3 : 0})
        dxl_io.set_moving_speed({4 : 0})
                  