import requests
import json
import time

# Swaggerhub: https://app.swaggerhub.com/apis-docs/interactions-hsg/robots/1.0.0

base_url = 'https://api.interactions.ics.unisg.ch/cherrybot2'
movement_speed = 100


def initialize(token):
    time.sleep(1)
    url = base_url + '/initialize'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    response = requests.put(url, headers=headers)
    return response.status_code


def get_token():
    time.sleep(1)
    response = requests.get(base_url + '/operator')
    if response.status_code == 200:
        return dict(json.loads(response.text))['token']
    else:
        return None

# Log on with "log_on name,email"
def log_on(name, email):
    print("connect to the robot\n")
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
        # We retrieve the token again, because the response to the post request is in an
        token = get_token()
        return token
    else:
        return response.status_code



# Move to a position with "move x,y,z, pitch, roll, yaw"
def move(new_x, new_y, new_z, new_pitch, new_roll, new_yaw, token):
    # Protect against collisions with the table

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

    return response.status_code

def open_gripper(token):
    url = base_url + '/gripper'
    headers = {
        'Content-Type': 'application/json',
        'Authentication': token
    }
    response = requests.put(url, headers=headers, data='500')
    return response.status_code



# Log off with "log_off" command
def log_off(token):
    try:
        url = base_url + '/operator/'
        url += token
        response = requests.delete(url)

        return response.status_code
    except:
        return None



