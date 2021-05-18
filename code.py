# this is designed to run on an adafruit QT Py board running Circuit Python 6.1.0
# using a VL53L0X ToF sensor and a DRV8833 motor driver.

import board
import time
import busio
import adafruit_vl53l0x
import pwmio
import touchio
from adafruit_debouncer import Debouncer
from adafruit_motor import motor

# set up PWM pins for left motor
PWM_PIN_A = board.D7
PWM_PIN_B = board.D8

# set up PWM pins for right motor
PWM_PIN_C = board.D9
PWM_PIN_D = board.D10

# set up left motor
pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=50)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=50)
leftmotor = motor.DCMotor(pwm_a, pwm_b)

# set up right motor
pwm_c = pwmio.PWMOut(PWM_PIN_C, frequency=50)
pwm_d = pwmio.PWMOut(PWM_PIN_D, frequency=50)
rightmotor = motor.DCMotor(pwm_c, pwm_d)

# initialize i2c and time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tof = adafruit_vl53l0x.VL53L0X(i2c)

# setup touch input
touch = touchio.TouchIn(board.D6)
touch_debounced = Debouncer(touch)

# set up turn and drive parameters
start_turn_distance = 100
stop_turn_distance = 150
turn_time = 2
abort_turn_time = 5
start_turn_time = -1
turn_flag = False
run_flag = False

# set up stuck decetion
stuck_iterator = 0
stuck_counter = 0
stuck_range = tof.range
stuck_variance = 5
stuck_flag = False

while True:
    now = time.monotonic()
    # print(tof.range)

    # invert run value when touched
    touch_debounced.update()
    if touch_debounced.rose:
        run_flag = ~run_flag

    # if stuck, stop driving and reset stuck flag
    if stuck_flag:
        run_flag = False
        stuck_flag = False

    # if run_flag is true, then drive
    if run_flag:
        # detect when stuck and set stuck_flag to True
        stuck_iterator += 1
        if stuck_iterator >= 50:
            stuck_iterator = 0
            stuck_range = tof.range
            print(stuck_range)
            print(stuck_counter)
        if stuck_iterator == 49:
            if tof.range <= stuck_range + stuck_variance or tof.range >= stuck_range - stuck_variance:
                stuck_counter += 1
                print("TOF range:", tof.range)
                print("stuck_range: ", stuck_range)
                # print(stuck_counter)
                # print(stuck_flag)
        if stuck_counter >= 5:
            stuck_flag = True
            stuck_counter = 0

        # when start_turn_distance or less from an obstacle, start turning right
        if tof.range <= start_turn_distance:
            turn_flag = True
        if turn_flag:

            # stop driving if attempting to turn for more than abort_turn_time
            if now > abort_turn_time + start_turn_time:
                run_flag = False

            #turn right for turn_time or until stop_turn_distance or more from an obstacle
            elif tof.range < stop_turn_distance or now <= start_turn_time + turn_time:
                # now = time.monotonic()
                leftmotor.throttle = 0.5
                rightmotor.throttle = -0.5

            else:
                turn_flag = False

        # drive straight forward when greater than start_turn_distance from an obstacle
        else:
            leftmotor.throttle = 0.5
            rightmotor.throttle = 0.5
            start_turn_time = now

    # if run is false, shut off motors and set turn_flag and stuck_flag to False
    else:
        leftmotor.throttle = 0
        rightmotor.throttle = 0
        turn_flag = False
        stuck_flag = False
