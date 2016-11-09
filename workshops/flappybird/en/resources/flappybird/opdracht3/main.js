// Initialize Phaser, and create a 400x490px game
var game = new Phaser.Game(400, 490, Phaser.AUTO, 'gameDiv');

// Create our 'main' state that will contain the game
var mainState = {

    preload: function() {
        // This function will be executed at the beginning
        // That's where we load the game's assets
    },

    create: function() {
        // This function is called after the preload function
        // Here we set up the game, display sprites, etc.
    },

    update: function() {
        // This function is called 60 times per second
        // It contains the game's logic
    },
};

// Add and start the 'main' state to start the game
game.state.add('main', mainState);
game.state.start('main');  
