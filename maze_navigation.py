#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
distance_8 = Distance(Ports.PORT8)
optical_7 = Optical(Ports.PORT7)
left_motors_motor_a = Motor(Ports.PORT6, False)
left_motors_motor_b = Motor(Ports.PORT10, False)
left_motors = MotorGroup(left_motors_motor_a, left_motors_motor_b)
right_motors_motor_a = Motor(Ports.PORT1, True)
right_motors_motor_b = Motor(Ports.PORT5, True)
right_motors = MotorGroup(right_motors_motor_a, right_motors_motor_b)
bumper_b = Bumper(brain.three_wire_port.b)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()


# Color to String Helper
def convert_color_to_string(col):
    if col == Color.RED:
        return "red"
    if col == Color.GREEN:
        return "green"
    if col == Color.BLUE:
        return "blue"
    if col == Color.WHITE:
        return "white"
    if col == Color.YELLOW:
        return "yellow"
    if col == Color.ORANGE:
        return "orange"
    if col == Color.PURPLE:
        return "purple"
    if col == Color.CYAN:
        return "cyan"
    if col == Color.BLACK:
        return "black"
    if col == Color.TRANSPARENT:
        return "transparent"
    return ""

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      Autonomous Maze Navigation
#	Description:  Reactive wall-following maze traversal for a VEX EXP robot
# 
# ------------------------------------------
# --- Tunable Constants ---
BASE_LEFT       = 50    # Base speed for left motor (PERCENT)
BASE_RIGHT      = 51
TARGET_DIST     = 3     # Target distance from followed wall in INCHES
STEP_SIZE       = 2     # Steering correction multiplier
LARGE_DIST      = 20    # Corner Turn Adjustment 
TURN_SPEED      = 100   # Speed during turns (PERCENT)
TURN_TIME       = 0.4   # Seconds to complete a 90-degree turn (tune this)
CORNER_TURN     = 12    # Threshold for when to invoke corner turn (Big Error)
LEFT_DOWN       = 40    # How Wide to make the turn 
CLOSE_WALL_BUFFER = 30


# --- Helper: Print to brain screen ---
def brain_print(output):
    brain.screen.set_cursor(1, 1)
    brain.screen.clear_row()
    brain.screen.print(output)

def brain_print_line(output, line):
    brain.screen.set_cursor(line, 1)
    brain.screen.clear_row()
    brain.screen.print(output)


# --- Helper: Turn in place using motor groups ---
def turn_left_90():
    left_motors.stop()
    right_motors.stop()
    wait(50, MSEC)
    left_motors.set_velocity(TURN_SPEED, PERCENT)
    right_motors.set_velocity(TURN_SPEED, PERCENT)
    left_motors.spin(REVERSE)
    right_motors.spin(FORWARD)
    wait(TURN_TIME, SECONDS)
    left_motors.stop()
    right_motors.stop()
    wait(100, MSEC)

def turn_right_90():
    left_motors.stop()
    right_motors.stop()
    wait(50, MSEC)
    left_motors.set_velocity(TURN_SPEED, PERCENT)
    right_motors.set_velocity(TURN_SPEED, PERCENT)
    left_motors.spin(FORWARD)
    right_motors.spin(REVERSE)
    wait(TURN_TIME, SECONDS)
    left_motors.stop()
    right_motors.stop()
    wait(100, MSEC)

def right_turn(angle):
    left_motors.set_stopping(BRAKE)
    right_motors.set_stopping(BRAKE)
    turn_times = TURN_TIME/90 # turn time for 90 / 90 degree 
    left_motors.stop()
    right_motors.stop()
    wait(50, MSEC)
    left_motors.set_velocity(TURN_SPEED, PERCENT)
    right_motors.set_velocity(TURN_SPEED, PERCENT)
    left_motors.spin(FORWARD)
    right_motors.spin(REVERSE)
    wait(turn_times * angle, SECONDS)
    left_motors.stop()
    right_motors.stop()
    wait(100, MSEC)

def left_turn(angle):
    left_motors.set_stopping(BRAKE)
    right_motors.set_stopping(BRAKE)
    turn_times = TURN_TIME/90 # turn time for 90 / 90 degree 
    left_motors.stop()
    right_motors.stop()
    wait(50, MSEC)
    left_motors.set_velocity(TURN_SPEED, PERCENT)
    right_motors.set_velocity(TURN_SPEED, PERCENT)
    left_motors.spin(REVERSE)
    right_motors.spin(FORWARD)
    wait(turn_times * angle, SECONDS)
    left_motors.stop()
    right_motors.stop()
    wait(100, MSEC)


# --- Active Wall Following: Drive forward with correction ---
def left_drive_with_correction():
    left_dist = distance_8.object_distance(INCHES)  # Left wall sensor
    left_velocity = 0
    right_velocity = 0
            

    if left_dist < CORNER_TURN :
        # Drive Along Wall
        error = left_dist - TARGET_DIST
        left_velocity  = BASE_LEFT
        right_velocity = BASE_RIGHT + (error * STEP_SIZE)

    else: 
        # Turn on Opening 
        error = (left_dist - TARGET_DIST) * LARGE_DIST
        left_velocity  = BASE_LEFT - LEFT_DOWN
        right_velocity = BASE_RIGHT + (error * STEP_SIZE)

    # Left motor stays at base, right motor corrects:
    # Too far from wall (positive error) → speed up right to arc left
    # Too close to wall (negative error) → slow down right to arc right

    if left_dist <= 1:
        left_velocity = left_velocity + CLOSE_WALL_BUFFER
        right_velocity = right_velocity - CLOSE_WALL_BUFFER

    left_motors.set_velocity(left_velocity, PERCENT)
    right_motors.set_velocity(right_velocity, PERCENT)
    left_motors.spin(FORWARD)
    right_motors.spin(FORWARD)

def right_drive_with_correction():
    right_dist = distance_8.object_distance(INCHES)  # Right wall sensor
    left_velocity = 0
    right_velocity = 0
            

    if right_dist < CORNER_TURN :
        # Drive Along Wall
        error = right_dist - TARGET_DIST
        left_velocity  = BASE_LEFT + (error * STEP_SIZE)
        right_velocity = BASE_RIGHT 
    else: 
        # Turn on Opening 
        error = (right_dist - TARGET_DIST) * LARGE_DIST
        left_velocity = BASE_LEFT + (error * STEP_SIZE)
        right_velocity = BASE_RIGHT - LEFT_DOWN

    # Right motor stays at base, left motor corrects:
    # Too far from wall (positive error) -> speed up left to arc right
    # Too close to wall (negative error) -> slow down left to arc left

    if right_dist <= 1:
        left_velocity = left_velocity - CLOSE_WALL_BUFFER
        right_velocity = right_velocity + CLOSE_WALL_BUFFER

    left_motors.set_velocity(left_velocity, PERCENT)
    right_motors.set_velocity(right_velocity, PERCENT)
    left_motors.spin(FORWARD)
    right_motors.spin(FORWARD)

# Main Loop
def left_solve_maze():
    
    while True:
        roll = brain_inertial.orientation(OrientationType.ROLL,DEGREES)
        # Print Metrics 
        brain_print(optical_7.is_near_object())
        brain_print_line(distance_8.object_distance(INCHES), 2)
        brain_print_line(roll,3)
        

        optical_7.set_light(LedStateType.ON)
        optical_7.set_light_power(100,PERCENT)

        left_motors.set_stopping(BRAKE)
        right_motors.set_stopping(BRAKE)


        if bumper_b.pressing():
            left_motors.set_velocity(25,PERCENT)
            right_motors.set_velocity(15,PERCENT)
            left_motors.spin(REVERSE)
            right_motors.spin(REVERSE)
            wait(1,SECONDS)
                

        # Wall in front 
        if optical_7.is_near_object():
            if distance_8.object_distance(INCHES) >= CORNER_TURN:
                left_drive_with_correction()
            else:
                left_motors.stop()
                right_motors.stop()
                wait(0.1, SECONDS)
                left_turn(90-brain_inertial.rotation(DEGREES))

        else:
            # Follow Wall
            left_drive_with_correction()

        wait(20, MSEC)

def right_solve_maze():
    
    while True:
        roll = brain_inertial.orientation(OrientationType.ROLL,DEGREES)
        # Print Metrics 
        brain_print(optical_7.is_near_object())
        brain_print_line(distance_8.object_distance(INCHES), 2)
        brain_print_line(roll,3)
        

        optical_7.set_light(LedStateType.ON)
        optical_7.set_light_power(100,PERCENT)

        left_motors.set_stopping(BRAKE)
        right_motors.set_stopping(BRAKE)


        if bumper_b.pressing():
            left_motors.set_velocity(15,PERCENT)
            right_motors.set_velocity(25,PERCENT)
            left_motors.spin(REVERSE)
            right_motors.spin(REVERSE)
            wait(1,SECONDS)
                

        # Wall in front 
        if optical_7.is_near_object():
            if distance_8.object_distance(INCHES) >= CORNER_TURN:
                right_drive_with_correction()
            else:
                left_motors.stop()
                right_motors.stop()
                wait(0.1, SECONDS)
                left_turn(90-brain_inertial.rotation(DEGREES))

        else:
            # Follow Wall
            right_drive_with_correction()

        wait(20, MSEC)

# left_solve_maze()
right_solve_maze()
# while True:
#     print(brain_inertial.orientation(OrientationType.ROLL,DEGREES))
#     wait(100,MSEC)
#     # while brain_inertial.orientation(OrientationType.ROLL,DEGREES) >= 3:
#         # brain_print("OVER THE WALL")
#         # left_motors.spin(REVERSE)
#         # right_motors.spin(REVERSE)
#     left_motors.stop()
#     right_motors.stop()