import pgzrun

WIDTH = 963 
HEIGHT = 464

CARD_WIDTH = 71
CARD_HEIGHT = 96
GAP = 20
	
ROWMAX = 4
COLMAX = 13
	
cardImgFiles = [
  		"c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
  		"d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "dj", "dq", "dk",
  		"s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk",
  		"h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk"
  	]

cardSprites = [Actor(cardImg) for cardImg in cardImgFiles]

CARD_BACK = Actor('b1fv')

WHITE = (255,255,255)
BACK_GROUND = (0x00, 0x66, 0x33)


TOP_LEFT = 0
CW2 = CARD_WIDTH / 2 + GAP
CH2 = CARD_HEIGHT / 2 + GAP

def draw():
	screen.fill(WHITE)
	screen.draw.filled_rect(Rect(TOP_LEFT,TOP_LEFT,TOP_LEFT+WIDTH,TOP_LEFT+HEIGHT),BACK_GROUND)

	col = 0
	row = 0
	for sp in cardSprites:
		sp.pos = col*CARD_WIDTH + CW2, row*CARD_HEIGHT + CH2
		sp.draw()
		col += 1
		if col == 13:
			col = 0
			row += 1 

def update():
	# ToDo
	pass

pgzrun.go()