import pgzrun

WIDTH = 600
HEIGHT = 600
TITLE = 'Tic Tac Toe'

WBOX = 400
OBOX = 100

wdiv3 = WBOX / 3
hdiv3 = WBOX / 3
wdiv32 = wdiv3*2.0
hdiv32 = hdiv3*2.0

woffset = wdiv3 / 2
hoffset = hdiv3 / 2

WHITE=(255,255,255)
BACK_GROUND = (0xEE, 0xFF, 0xFF)
BLUE10 = (125,125,255)

o133 = Actor('o133')
x133 = Actor('x133')

stage = 0
tileStatus = [
			0,0,0,
			0,0,0,
			0,0,0]
winList = [
		[0,1,2],
		[3,4,5],
		[6,7,8],
		[0,3,6],
		[1,4,7],
		[2,5,8],
		[0,4,8],
		[2,4,6]
	]

def drawLine2(color, x1, y1, w, h):
    rect = Rect((x1, y1), (w, h))
    screen.draw.filled_rect(rect, color)

def drawX(tile):
    px = tile.x + OBOX
    py = tile.y + OBOX
    Actor('x133', (px+woffset, py+hoffset)).draw()

def drawO(tile):
    px = tile.x + OBOX
    py = tile.y + OBOX
    Actor('o133', (px+woffset, py+hoffset)).draw()

class Tile:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def contains(self, px, py):
        return self.x < px and px < self.x+self.width and self.y < py and py < self.y+self.height

tiles = [ 
    Tile(0,0,wdiv3,hdiv3), Tile(wdiv3,0,wdiv3,hdiv3), Tile(wdiv32,0,wdiv3,hdiv3),
    Tile(0,hdiv3,wdiv3,hdiv3), Tile(wdiv3,hdiv3,wdiv3,hdiv3), Tile(wdiv32,hdiv3,wdiv3,hdiv3),
    Tile(0,hdiv32,wdiv3,hdiv3), Tile(wdiv3,hdiv32,wdiv3,hdiv3), Tile(wdiv32,hdiv32,wdiv3,hdiv3)]

def findMousePointTile(px, py):
    for i, ti in enumerate(tiles):
        if ti.contains(px, py):
            return i;
    return -1;

def draw():
    screen.fill(WHITE)
    screen.draw.filled_rect(Rect(OBOX,OBOX,WBOX,WBOX), BACK_GROUND)

    # Draw OX Mark
    for i,t in enumerate(tiles):
        if tileStatus[i]==1: 
            drawX(tiles[i])
        elif tileStatus[i]==2:
            drawO(tiles[i])
    
    # Draw Tile Line
    for i in range(4):
        drawLine2(BLUE10, wdiv3*i+OBOX, 0+OBOX, 2, WBOX+2)
        drawLine2(BLUE10, 0+OBOX, hdiv3*i+OBOX, WBOX+2, 2)
    
def update():
    pass

def on_mouse_down(pos):
    global stage
    px, py = pos
    px -= OBOX
    py -= OBOX
    pos = findMousePointTile(px, py)
    if tileStatus[pos]==0:
        stage += 1
        if stage%2 == 0:
            tileStatus[pos] = 2
        else:
            tileStatus[pos] = 1

pgzrun.go()
