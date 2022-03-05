#! /usr/bin/env python

import time
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(50)

wait_time = 0.1
angle = 150


while True:
    if 150 < angle:
        angle = 150
    else:
        angle = 500
    print( angle )
    for i in range(8):
        pwm.set_pwm(i+8,0,angle)
        time.sleep(wait_time)

# while True:
#     pwm.set_pwm(15,0,150)
#     time.sleep(wait_time)
#     pwm.set_pwm(15,0,500)
#     time.sleep(wait_time)
#     print( '!' )
