import requests
import json
import time

# Swaggerhub: https://app.swaggerhub.com/apis-docs/interactions-hsg/robots/1.0.0

base_url = 'https://api.interactions.ics.unisg.ch/cherrybot2'
movement_speed = 50

def help():
    print("Commands:\n\tlog_on name,email\n\tmove x,y,z, pitch, roll, yaw\n\ttoggle\n\tlog_off\n\tprint_cords\n\tupdate_cords\n\tinitialize\n\tget_tcp\n\tget_token\n\tdeltaMove delta_x, delta_y, delta_z, delta_pitch, delta_roll, delta_yaw\n")

def print_cords():
    global x_pos, y_pos, z_pos, pitch, roll, yaw
    print("Coordinates:", "\n\tx: ", x_pos, "\n\ty: ", y_pos, "\n\tz: ", z_pos, "\n")
    print("Rotation:", "\n\tpitch: ", pitch, "\n\troll: ", roll, "\n\tyaw: ", yaw, "\n")

def get_cords():
    global x_pos, y_pos, z_pos, pitch, roll, yaw
    tcp = get_tcp()
    x_pos = tcp['coordinate']['x']
    y_pos = tcp['coordinate']['y']
    z_pos = tcp['coordinate']['z']
    pitch = tcp['rotation']['pitch']
    roll = tcp['rotation']['roll']
    yaw = tcp['rotation']['yaw']

def update_cords(new_x, new_y, new_z, new_pitch, new_roll, new_yaw):
    global x_pos, y_pos, z_pos, pitch, roll, yaw
    x_pos = new_x
    y_pos = new_y
    z_pos = new_z
    pitch = new_pitch
    roll = new_roll
    yaw = new_yaw

def initialize():
    time.sleep(1)
    url = base_url + '/initialize'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        # Wait for the robot to initialize, and make sure it is done
        time.sleep(5)
        print('Initialization successful\n')
        get_cords()
        print_cords()
    else:
        return False

def get_tcp():
    time.sleep(1)
    url = base_url + '/tcp'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    try:
        data = dict(json.loads(requests.get(url, headers=headers).text))
        return data
    except:
        print('Something went wrong')


def get_token():
    global token
    time.sleep(1)
    response = requests.get(base_url + '/operator')
    token = response.text[-34:-2]
    print(token)


# Log on with "log_on name,email"
def log_on(userdata):
    print("connect to the robot\n")
    name, email = userdata.split(',')
    url = base_url + '/operator'

    payload = json.dumps({
        "name": name,
        "email": email.strip(" ")
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        get_token()
        print("Successful Connection")
        print(f'Token: {token}\n')
        initialize()
    else:
        print("Someone else is using the robot\n")


# Move to a position with "move x,y,z, pitch, roll, yaw"
def move(new_x, new_y, new_z, new_pitch, new_roll, new_yaw):
    # Protect against collisions with the table
    if new_z <= 180:
        new_z = 180

    url = base_url + '/tcp/target'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    payload = json.dumps({
        "target": {
            "coordinate": {
                "x": new_x,
                "y": new_y,
                "z": new_z
            },
            "rotation": {
                "roll": new_roll,
                "pitch": new_pitch,
                "yaw": new_yaw
            }
        },
        "speed": movement_speed
    })
    response = requests.put(url, headers=headers, data=payload)

    if response.status_code == 200:
        print('Moved to position\n')
        update_cords(new_x, new_y, new_z, new_pitch, new_roll, new_yaw)
        print_cords()
    else:
        print('Something went wrong\n')
        print(response.text)

def deltaMove(delta_x, delta_y, delta_z, delta_pitch, delta_roll, delta_yaw):
    move(x_pos + delta_x, y_pos + delta_y, z_pos + delta_z, pitch + delta_pitch, roll + delta_roll, yaw + delta_yaw)

# Toggle gripper with "toggle"
def toggle():
    url = base_url + '/gripper'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }

    distance = json.loads(requests.get(url, headers=headers).text)
    time.sleep(1)
    try:
        if int(distance) == 0:
            response = requests.put(url, headers=headers, data='100')
            if response.status_code == 200:
                print('gripper open\n')
        else:
            response = requests.put(url, headers=headers, data='0')
            if response.status_code == 200:
                print('gripper closed\n')
    except:
        print('Something went wrong\n')


# Log off with "log_off" command
def log_off():
    try:
        print("log off from the robot\n")
        url = base_url + '/operator/'
        url += token
        response = requests.delete(url)

        print(token)

        if response.status_code == 200:
            print("log off successful\n")
        else:
            print("Invalid token, no such user\n")
    except:
        print('Not logged-in\n')

def start_position():
    print("Moving to start position")
    move(400, 0, 250, -180, 0, -180)

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

