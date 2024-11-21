import calibrator
import robot_control_http as rch

token = None

def log_on():
    global token
    name = "janis"
    email = "janisjoel.enzler@student.unisg.ch"
    token = rch.log_on(name, email)

def log_off():
    rch.log_off(token)

def stop():
    rch.initialize(token)

def start_position():
    rch.move(400, 0, 250, -180, 0, -180, token)

def calibrate():
    calibrator.calibrate(token)

def move(x, y, z, pitch, roll, yaw):
    rch.move(x, y, z, pitch, roll, yaw, token)

def get_token():
    global token
    token = rch.get_token()


while True:
    command = input("Command: ")
    try:
        func, param = command.split(" ", 1)
        exec(f'{func}(\"{param}\")')
    except:
        try:
            exec(f'{command}()')
        except:
            pass