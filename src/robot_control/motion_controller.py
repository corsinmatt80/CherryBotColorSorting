import time

def send_command(command):

    #INSERT REAL FUNCTION HERE

    print(f"Sending Command: {command}")
    time.sleep(0.5)


def move_to_bin(color):
    if color == "red":
        send_command("MOVE_TO_RED_BIN")
    elif color == "dark":
        send_command("MOVE_TO_BIN_DARK")
    elif color == "light":
        send_command("MOVE_TO_BIN_LIGHT")
    else:
        print("Invalid color")