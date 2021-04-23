import pgzrun
from datetime import datetime

sec = 0
def draw():
  global sec
  if sec == 60:
    sec = 0
    screen.fill((0,0,0))
    screen.draw.text(str(datetime.now()).split('.')[0], (100, 200))
    print(datetime.now())


def update(dt):
    global sec
    sec += 1

pgzrun.go()