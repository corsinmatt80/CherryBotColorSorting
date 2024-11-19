import requests
import json
import time
import math
import numpy

base_url = 'https://api.interactions.ics.unisg.ch/cherrybot2'

def initialize():
    time.sleep(1)
    url = base_url + '/initialize'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        global current_distance
        global current_angle
        global initz
        global initpitch
        global initroll
        tcp = get_tcp()
        initx = tcp['coordinate']['x']
        inity = tcp['coordinate']['y']
        initz = tcp['coordinate']['z']
        initpitch = tcp['rotation']['pitch']
        initroll = tcp['rotation']['yaw']
        current_angle = tcp['rotation']['yaw']
        current_distance = float(math.sqrt(initx * initx + inity * inity))
        current_angle = 0
        print("Coordinates: ", initx, inity, initz)
    else:
        return False


def put_x_y_yaw(x, y, yaw):
    time.sleep(1)
    print(x, y, yaw)
    url = base_url + '/tcp/target'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    payload = json.dumps({
  "target": {
    "coordinate": {
      "x": x,
      "y": y,
      "z": initz
    },
    "rotation": {
      "roll": initroll,
      "pitch": initpitch,
      "yaw": yaw
    }
  },
  "speed": 50
})
    requests.put(url, headers=headers, data=payload)


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


# Use by the command move
def move(param):
    global current_distance
    global current_angle
    current_distance += float(param)
    x = math.cos(numpy.deg2rad(current_angle)) * current_distance
    y = math.sin(numpy.deg2rad(current_angle)) * current_distance
    put_x_y_yaw(x, y, current_angle)


# Use by the command rotate
def rotate(param):
    global current_distance
    global current_angle
    current_angle += float(param)
    if current_angle < 0:
        current_angle += 360
    elif current_angle >= 360:
        current_angle -= 360
    x = math.cos(numpy.deg2rad(current_angle)) * current_distance
    y = math.sin(numpy.deg2rad(current_angle)) * current_distance
    put_x_y_yaw(x, y, current_angle)
    # Add your code here to connect to process the rotate command.


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
