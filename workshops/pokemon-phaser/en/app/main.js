// Initialize Phaser, and create a game
var screenWidth = 1024;
var screenHeight = 768;
var game = new Phaser.Game(screenWidth, screenHeight, Phaser.CANVAS, 'gameContainer');

var updatesCounter = 0;
var caughtPokemons = 0;
// var score = 0;
var message = null;

// Create our 'main' state that will contain the game
var mainState = {

    preload: function() {
	game.load.crossOrigin = 'anonymous';
	loadImages(game);
    },

    create: function() {
      	
      	// Set the background image
    	game.add.tileSprite(0, 0, screenWidth, screenHeight, 'background');  
    	// Set the physics system
     	game.physics.startSystem(Phaser.Physics.ARCADE);
     
     	// Create text container and set it to initial value
     	message = game.add.text(0, 0, 'Catch a Pokemon by clicking on it');
	// message.fill = '#FF0000';
    },
     
    update: function() {
	updatesCounter++;
	// Create pokemon only every 100th call of update function
        if(updatesCounter % 100 == 0) {
		createPokemon();    
	}
	message.text = 'Congratulations, you caught ' + caughtPokemons; // + ' Pokemon. Score: ' + score;
    }

};

function createPokemon() {
	// Select initial x position of the pokemon randomly
 	var horizontalPosition = parseInt(screenWidth * Math.random());
 	var verticalPosition = 0;

	// We already have several pre-defined shapes.
	// 'pikachu', 'kyogre', 'bikkuriman', 'bsquadron1'

	// Display the Pokemon on the screen
	var pokemon = game.add.sprite(horizontalPosition, verticalPosition, 'pikachu');

	// Enables all kind of input actions on this image (click, etc)
	pokemon.inputEnabled = true;
		
	// Do stuff when the mouse is clicked over the Pokemon
	pokemon.events.onInputDown.add(function(){
		caughtPokemons++;
		// score += 100; 
		// score += Math.round(pokemon.body.speed);
		pokemon.destroy();
	}, this);


	// Do stuff when the cursor is hovering over the Pokemon	
	pokemon.events.onInputOver.add(function() {
	
	}, this);

	pokemon.checkWorldBounds = true;
	pokemon.events.onOutOfBounds.add(function() {
		// score = Math.max(0, score-100);
		pokemon.destroy();
	}, this);

	// Add gravity to the pokemon to make it fall
	game.physics.arcade.enable(pokemon);
	pokemon.body.gravity.y = 300;
};


// Add and start the 'main' state to start the game
game.state.add('main', mainState);
game.state.start('main');

