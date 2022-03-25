#! /usr/bin/env python

import time
import math
import signal
import threading
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

def signal_interrupt(arg1,arg2):
    event.set()

def thread_handler(event):
    while True:
        event.wait()
        event.clear()
        # print( time.time() )

if __name__ == '__main__':
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq( 60 )
    motor = []
    for i in range(8):
        servo_motor = ServoMotor( pwm, i, 120, 602 )
        servo_motor.set_angle_limit_deg( 30,150 )
        motor.append( servo_motor )
    leg = []
    for i in range(4):
        n = 2 * i
        leg.append( Leg( motor[n], motor[n+1], 21.58, 40 ) )

    global event
    event = threading.Event()
    thread = threading.Thread( target=thread_handler, args=(event,))
    thread.start()


    signal.signal( signal.SIGALRM, signal_interrupt )
    signal.setitimer( signal.ITIMER_REAL, 1, 0.05)

    while True:
        command_str = raw_input('>> ')
        splited_command_str = command_str.split()
        # print( command_str.split() )
        exec_command = False
        if 0<len(splited_command_str):
            if splited_command_str[0]=='test':
                print( 'test[' + command_str +']' )
                exec_command = True
            elif splited_command_str[0]=='motor' :
                axis_no = int(splited_command_str[1])
                axis_angle = int(splited_command_str[2])
                if 0<=axis_no and axis_no<8 :
                    motor[axis_no].set_angle_deg(axis_angle)
                exec_command = True
        if exec_command==False:
            print('nothing to do for ['+command_str+']')

        # time.sleep(100)

    # while True:
    #     command = input('command ( stop, pushup, walk ) = ')

    #     length = input('length = ')
    #     leg_front_left.set_pose( angle, length )
        # servo01.set_angle_deg( angle )
        # servo02.set_angle_deg( angle )


    # while True:
    #     angle = input('angle = ')
    #     length = input('length = ')
    #     leg_front_left.set_pose( angle, length )
    #     # servo01.set_angle_deg( angle )
    #     # servo02.set_angle_deg( angle )
