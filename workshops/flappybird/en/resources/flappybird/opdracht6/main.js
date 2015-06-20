// Initialize Phaser, and create a 400x490px game
var game = new Phaser.Game(400, 490, Phaser.AUTO, 'gameDiv');

// Create our 'main' state that will contain the game
var mainState = {

    preload: function() {
      // Change the background color of the game
      game.stage.backgroundColor = '#71c5cf';


      // Load the bird sprite
      game.load.image('bird', 'assets/bird.png');
    },

    create: function() {
      // Set the physics system
     game.physics.startSystem(Phaser.Physics.ARCADE);

     // Create BitmapData
     bird = game.add.bitmapData(50,50);
     pipe = game.add.bitmapData(50,50);

     // Draw bird
     bird.ctx.fillStyle = '#fdf317';
     bird.ctx.strokeStyle = '#000000';
     bird.ctx.beginPath();
     bird.ctx.rect(0, 0, 50, 50);
     bird.ctx.closePath();
     bird.ctx.fill();
     bird.ctx.lineWidth = "6";
     bird.ctx.stroke();

     // Draw pipe
     pipe.ctx.fillStyle = '#40f225';
     pipe.ctx.strokeStyle = '#000000';
     pipe.ctx.beginPath();
     pipe.ctx.rect(0, 0, 50, 50);
     pipe.ctx.closePath();
     pipe.ctx.fill();
     pipe.ctx.lineWidth = "6";
     pipe.ctx.stroke();

     // Display the bird on the screen
     this.bird = this.game.add.sprite(100, 245, bird);

     this.pipes = game.add.group(); // Create a group
     this.pipes.enableBody = true;  // Add physics to the group
     this.pipes.createMultiple(20, pipe); // Create 20 pipes

     // Add gravity to the bird to make it fall
     game.physics.arcade.enable(this.bird);
     this.bird.body.gravity.y = 1000;

     this.timer = game.time.events.loop(1500, this.addRowOfPipes, this);

     // Call the 'jump' function when the spacekey is hit
     var spaceKey = this.game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);
     spaceKey.onDown.add(this.jump, this);


     // Add a score label on the top left of the screen
     this.score = 0;
     this.labelScore = game.add.text(20, 20, "0", { font: "30px Arial", fill: "#ffffff" });


    },

    addOnePipe: function(x, y) {
      // Get the first dead pipe of our group
      var pipe = this.pipes.getFirstDead();

      // Set the new position of the pipe
      pipe.reset(x, y);

      // Add velocity to the pipe to make it move left
      pipe.body.velocity.x = -200;

      // Kill the pipe when it's no longer visible
      pipe.checkWorldBounds = true;
      pipe.outOfBoundsKill = true;
    },

    addRowOfPipes: function() {
      // Pick where the hole will be
      var hole = Math.floor(Math.random() * 5) + 1;

      // Add the 6 pipes
      for (var i = 0; i < 8; i++)
          if (i != hole && i != hole + 1)
              this.addOnePipe(400, i * 60 + 10);
      this.score += 1;
      this.labelScore.text = this.score;  
    },

    update: function() {
      // If the bird is out of the world (too high or too low), call the 'restartGame' function
      if (this.bird.inWorld == false)
          this.restartGame();

      // If the bird overlap any pipes, call 'restartGame'
      game.physics.arcade.overlap(this.bird, this.pipes, this.restartGame, null, this);
      },

    // Make the bird jump
    jump: function() {
      // Add a vertical velocity to the bird
      this.bird.body.velocity.y = -350;
    },

    // Restart the game
    restartGame: function() {
        // Start the 'main' state, which restarts the game
        game.state.start('main');
    }

};

// Add and start the 'main' state to start the game
game.state.add('main', mainState);
game.state.start('main');
