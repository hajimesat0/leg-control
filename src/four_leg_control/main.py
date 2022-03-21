#! /usr/bin/env python

import time
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)

wait_time = 0.1
angle = 150


while True:
    step = input()
    print( 'step is ' + str(step) )
    for i in range(8):
        pwm.set_pwm(i,0,step)
        # pwm.set_pwm(i+8,0,step)

# while True:
#     pwm.set_pwm(15,0,150)
#     time.sleep(wait_time)
#     pwm.set_pwm(15,0,500)
#     time.sleep(wait_time)
#     print( '!' )
