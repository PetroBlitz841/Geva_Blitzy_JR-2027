from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task


hub = PrimeHub(top_side=-Axis.X, front_side=Axis.Z) 

# Color sensors
floor_color_sensor = ColorSensor(Port.D)
arm_color_sensor = ColorSensor(Port.C)
# Arms
arm_right = Motor(Port.E)
arm_left = Motor(Port.A)
# Wheels
wheel_left = Motor(Port.F, Direction.COUNTERCLOCKWISE)
wheel_right = Motor(Port.B)

chassis = DriveBase(wheel_left, wheel_right, 62.4, 97.5)

# reflection color
WHITE = Color(h=10, s=0, v=100)
RED = Color(h=354, s=89, v=59)
BLUE = Color(h=216, s=92, v=55)
GREEN = Color(h=156, s=79, v=38)
YELLOW = Color(h=40, s=70, v=94)
BLACK = Color(h=210, s=26, v=14)
MAGENTA = Color(h=338, s=83, v=31)
NO_COLOR = Color(h=200, s=78, v=5)

arm_color_sensor.detectable_colors(
    [
        WHITE,
        RED,
        BLUE,
        GREEN,
        YELLOW,
        BLACK,
        MAGENTA,
        NO_COLOR
    ]
)

def drive_settings(straight_speed=500, straight_acceleration=300, turn_rate=300, turn_acceleration=100):
    """resets to the default speed, acceleration and turn rate"""
    chassis.settings(
        straight_speed=straight_speed,
        straight_acceleration=straight_acceleration,
        turn_rate=turn_rate,
        turn_acceleration=turn_acceleration,
    )

def reset(gyro=0):
    """resets the gyro and drive settings to default values"""
    chassis.use_gyro(False)
    hub.imu.reset_heading(gyro)
    drive_settings()
    chassis.use_gyro(True)

def check_battery_percent():
    v = hub.battery.voltage()  # Read battery voltage (mV)
    percent = int((v - 7000) * 100 // 1200)  # Convert voltage to percentage
    return percent

def wheels_cleaning():
    chassis.use_gyro(False)
    chassis.drive(speed=1000, turn_rate=0)
    while True:
        hub.display.number(check_battery_percent())
        wait(500)

def drive_untill_black(speed=100, turn_rate=0):
    chassis.drive(speed, turn_rate)
    while floor_color_sensor.reflection() > 10:
        print(floor_color_sensor.reflection())
    chassis.stop()

def hsv_check(sensor):
    while True:
        hsv = sensor.hsv()
        print(hsv)

def turn_to(angle):
    start_angle = (hub.imu.heading() + 360) % 360
    deg_to_turn = (angle - start_angle) % 360
    if deg_to_turn >= 180:
        chassis.turn(deg_to_turn - 360)
    else:
        chassis.turn(deg_to_turn)


def black_run():
    #settings
    reset(gyro=90)
    arm_left.run_time(speed=-900, time=1000,wait=False) # Reset the  arm
    arm_right.run_time(speed=900, time=1000) # Reset the arm
    arm_left.run_time(speed=-500, time=1000, wait=False) # Reset the  arm 3
    arm_right.run_time(speed=500, time=1000, wait=False)
    chassis.use_gyro(True) # use PID for the wall following
    #pushing the drone
    chassis.straight(790)
    #puttind the red thingy in the other thingy
    chassis.turn(-60) 
    wheel_right.run_angle(speed=800, rotation_angle=230)
    wheel_right.run_angle(speed=1000, rotation_angle=-30)
    wheel_right.run_angle(speed=1000, rotation_angle=30)
    #going to the base
    wheel_right.run_angle(speed=800, rotation_angle=-115 ) 
    turn_to(90) 
    chassis.straight(-780) 
    turn_to(45) 
    #going to mission 2
    arm_left.run_time(speed=700, time=1000,wait=False) # putting down the cage
    arm_right.run_time(speed=-700, time=1000,wait=False) #putting down the cage2
    chassis.straight(550) 
    #doing the mission
    chassis.straight(-15) 
    arm_left.run_angle(speed=-1000, rotation_angle=1400, wait=False) # picking up the cage and seed
    arm_right.run_angle(speed=1000, rotation_angle=1400, wait=False) #picking up the cage2 and seed
    #going home
    wait(1000)
    chassis.settings(400) 
    chassis.straight(-500) 
    


    
def white_run():
    while True:
        reset()
        drive_settings(straight_speed=1000)
        chassis.straight(300, then=Stop.NONE)
        chassis.curve(radius=300, angle=180)
        chassis.curve(radius=150, angle=-140)
        chassis.straight(200, then=Stop.NONE)
        chassis.curve(radius=250, angle=230)

        chassis.straight(100, then=Stop.NONE)
        chassis.curve(radius=100, angle=30, then=Stop.NONE)

        chassis.straight(100 ,then=Stop.NONE)

        chassis.curve(radius=100, angle=-30, then=Stop.NONE)
        chassis.straight(50 ,then=Stop.NONE)

        chassis.curve(radius=100, angle=-30)
        drive_untill_black()

        chassis.curve(radius=100, angle=30, then=Stop.NONE)

        chassis.straight(330, then=Stop.NONE)
        chassis.curve(radius=300, angle=-90)
        chassis.straight(-650)


def green_run():
    #settings & going to the first mission
    chassis.use_gyro(True)
    chassis.settings(straight_speed=300, straight_acceleration=100)
    arm_left.run_time(speed=900, time=1000,wait=False)
    chassis.straight(830)
    arm_left.run_time(speed=-220, time=750,wait=False)
    # doint the leaves
    chassis.straight(100)
    arm_left.run_time(speed=220, time=750)
    chassis.settings(straight_speed=100)
    chassis.straight(40,wait=False)
    #doint the coopp mission
    arm_right.run_angle(speed=700, rotation_angle=25)
    chassis.straight(50)
    arm_right.run_time(speed=600, time=1000)
    chassis.settings(straight_speed=500, straight_acceleration=170)
    chassis.straight(-90)
    #going home
    chassis.settings(straight_speed=600, straight_acceleration=600)
    chassis.straight(-1000)

def blue_run():
    #settings
    arm_right.run_time(speed=900, time=1000, wait=False)
    chassis.use_gyro(True) # use PID for the wall following
    #going to the first mission
    chassis.straight(450)
    chassis.turn(-25)
    chassis.straight(240)
    chassis.turn(23)
    chassis.straight(195)
    #doing fungus mission
    chassis.straight(-7)
    arm_right.run_time(speed=-1000, time=1000, wait=False)
    chassis.straight(1100, wait=False)
    #doing the ant& leaves mission
    arm_left.run_angle(speed=-1000, rotation_angle=2750)
    wheel_right.run_angle(speed=-400, rotation_angle=200)
    wheel_left.run_angle(speed=400, rotation_angle=-50)
    #pushing down the box
    chassis.settings(straight_speed=700, straight_acceleration=700)
    chassis.straight(-110)
    chassis.turn(-60)
    chassis.curve(radius=-547, angle=-35,then=Stop.NONE)
    chassis.curve(radius=-270, angle=80)


def yellow_run():
    #settings
    chassis.use_gyro(True) # use PID for the wall following
    hub.imu.reset_heading(0)
    chassis.settings(straight_speed= 200, straight_acceleration=200)
    arm_left.run_time(speed=-900, time=1000,wait=False)
    #driving
    chassis.straight(610)
    chassis.turn(32, absolute=True)
    chassis.straight(-75)
    arm_left.run_time(speed=900, time=1000)
    chassis.settings(straight_speed= 400, straight_acceleration=400)
    chassis.straight(100)
    chassis.straight(-50)
    chassis.turn(32, absolute=True)
    chassis.straight(100)
    chassis.turn(30, absolute=True)
    chassis.straight(-75)
    chassis.turn(30, absolute=True)
    arm_left.run_time(speed=-900, time=1000)
    chassis.straight(100)
    arm_left.run_time(speed=200, time=1000)
    chassis.straight(100, wait=False)
    arm_left.run_time(speed=-100, time=2000)
    chassis.straight(50, wait=False)
    chassis.settings(straight_speed= 600, straight_acceleration=600)
    chassis.straight(220)
    chassis.turn(75, absolute=True)
    chassis.straight(100)
    arm_left.run_time(speed=700, time=2000)
    chassis.straight(-120)
    arm_left.run_time(speed=-100, time=1300)
    #chassis.curve(radius=200, angle=45)
    chassis.straight(150, then=Stop.NONE)
    wheel_right.run_angle(speed=800, rotation_angle=150, then=Stop.NONE)
    #chassis.turn(15 ,then=Stop.NONE)
    chassis.straight(750)


def red_run():
    chassis.use_gyro(True) # use PID for the wall following
    chassis.settings(straight_speed= 500, straight_acceleration=500)
    #chassis.settings(straight_speed= 200, straight_acceleration=200)

    arm_left.run_time(speed=900, time=1000,wait=False)
    arm_right.run_time(speed=-900, time=1000)
    chassis.straight(560)
    chassis.straight(-40)

    arm_left.run_time(speed=-900, time=3000,wait=False)
    arm_right.run_time(speed=900, time=3000)
    chassis.settings(straight_speed=800, straight_acceleration=800)
    chassis.straight(-500)





def run_none():
    #hsv_check(arm_color_sensor)
    #chassis.straight(100000)
    wheels_cleaning()
    








runs = [
    (BLACK, black_run, 1, "black run"),
    (WHITE, white_run, 2, "white run"),
    # (ORANGE, orange_run, 3, "orange run"),
    (YELLOW, yellow_run, 4, "yellow run"),
    (BLUE, blue_run, 56, "blue+vroom vroom contingency"),
    (GREEN, green_run, 7, "matcha run"),
    (RED, red_run, 8, "red run"),
    (NO_COLOR, run_none, 0, "run straight"),
]  # for each run: attachment color, run function, run number (for display)

finished = False
while not finished:
    for run in runs:
        if arm_color_sensor.color() == run[0]:
            finished = True
            hub.display.number(run[2])  # Display run number on the matrix (screen)
            hub.light.on(run[0])  # Change the button light color to the run color
            print("BAT_percent:", f"{check_battery_percent()}%")
            run_task(run[1]())  # Run the run funciton
            break

