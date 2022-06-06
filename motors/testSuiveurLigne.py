import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lineFront=26 #suiveur de ligne devant
lineLeft=1
lineRight=1

GPIO.setup(lineFront, GPIO.IN)
GPIO.setup(lineLeft, GPIO.IN)
GPIO.setup(lineRight, GPIO.IN)
while True:
    print(GPIO.input(lineFront))