#! /usr/bin/env python

import time
import math
import Adafruit_PCA9685


class ServoMotor:
    def __init__( self, pwm, channel, step_for_0deg, step_for_180deg ):
        self.__pwm = pwm
        self.__channel = channel
        self.__min_step = step_for_0deg
        self.__max_step = step_for_180deg
        self.__angle_to_step = ( step_for_180deg - step_for_0deg ) / 180.0
        self.__angle_deg_min = 0
        self.__angle_deg_max = 180
        # print( self.__angle_to_step )

    
    def set_angle_deg( self, angle_deg ):
        if ( angle_deg < self.__angle_deg_min ) or ( self.__angle_deg_max < angle_deg ):
            print('ServoMotor error: target angle is out of range')
            return False
        step = angle_deg * self.__angle_to_step + self.__min_step
        # print( step )
        self.__pwm.set_pwm(self.__channel,0,int(step))
        return True

    def set_angle_limit_deg( self, angle_deg_min, angle_deg_max ):
        if ( angle_deg_min < 0 ) or ( 180 < angle_deg_min ):
            print('ServoMotor error: limit_min angle is out of range')
            return False
        if ( angle_deg_max < 0 ) or ( 180 < angle_deg_max ):
            print('ServoMotor error: limit_max angle is out of range')
            return False
        if ( angle_deg_max <= angle_deg_min ):
            print('ServoMotor error: limit_max <= limit_min')
            return False
        self.__angle_deg_min = angle_deg_min
        self.__angle_deg_max = angle_deg_max

class Leg:
    def __init__( self, servo_motor_inside, servo_motor_outside, length_thigh, length_shin ):
        self.__servo_motor_inside = servo_motor_inside
        self.__servo_motor_outside = servo_motor_outside
        self.__length_thigh = length_thigh
        self.__length_shin = length_shin
        self.__length_coeff_sqrt = math.sqrt(length_thigh**2+length_shin**2)
    
    def set_pose( self, angle, length ):
        if ( ( length < ( self.__length_shin - self.__length_thigh ) ) or ( ( self.__length_shin + self.__length_thigh ) < length ) ):
            print('Leg error: length is out of range')
            return False
        cos_val = ( length**2 + self.__length_thigh**2 - self.__length_shin**2 ) / ( 2 * length * self.__length_thigh )
        # print( 'cos='+str(cos_val) )
        angle_thigh = 2 * math.acos( cos_val )
        angle_inside = -( angle - math.degrees(angle_thigh/2) )
        angle_outside = angle + math.degrees(angle_thigh/2)
        print('inside = ' + str(angle_inside) + '[deg]')
        print('outside = ' + str(angle_outside) + '[deg]')
        self.__servo_motor_inside.set_angle_deg(angle_inside)
        self.__servo_motor_outside.set_angle_deg(angle_outside)
        return True


if __name__ == '__main__':
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq( 60 )
    servo01 = ServoMotor( pwm, 0, 120, 602 )
    servo01.set_angle_limit_deg( 30, 150 )
    servo02 = ServoMotor( pwm, 1, 120, 602 )
    servo02.set_angle_limit_deg( 30, 150 )
    leg_front_left = Leg( servo01, servo02, 21.58, 40 )

    while True:
        angle = input('angle = ')
        length = input('length = ')
        leg_front_left.set_pose( angle, length )
        # servo01.set_angle_deg( angle )
        # servo02.set_angle_deg( angle )


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
