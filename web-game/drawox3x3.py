import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = 'Draw OX 3x3'

wdiv3 = WIDTH / 3
hdiv3 = HEIGHT / 3
woffset = wdiv3 / 2
hoffset = hdiv3 / 2

BACK_GROUND = (0xEE, 0xFF, 0xFF)

o133 = Actor('o133')
x133 = Actor('x133')

def draw():
    screen.fill(BACK_GROUND)
    for row in range(3):
        for col in range(3):
            if (row*3 + col) % 2 == 0:
                Actor('x133', (wdiv3*row+woffset, hdiv3*col+hoffset)).draw()
            else:
                Actor('o133', (wdiv3*row+woffset, hdiv3*col+hoffset)).draw()

def update():
    pass

pgzrun.go()
