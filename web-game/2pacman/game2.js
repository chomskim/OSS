
const ZERO_POS = { x : 0, y : 0 };
const FPS = 60;
const SPEED = 3;
const MOVE_SPEED = 1;
const WIDTH = 600
const HEIGHT = 580
const LIVES_MAX = 3;

var canvas;
var canvasContext;

//var mousePos = { x : 0, y : 0 };
var keyDown = -1;

function randint(st, end) {
	return Math.floor(Math.random() * (end-st+1) + st);
}

function Ghost(sprite, pos) {
	this.sprite = sprite;
	this.position = pos;
	this.dir = randint(0,3);
	this.status = 0;
	
	this.center = { x : this.sprite.width / 2, y : this.sprite.height / 2 };
	this.contains = function(p1) {
		return this.position.x-this.center.x < p1.x && p1.x < this.position.x+this.center.x
		&& this.position.y-this.center.y < p1.y && p1.y < this.position.y+this.center.y;
	};
	this.colliderect = function(target) {
		var targetX = target.position.x + target.center.x;
		var targetY = target.position.y + target.center.y;
		var distX = Math.abs(targetX - (this.position.x + this.center.x));
		var distY = Math.abs(targetY - (this.position.y + this.center.y));
		return distX < this.center.x && distY < this.center.y
	};
	this.ghostCollided = function() {
        for (var g=0; g<ghosts.length; ++g) {
            if (ghosts[g]!==this && ghosts[g].colliderect(this))
                return true;
        }
        return false;
	};
	this.draw = function () {
		drawImage(this.sprite, this.position, 0, this.center);
	};
}
function Dot(sprite, pos) {
	this.sprite = sprite;
    this.position = pos;
    this.status = 0;
    this.type = 1;
    
	this.center = { x : this.sprite.width / 2, y : this.sprite.height / 2 };
	this.contains = function(p1) {
		return this.position.x-this.center.x < p1.x && p1.x < this.position.x+this.center.x
		&& this.position.y-this.center.y < p1.y && p1.y < this.position.y+this.center.y;
	};
	this.draw = function () {
		drawImage(this.sprite, this.position, 0, this.center);
	};
}
function Player(sprite, pos) {
	this.sprite = sprite;
    this.position = pos;
	this.status = 0;
	this.movex = 0;
	this.movey = 0;
	this.angle = 0;
	this.lives = 3;
	
	this.center = { x : this.sprite.width / 2, y : this.sprite.height / 2 };
	this.draw = function () {
		drawImage(this.sprite, this.position, this.angle*Math.PI/180, this.center);
	};
	this.contains = function(p1) {
		return this.position.x-this.center.x < p1.x && p1.x < this.position.x+this.center.x
		&& this.position.y-this.center.y < p1.y && p1.y < this.position.y+this.center.y;
	};

}

function Life(sprite, pos) {
	this.sprite = sprite;
    this.position = pos;
	this.center = { x : this.sprite.width / 2, y : this.sprite.height / 2 };
	this.draw = function () {
		drawImage(this.sprite, this.position, 0, ZERO_POS);
	};
}
function Sound(sound, looping) {
	this.looping = typeof looping !== 'undefined' ? looping : false;
	this.sound = new Audio();
	this.sound.src = sound;
	this.play = function () {
		if (this.sound === null) {
			return;
		}
		console.log("Sound play ", this.sound.src);
		this.sound.load();
		this.sound.autoplay = true;
		if (this.looping) {
			this.sound.addEventListener('ended', function () {
				this.load();
				this.autoplay = true;
			}, false);
		}
	}
}

var spritesStillLoading = 0;
var sprites = {};
var sounds = {};

var level = 0;
var player;
var pacDots = [];
var ghosts = [];
var lives = [];

var moveDelay = FPS/SPEED;
var moveCount = 0;

var score = 0;

window.requestAnimationFrame =  window.requestAnimationFrame ||
								window.webkitRequestAnimationFrame ||
								window.mozRequestAnimationFrame ||
								window.oRequestAnimationFrame ||
								window.msRequestAnimationFrame ||
								function (callback) {
    								window.setTimeout(callback, 1000 / FPS);
								};

function clearCanvas() {
	canvasContext.clearRect(0, 0, canvas.width, canvas.height);
}
function drawImage (sprite, position, rotation, center) {
	canvasContext.save();
	canvasContext.translate(position.x, position.y);
	canvasContext.rotate(rotation);
	canvasContext.drawImage(sprite, 0, 0, sprite.width, sprite.height,
			-center.x, -center.y, sprite.width, sprite.height);
	canvasContext.restore();
}

function drawText(textId, textStr) {
	var textArea = document.getElementById(textId)
	textArea.innerHTML = textStr;
	textArea.style.cursor = "default";
}
function clearTexts() {
	drawText('textArea', '');
}

function isImageDataBlack(mapArray, x, y) {
	var xp = Math.floor(x/20);
	var yp = Math.floor(y/20);
	//console.log('xp, yp=', xp, yp, 'mapArray[yp][xp]=',mapArray[yp][xp], mapArray[yp][xp]==='1');
	return mapArray[yp][xp]==='1';
}
function getDotMapData(x, y) {
	var xp = Math.floor(x/20);
	var yp = Math.floor(y/20);
	//console.log('xp, yp=', xp, yp, 'mapArray[yp][xp]=',mapArray[yp][xp], mapArray[yp][xp]==='1');
	return parseInt(dotmap[yp][xp]);
}

function draw() {

	clearCanvas();
	clearTexts();
	drawImage(sprites['header'], ZERO_POS, 0, ZERO_POS);
	drawImage(sprites['colourmap'], { x : 0, y : 80 }, 0, ZERO_POS);

    var pacDotsLeft = 0;
    for (var a=0; a<pacDots.length; ++a) {
        if (pacDots[a].status === 0) {
            pacDots[a].draw();
            pacDotsLeft += 1;
        }
        if (pacDots[a].contains({ x:player.position.x, y:player.position.y })) {
            if (pacDots[a].status === 0) {
                if (pacDots[a].type === 2) {
                    for (var g=0; g<ghosts.length; ++g){
                    	ghosts[g].status = 1200;
                    }
                }
                else {
                    score += 10;
                }
            }
            pacDots[a].status = 1;
        }
    }
    if (pacDotsLeft === 0)
    	player.status = 2;
    drawGhosts();
    
    getPlayerImage();
    player.draw();
    drawLives();


	drawText('scoreArea', score);
	drawText('levelArea', "LEVEL " + level);
	if (player.status === 1) {
		drawText('textArea', "CAUGHT!<br>Press Enter to Continue");
	}
	if (player.status === 2) {
		drawText('textArea', "LEVEL CLEARED!<br>Press Enter to Continue");
	}
	if (player.status === 3) {
		drawText('textArea', "GAME OVER");
	}
}
function drawLives() {
    for (var l=0; l < player.lives; ++l) {
    	lives[l].draw();
    }
}

function update() {
	if (player.status === 0) {
		//console.log("update moveGhostsFlag=", moveGhostsFlag, "moveCount=", moveCount);
		if (moveCount <= moveDelay) { // every FPS cycle
			updateGhosts();
			for (var g=0; g<ghosts.length; ++g) {
				if (ghosts[g].status > 0)
					ghosts[g].status -= 1;
				if (ghosts[g].contains({x:player.position.x, y:player.position.y})) {
					if (ghosts[g].status > 0) {
						score += 100;
						ghosts[g].position = { x: 290, y: 370 };
					}
					else {
						player.lives -= 1;
	                    sounds["pac2"].play();
	                    if (player.lives === 0) {
	                        player.status = 3;
	                        //music.fadeout(3);
	                    }
	                    else {
	                        player.status = 1;
	                    }
					}
				}
			}
			//animate(player, 
			//pos=(player.x + player.movex, player.y + player.movey), 
			//duration=1/SPEED, tween='linear', on_finished=inputUnLock)
			if (player.movex !== 0 || player.movey !== 0) {
				//inputLock();
				player.position.x += player.movex;
				player.position.y += player.movey;
			}
		}
		else { // 1/3 sec period
			moveCount = 0;
			inputUnLock();
			checkInput();
			//if (player.movex !== 0 || player.movey !== 0)
			//	console.log("checkInput move x,y=", player.movex, player.movey);
			checkMovePoint(player);
			if (player.movex !== 0 || player.movey !== 0) {
			//console.log("checkMovePoint move x,y=", player.movex, player.movey, 
			//		"pos=",player.position);
				sounds["pac1"].play();
			}
			moveGhosts();
		}
		moveCount +=1;
	}
    if (player.status === 1) {
        if (checkInput() === 1) {
            player.status = 0;
            player.position.x = 290;
            player.position.y = 570;
        }
    }
    if (player.status === 2) {
        if (checkInput() === 1)
            initialize();
    }
	
}
var dmoves = [[1,0],[0,1],[-1,0],[0,-1]];
//             -->    v    <--     ^
function updateGhosts() {
    for (var g=0; g<ghosts.length; ++g) {
		ghosts[g].position.x += dmoves[ghosts[g].dir][0]*MOVE_SPEED;
		ghosts[g].position.y += dmoves[ghosts[g].dir][1]*MOVE_SPEED;
    }
}
function getPlayerImage() {
	if (player.status !== 0) {
		player.sprite = sprites["pacman_o"];
		return;
	}
    var dt = new Date().getTime() * 1000; // micro seconds
    var a = player.angle;
    var tc = dt % (500000/SPEED) / (100000/SPEED);
    //console.log("tc=", tc);
    if (tc > 2.5 && (player.movex !== 0 || player.movey !== 0)) {
        if (a !== 180)
            player.sprite = sprites["pacman_c"];
        else
            player.sprite = sprites["pacman_cr"];
    }
    else {
        if (a !== 180)
            player.sprite = sprites["pacman_o"];
        else
            player.sprite = sprites["pacman_or"];
    }
}

function drawGhosts() {
    for (var g=0; g<ghosts.length; ++g) {
    	//console.log('"ghost"+(g+1)', "ghost"+(g+1));
    	if (ghosts[g].position.x > player.position.x) {
            if (ghosts[g].status > 200 || (ghosts[g].status > 1 && ghosts[g].status%2 === 0)) 
            	ghosts[g].sprite = sprites["ghost5r"];
            else
            	ghosts[g].sprite = sprites["ghost"+(g+1)+"r"];
    	}
    	else {
            if (ghosts[g].status > 200 || (ghosts[g].status > 1 && ghosts[g].status%2 === 0)) 
            	ghosts[g].sprite = sprites["ghost5"];
            else
            	ghosts[g].sprite = sprites["ghost"+(g+1)];
    	}
    	ghosts[g].draw();
    }
}

function moveGhosts() {
	//console.log('moveGhosts', 'moveGhostsFlag=',moveGhostsFlag);
	moveGhostsFlag = 0;
    for (var g=0; g<ghosts.length; ++g) {
        var dirs = getPossibleDirection(ghosts[g]);
        if (inTheCentre(ghosts[g]))
        	ghosts[g].dir = 3;
        else {
            if (g === 0)
            	followPlayer(g, dirs);
            if (g === 1)
            	ambushPlayer(g, dirs);
        }
        if (dirs[ghosts[g].dir] === 0 || randint(0,50) === 0) {
            var d = -1;
            while (d === -1) {
                var rd = randint(0,3);
                if (dirs[rd] === 1)
                    d = rd;
            }
            //console.log("dirs[ghosts[g].dir] =", dirs[ghosts[g].dir], "d=", d);
            ghosts[g].dir = d;
        }
		//animate(ghosts[g], 
		//pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), 
		//duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)
    }
}
function followPlayer(g, dirs) {
    var d = ghosts[g].dir;
    if (d === 1 || d === 3) {
        if (player.position.x > ghosts[g].position.x && dirs[0] === 1)
        	ghosts[g].dir = 0;
        if (player.position.x < ghosts[g].position.x && dirs[2] === 1)
        	ghosts[g].dir = 2;
    }
    if (d === 0 || d === 2) {
        if (player.position.y > ghosts[g].position.y && dirs[1] == 1 && !aboveCentre(ghosts[g]))
        	ghosts[g].dir = 1;
        if (player.position.y < ghosts[g].position.y && dirs[3] == 1)
        	ghosts[g].dir = 3;
    }
}

function ambushPlayer(g, dirs) {
    var d = ghosts[g].dir
    if (player.movex > 0 && dirs[0] === 1)
    	ghosts[g].dir = 0;
    if (player.movex < 0 && dirs[2] === 1)
    	ghosts[g].dir = 2;

    if (player.movey > 0 && dirs[1] == 1 && !aboveCentre(ghosts[g]))
    	ghosts[g].dir = 1;
    if (player.movey < 0 && dirs[3] == 1)
    	ghosts[g].dir = 3;
}

function inTheCentre(ga) {
    if (ga.position.x > 220 && ga.position.x < 380 && ga.position.y > 320 && ga.position.y < 420)
        return true;
    return false;
}
function aboveCentre(ga) {
    if (ga.x > 220 && ga.x < 380 && ga.y > 300 && ga.y < 320)
        return true;
    return false;
}

function handleKeyDown(evt) {
	if (evt.repeat !== undefined) {
		if (evt.keyCode !== -1)
			keyDown = evt.keyCode;
	}
}

function handleKeyUp(evt) {
    keyDown = -1;
}

function handleMouseMove(evt) {
	mousePos = {x: evt.clientX, y: evt.clientY };
}
function handleMouseDown(evt) {
}

function handleMouseUp(evt) {
}

function loadSprite(imageName) {
    var image = new Image();
    image.src = imageName;
    spritesStillLoading += 1;
    image.onload = function () {
        spritesStillLoading -= 1;
    };
    return image;
}
function loadAssets() {
	// load sprites
	sprites["colourmap"] = loadSprite("images/colourmap.png");
	sprites["dot"] = loadSprite("images/dot.png");
	sprites["ghost1"] = loadSprite("images/ghost1.png");
	sprites["ghost1r"] = loadSprite("images/ghost1r.png");
	sprites["ghost2"] = loadSprite("images/ghost2.png");
	sprites["ghost2r"] = loadSprite("images/ghost2r.png");
	sprites["ghost3"] = loadSprite("images/ghost3.png");
	sprites["ghost3r"] = loadSprite("images/ghost3r.png");
	sprites["ghost4"] = loadSprite("images/ghost4.png");
	sprites["ghost4r"] = loadSprite("images/ghost4r.png");
	sprites["ghost5"] = loadSprite("images/ghost5.png");
	sprites["ghost5r"] = loadSprite("images/ghost5r.png");
	sprites["header"] = loadSprite("images/header.png");
	sprites["pacman_c"] = loadSprite("images/pacman_c.png");
	sprites["pacman_cr"] = loadSprite("images/pacman_cr.png");
	sprites["pacman_o"] = loadSprite("images/pacman_o.png");
	sprites["pacman_or"] = loadSprite("images/pacman_or.png");
	sprites["pacmandotmap"] = loadSprite("images/pacmandotmap.png");
	sprites["pacmanmovemap"] = loadSprite("images/pacmanmovemap.png");
	sprites["player"] = loadSprite("images/player.png");
	sprites["power"] = loadSprite("images/power.png");

	// load sounds
	sounds["pm1"] = new Sound("music/pm1.mp3", true);
	sounds["pm1"].sound.volume = 0.5;
	sounds["pac1"] = new Sound("sounds/pac1.ogg");
	sounds["pac2"] = new Sound("sounds/pac2.ogg");
}
function assetLoadingLoop() {
    if (spritesStillLoading > 0)
        window.requestAnimationFrame(assetLoadingLoop);
    else {
        initialize();
        mainLoop();
    }
}
function initDots() {
	pacDots = [];
    for (var x=0; x<30; ++x) {
    	for (var y=0; y<29; ++y) {
    		var d = checkDotPoint({ x :10+x*20, y :10+y*20 });
    		var dot;
    		if (d === 1) {
    			dot = new Dot(sprites["dot"], { x :10+x*20, y :90+y*20 });
    			dot.type = 1;
    			pacDots.push(dot);
    		}
    		else if (d === 2) {
    			dot = new Dot(sprites["power"], { x :10+x*20, y :90+y*20 });
    			dot.type = 2;
    			pacDots.push(dot);
    		}
    	}
    }
}

function initGhosts() {
	moveGhostsFlag = 4;
	ghosts = [];
    for (var g=0; g<4; ++g) {
    		ghosts.push(new Ghost(sprites["ghost"+(g+1)], {x:270+(g*20), y:370}));
    }
}

function inputLock() {
}
function inputUnLock() {
    player.movex = 0;
    player.movey = 0;
}

function checkInput() {

	if (player.status === 0) {
		switch (keyDown) {
		case Keys.left:
			player.angle = 180;
			player.movex = -1;
			break;
		case Keys.right:
			player.angle = 0;
			player.movex = 1;
			break;
		case Keys.up:
			player.angle = 270;
			player.movey = -1;
			break;
		case Keys.down:
			player.angle = 90;
			player.movey = 1;
			break;
		}
	}
	else if (player.status === 1 || player.status === 2) {
		if (keyDown === Keys.enter) {
			return 1;
		}
	}
	return 0;
}

function checkMovePoint(p) {
    if (p.position.x+p.movex*20 < 0)
    	p.position.x = p.position.x+600;
    if (p.position.x+p.movex*20 > 600)
    	p.position.x = p.position.x-600;
    //console.log("checkMovePoint=", p.position.x+p.movex*20, p.position.y+p.movey*20-80,
    //		isImageDataBlack(movemap, p.position.x+p.movex*20, p.position.y+p.movey*20-80));
    if (!isImageDataBlack(movemap, p.position.x+p.movex*20, p.position.y+p.movey*20-80)) {
        p.movex = 0;
        p.movey = 0;
        playerMoveX = 0;
        playerMoveY = 0;
    }
}

function checkDotPoint(pos) {
    return getDotMapData(pos.x, pos.y);
}
function getPossibleDirection(g) {
    if (g.position.x-20 < 0)
    	g.position.x = g.position.x+600;
    if (g.position.x+20 > 600)
        g.position.x = g.position.x-600;
    var directions = [0,0,0,0];
    if (g.position.x+20 < 600)
        if (isImageDataBlack(movemap, g.position.x+20, g.position.y-80))
        	directions[0] = 1;
    if (g.position.x < 600 && g.position.x >= 0)
        if (isImageDataBlack(movemap, g.position.x, g.position.y-60))
        	directions[1] = 1;
    if (g.position.x-20 >= 0)
        if (isImageDataBlack(movemap, g.position.x-20, g.position.y-80))
        	directions[2] = 1;
    if (g.position.x < 600 && g.position.x >= 0)
        if (isImageDataBlack(movemap, g.position.x, g.position.y-100))
        	directions[3] = 1;
    return directions;
}                       

function initialize() {
	
	//console.log('dotmap =',dotmap);
	//console.log('movemap =',movemap);
	initDots();
	initGhosts();
	
	player = new Player(sprites["pacman_o"], { x : 290, y : 570 });
	
	for (var i=0; i<LIVES_MAX; ++i) {
		lives.push(new Life(sprites["pacman_o"], {x: 10+(i*32), y: 40}));
	}
	inputUnLock();
	level += 1;
	sounds["pm1"].play();
	// mouse initialize
    //document.onmousedown = handleMouseDown;
    //document.onmouseup = handleMouseUp;
    //document.onmousemove = handleMouseMove;
    
	// Keyboard initialize
    document.onkeydown = handleKeyDown;
    document.onkeyup = handleKeyUp;
    
	canvas.style.cursor = "default";

}
function handleInput() {
}

function mainLoop() {
    handleInput();
    update();
    
    draw();
    
    window.requestAnimationFrame(mainLoop);
}
function start() {
	canvas = document.getElementById("gamepan");
	canvasContext = canvas.getContext("2d");

	loadAssets();
	assetLoadingLoop();
}
document.addEventListener( 'DOMContentLoaded', start);

