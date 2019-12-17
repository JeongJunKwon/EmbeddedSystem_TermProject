import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
pin17 = 17
pin18 = 18

lur = AnalogIn(ads, ADS.P0)
lul = AnalogIn(ads, ADS.P1)
ldr = AnalogIn(ads, ADS.P2)
ldl = AnalogIn(ads, ADS.P3)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin17, GPIO.OUT)
GPIO.setup(pin18, GPIO.OUT)

servoh = GPIO.PWM(pin17, 50)
servov = GPIO.PWM(pin18, 50)

moveHorizontal = 7.5
moveVertical = 7.5

servoh.start(0)
servov.start(0)

servoh.ChangeDutyCycle(moveHorizontal)
servov.ChangeDutyCycle(moveVertical)

try:
    while True:
        up = (lur.value + lul.value) / 2
        down = (ldr.value + ldl.value) / 2
        right = (lur.value + ldr.value) / 2
        left = (lul.value + ldl.value) / 2

        print("up: ", up, end= " ")
        print("down: ", down)
        print("right: ", right, end = " ")
        print("left: ", left)

        if right < left:
            servoh.ChangeDutyCycle(moveHorizontal)
            if moveHorizontal < 12.5:
                moveHorizontal += 0.1
        else:
            servoh.ChangeDutyCycle(moveHorizontal)
            if moveHorizontal > 2.5:
                moveHorizontal -= 0.1

        if down < up:
            servov.ChangeDutyCycle(moveVertical)
            if moveVertical < 12.5:
                moveVertical += 0.1
        else:
            servov.ChangeDutyCycle(moveVertical)
            if moveVertical > 2.5:
                moveVertical -= 0.1
        time.sleep(0.1)   
except KeyboardInterrupt:
    servoh.stop()
    servov.stop()

GPIO.cleanup() 