import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = 'Draw O'

WHITE=(255,255,255)
BLACK=(0,0,0)
BACK_GROUND = (0xEE, 0xFF, 0xFF)

o400 = Actor('o400')

def draw():
    screen.fill(BACK_GROUND)
    o400.draw()


def update():
    pass

pgzrun.go()
