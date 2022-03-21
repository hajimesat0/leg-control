#! /usr/bin/env python

import time
import Adafruit_PCA9685


class ServoMotor:
    def __init__( self, pwm, channel, step_for_0deg, step_for_180deg ):
        self.__pwm = pwm
        self.__channel = channel
        self.__min_step = step_for_0deg
        self.__max_step = step_for_180deg
        self.__angle_to_step = ( step_for_180deg - step_for_0deg ) / 180.0
        # print( self.__angle_to_step )

    
    def set_angle_deg( self, angle_deg ):
        if ( angle_deg < 0 ) or ( 180 < angle_deg ):
            return False
        step = angle_deg * self.__angle_to_step + self.__min_step
        # print( step )
        self.__pwm.set_pwm(self.__channel,0,int(step))
        return True




if __name__ == '__main__':
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq( 60 )
    servo01 = ServoMotor( pwm, 0, 120, 602 )
    servo02 = ServoMotor( pwm, 1, 120, 602 )

    while True:
        angle = input()
        print( 'angle is ' + str(angle) )
        servo01.set_angle_deg( angle )
        servo02.set_angle_deg( angle )


# while True:
#     step = input()
#     print( 'step is ' + str(step) )
#     for i in range(8):
#         pwm.set_pwm(i,0,step)
#         # pwm.set_pwm(i+8,0,step)

# while True:
#     pwm.set_pwm(15,0,150)
#     time.sleep(wait_time)
#     pwm.set_pwm(15,0,500)
#     time.sleep(wait_time)
#     print( '!' )
