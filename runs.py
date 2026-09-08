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
arm_right = Motor(Port.A)
arm_left = Motor(Port.E)
# Wheels
wheel_left = Motor(Port.F, Direction.COUNTERCLOCKWISE)
wheel_right = Motor(Port.B)

chassis = DriveBase(wheel_left, wheel_right, 62.4, 97.5)

# reflection color
WHITE = Color(h=10, s=0, v=100)
# RED = Color(h=352, s=92, v=75)
# BLUE = Color(h=218, s=94, v=72)
# GREEN = Color(h=155, s=78, v=48)
# YELLOW = Color(h=40, s=70, v=100)
BLACK = Color(h=210, s=57, v=8)
# ORANGE = Color(h=7, s=86, v=99)
NO_COLOR = Color(h=200, s=78, v=5)

arm_color_sensor.detectable_colors(
    [
        WHITE,
        # RED,
        # BLUE,
        # GREEN,
        # YELLOW,
        BLACK,
        # ORANGE,
        NO_COLOR
    ]
)

def drive_settings(straight_speed=300, straight_acceleration=300, turn_rate=300, turn_acceleration=400):
    """resets to the default speed, acceleration and turn rate"""
    chassis.settings(
        straight_speed=straight_speed,
        straight_acceleration=straight_acceleration,
        turn_rate=turn_rate,
        turn_acceleration=turn_acceleration,
    )

def reset(gyro=0):
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


def black_run():
    chassis.straight(500)

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
        chassis.curve(radius=300, angle=90)
        chassis.straight(-650)
    

def run_none():
    # hsv_check(arm_color_sensor)
    wheels_cleaning()

runs = [
    (BLACK, black_run, 1, "black run"),
    (WHITE, white_run, 2, "white run"),
    # (ORANGE, orange_run, 3, "orange run"),
    # (YELLOW, yellow_run, 4, "yellow run"),
    # (BLUE, blue_run, 56, "blue+vroom vroom contingency"),
    # (GREEN, green_run, 7, "matcha run"),
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