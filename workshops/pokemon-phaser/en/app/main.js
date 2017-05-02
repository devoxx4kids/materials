// Initialize Phaser, and create a 1280x800px game
var screenWidth = 1280;
var screenHeight = 800;
var game = new Phaser.Game(screenWidth, screenHeight, Phaser.CANVAS, 'gameContainer');

var updatesCounter = 0;
var caughtPokemons = 0;
var text = null;

// Create our 'main' state that will contain the game
var mainState = {

    preload: function() {
    	game.load.crossOrigin = 'anonymous';
      	
      	// Load all needed images
      	game.load.image('background', 'http://d4k.wwilk.com/assets/background.jpg');
      	game.load.image('pokemon', 'http://d4k.wwilk.com/assets/pikachu.png');
    },

    create: function() {
      	// Set the background image
    	game.add.tileSprite(0, 0, screenWidth, screenHeight, 'background');  
    	// Set the physics system
     	game.physics.startSystem(Phaser.Physics.ARCADE);
     
     	// Create text container and set it to initial value
     	text = game.add.text(0, 0, 'Catch a Pokemon by clicking on it', { fill: '#000000'});
    },
     
    update: function() {
		updatesCounter++;
		// Create pokemon only every 100th call of update function
        if(updatesCounter % 100 == 0){
	     	createPokemon();    
        }
    }

};

function createPokemon() {
	// Select initial x position of the pokemon randomly
 	var horizontalPosition = parseInt(screenWidth * Math.random());
 	var verticalPosition = 0;

    // Display the Pokemon on the screen
    var pokemon = game.add.sprite(horizontalPosition, verticalPosition, 'pokemon');

	// Enables all kind of input actions on this image (click, etc)
    pokemon.inputEnabled = true;
		
	pokemon.events.onInputDown.add(function(){
      	caughtPokemons++;
      	text.text = 'Congratulations, you caught ' + caughtPokemons + ' Pokemon';
      	pokemon.destroy();
    }, this);

    // Add gravity to the pokemon to make it fall
    game.physics.arcade.enable(pokemon);
    pokemon.body.gravity.y = 300;
};


// Add and start the 'main' state to start the game
game.state.add('main', mainState);
game.state.start('main');

