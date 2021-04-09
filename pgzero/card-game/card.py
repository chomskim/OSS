import pgzrun
import math
import random 

WIDTH = 963 
HEIGHT = 464

CARD_WIDTH = 71
CARD_HEIGHT = 96
GAP = 20
	
ROWMAX = 4
COLMAX = 13
	
class CardTile:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.width = w
    self.height = h

  def contains(self, px, py):
    return self.x < px and px < self.x+self.width and self.y < py and py < self.y+self.height

cardNames = [
  "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
  "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "dj", "dq", "dk",
  "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk",
  "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk"
  ]

cardSprites = [Actor(card) for card in cardNames]
cardSpritesDic = {}
for card in cardNames:
  cardSpritesDic[card] = Actor(card)
cardSpritesDic["back"] = Actor("b1fv")

WHITE = (255,255,255)
BACK_GROUND = (0x00, 0x66, 0x33)


TOP_LEFT = 0
CW2 = CARD_WIDTH / 2
CH2 = CARD_HEIGHT / 2

tile2d = [None]*COLMAX*ROWMAX
for i in range(ROWMAX):
  for j in range(COLMAX):
    tile2d[i*COLMAX+j] = CardTile(j*CARD_WIDTH+GAP, i*CARD_HEIGHT+GAP, CARD_WIDTH, CARD_HEIGHT)

cardStatus = cardNames[:]
cardStatusOpen = [True]*COLMAX*ROWMAX

#for i in range(ROWMAX):
#  for j in range(COLMAX):
#    print(cardStatus[i*COLMAX + j], end =" ")
#  print ()

def suffle(count):
  for _ in range(count):
    r1 = math.floor(random.random() * ROWMAX)
    r2 = math.floor(random.random() * ROWMAX)
    c1 = math.floor(random.random() * COLMAX)
    c2 = math.floor(random.random() * COLMAX)
    card1 = cardStatus[r1*COLMAX + c1]
    cardStatus[r1*COLMAX + c1] = cardStatus[r2*COLMAX + c2]
    cardStatus[r2*COLMAX + c2] = card1

def draw():
  screen.fill(WHITE)
  screen.draw.filled_rect(Rect(TOP_LEFT,TOP_LEFT,TOP_LEFT+WIDTH,TOP_LEFT+HEIGHT),BACK_GROUND)
  
  for loc, tile in enumerate(tile2d):
    card = cardStatus[loc]
    isopen = cardStatusOpen[loc]
    sprite = cardSpritesDic[card] if isopen else cardSpritesDic["back"]
    sprite.pos = tile.x+CW2, tile.y+CH2
    sprite.draw()

def update():
	# ToDo
	pass

def find_mouse_point_tile(px, py):
  for i, ti in enumerate(tile2d):
    if ti.contains(px, py):
      return i
  return -1

def on_mouse_down(pos):
  px, py = pos
  pos = find_mouse_point_tile(px, py)
  cardStatusOpen[pos] = not cardStatusOpen[pos]
  return pos

suffle(1000)
pgzrun.go()