import keyboard

def keyboardInput():
    right = False
    up = False
    down = False
    left = False
    if keyboard.is_pressed("up arrow"):
        up = True
    if keyboard.is_pressed("down arrow"):
        down = True
    if keyboard.is_pressed("left arrow"):
        left = True
    if keyboard.is_pressed("right arrow"):
        right = True
    return [up, down, left, right]
    

def newton(hp):
    return(hp * 735.49875)