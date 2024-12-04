from backend.robot_control.robot_control_http import move, toggle

def pick_up_cloth(token: str):
    move(0, 0, 180, 0, 0, 0, token) # Use coordinates of the cloth pile
    toggle(token)

def move_to_bin(color: str, token: str):
    if color == "light":
        move(0, 0, 180, 0, 0, 0, token) # Use coordinates of the light bin
        toggle(token)
    elif color == "dark":
        move(0, 0, 180, 0, 0, 0, token) # Use coordinates of the dark bin
        toggle(token)
    elif color == "unsortable":
        move(0, 0, 180, 0, 0, 0, token) # Use coordinates of the unsorted bin
        toggle(token)
    elif color == "colored":
        move(0, 0, 180, 0, 0, 0, token) # Use coordinates of the color bin
        toggle(token)

def pick_up_cloth_and_move_to_bin(token: str, color: str):
    pick_up_cloth(token)
    move_to_bin(color, token)