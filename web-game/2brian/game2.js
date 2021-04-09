
const ZERO_POS = { x : 0, y : 0 };
const FPS = 60;

var canvas;
var canvasContext;

const CENTER_POS = { x : 400, y : 270 };
var mousePos = { x : 0, y : 0 };

function randint(st, end) {
	return Math.floor(Math.random() * (end-st+1) + st);
}

function Sprite(sprite, pos) {
	this.sprite = sprite;
	this.position = pos;
	this.center = { x : this.sprite.width / 2, y : this.sprite.height / 2 };
	this.contains = function(p1) {
		return this.position.x-this.center.x < p1.x && p1.x < this.position.x+this.center.x
		&& this.position.y-this.center.y < p1.y && p1.y < this.position.y+this.center.y;
	}
	this.draw = function () {
		drawImage(this.sprite, this.position, 0, this.center);
	}
	
}
function Sound(sound) {
	this.sound = new Audio();
	this.sound.src = sound;
	this.onplay = false;
	this.play = function () {
	    if (this.sound === null || this.onplay) {
	        return;
	    }
    	//console.log("Sound play");
	    this.sound.load();
	    this.sound.autoplay = true;
	}
}
function Button(color) {
	this.litSprite = sprites[color+'lit'];
	this.unlitSprite = sprites[color+'unlit'];
	this.state = false;
	this.size = { x : this.litSprite.width, y : this.litSprite.height };
	
	var pos = { x : 0, y : 0 };
	if (color === "red") {
		pos.x = CENTER_POS.x - this.size.x;
		pos.y = CENTER_POS.y - this.size.y;
	}
	else if (color === "green") {
		pos.x = CENTER_POS.x;
		pos.y = CENTER_POS.y - this.size.y;
	}
	else if (color === "blue") {
		pos.x = CENTER_POS.x - this.size.x;
		pos.y = CENTER_POS.y;
	}
	else if (color === "yellow") {
		pos.x = CENTER_POS.x;
		pos.y = CENTER_POS.y;
	}
	this.position = pos;

	this.draw = function () {
		if (this.state) {
			drawImage(this.litSprite, this.position, 0, ZERO_POS);
		}
		else {
			drawImage(this.unlitSprite, this.position, 0, ZERO_POS);
		}
	};
	this.contains = function(p1) {
		return this.position.x < p1.x && p1.x < this.position.x+this.size.x
		&& this.position.y < p1.y && p1.y < this.position.y+this.size.y;
	};

}

var spritesStillLoading = 0;
var sprites = {};
var sounds = [];

const LOOPDELAY = 80;

var myButtons = [];
var playButton;
var buttonList = [];
var playPosition = 0;
var playingAnimation = false;
var gameCountdown = -1;
var score = 0;
var playerInput = [];
var signalScore = false;
var gameStarted = false;

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
function clearButtons() {
	for (var i=0; i<myButtons.length; ++i) {
		myButtons[i].state = false;
	}
}

function playAnimation() {
    playPosition = 0;
    playingAnimation = true;
}

function addButton() {
	var sel = randint(0, 3);
    buttonList.push(randint(0, 3));
    playAnimation();
}

function update() {
    if (playingAnimation) {
        playPosition += 1;
        var listpos = Math.floor(playPosition/LOOPDELAY);
        if (listpos === buttonList.length) {
            playingAnimation = false;
            clearButtons();
        }
        else {
            var litButton = buttonList[listpos];
            if (playPosition%LOOPDELAY > LOOPDELAY/2) {
            	litButton = -1;
            }
            var bcount = 0
            for (var i=0; i<myButtons.length; ++i) {
                if (litButton === bcount) {
                	myButtons[i].state = true;
                    sounds[i].play();
                    sounds[i].onplay = true;
                }
                else {
                	myButtons[i].state = false;
                	sounds[i].onplay = false;
                }
                bcount += 1;
            }
        }
    }
    if (gameCountdown > 0) {
        gameCountdown -=1
        if (gameCountdown === 0) {
            addButton();
            playerInput = [];
        }
    }
}

function gameOver() {
    gameStarted = false;
    gameCountdown = -1;
    playerInput = [];
    buttonList = [];
    clearButtons();
}

function checkPlayerInput() {
    var ui = 0;
    while (ui < playerInput.length) {
        //console.log("ui=", ui);
        if (playerInput[ui] != buttonList[ui]) {
        	gameOver();
        	return;
        }
        ui += 1;
    }
    if (ui >= buttonList.length) {
    	signalScore = true;
    }
    //console.log("playerInput=", playerInput);
    //console.log("buttonList=", buttonList);

}

function handleMouseMove(evt) {
	mousePos = {x: evt.clientX, y: evt.clientY };
}
function handleMouseDown(evt) {
	
    if (!playingAnimation && gameCountdown === 0) {
        bcount = 0;
        for (var i=0; i<myButtons.length; ++i) {
            if (myButtons[i].contains(mousePos)) {
                playerInput.push(bcount);
                myButtons[i].state = true;
                //console.log("sel btn=", i);
                //console.log("i=",i,"sounds[i].onplay=", sounds[i].onplay);
                sounds[i].play();

            }
            bcount += 1;
        }
        checkPlayerInput();
    }
}

function handleMouseUp(evt) {
	
    if (!playingAnimation && gameCountdown === 0) {
        for (var i=0; i<myButtons.length; ++i) {
            myButtons[i].state = false;
        }
    }
    if (playButton.contains(mousePos) && !gameStarted) {
        gameStarted = true;
        score = 0;
        gameCountdown = LOOPDELAY;
 
    }
    if (signalScore) {
        score += 1;
        gameCountdown = LOOPDELAY;
        clearButtons();
        signalScore = false;
    }
   	//console.log("mouseup play", mousePos, playButton.contains(mousePos),gameStarted, signalScore, score);
}

function draw() {
	
	clearCanvas();

	for (var i=0; i<myButtons.length; ++i) {
		myButtons[i].draw();
	}
	if (gameStarted) {
		drawText('scoreArea', "Score : " + score);
	}
	else {
		playButton.draw();
		
		drawText('scoreArea', "Play");
		if (score > 0) {
			drawText('titleArea', "Final Score : " + score);
		}
		else {
			drawText('titleArea', "Press Play to Start");
		}
	}
	if (playingAnimation || gameCountdown > 0) {
		drawText('titleArea', "Watch");
	}
	if (!playingAnimation && gameCountdown === 0) {
		drawText('titleArea', "Now You");
	}
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
	sprites["redunlit"] = loadSprite("images/redunlit.png");
	sprites["greenunlit"] = loadSprite("images/greenunlit.png");
	sprites["blueunlit"] = loadSprite("images/blueunlit.png");
	sprites["yellowunlit"] = loadSprite("images/yellowunlit.png");
	sprites["redlit"] = loadSprite("images/redlit.png");
	sprites["greenlit"] = loadSprite("images/greenlit.png");
	sprites["bluelit"] = loadSprite("images/bluelit.png");
	sprites["yellowlit"] = loadSprite("images/yellowlit.png");
	sprites["play"] = loadSprite("images/play.png");
	// load sounds
	sounds.push(new Sound("sounds/60.ogg"));
	sounds.push(new Sound("sounds/62.ogg"));
	sounds.push(new Sound("sounds/64.ogg"));
	sounds.push(new Sound("sounds/65.ogg"));

}
function assetLoadingLoop() {
    if (spritesStillLoading > 0)
        window.requestAnimationFrame(assetLoadingLoop);
    else {
        initialize();
        mainLoop();
    }
}
function handleInput() {

}
    
function initialize() {
	// button init
	playButton = new Sprite(sprites["play"], { x : 400, y : 540 });
	myButtons.push(new Button('red'));
	myButtons.push(new Button('green'));
	myButtons.push(new Button('blue'));
	myButtons.push(new Button('yellow'));
	// mouse initialize
    document.onmousedown = handleMouseDown;
    document.onmouseup = handleMouseUp;
    document.onmousemove = handleMouseMove;
    
	canvas.style.cursor = "default";

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

