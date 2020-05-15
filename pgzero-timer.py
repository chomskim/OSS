import pgzrun


timer = 0
frame_count = 0

def update(dt):
    global timer
    global frame_count
    timer += dt
    frame_count += 1


def draw():
    screen.clear()
    screen.draw.text(f"Time passed: {timer} frame count:{frame_count}", (0, 0))
    if timer > 5:    
        print("FPS: ", frame_count/timer)
        screen.draw.textbox("Time's up!", Rect(50, 50, 200, 200))

pgzrun.go()