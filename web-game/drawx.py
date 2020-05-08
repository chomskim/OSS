import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = 'Draw X'

WHITE=(255,255,255)
BLACK=(0,0,0)
BACK_GROUND = (0xEE, 0xFF, 0xFF)

x400 = Actor('x400')

def draw():
    screen.fill(BACK_GROUND)
    x400.draw()


def update():
    pass

pgzrun.go()
