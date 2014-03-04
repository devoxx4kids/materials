# Minecraft Modding using Forge

## Quick Start Instructions

You need to download/install only the following two components:

* [JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
* Modding Kit (one of the following based upon your platform)
    * [Modkit for Mac](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/12742874198/1)
    * [Modkit for Windows - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622594726/1)
    * [Modkit for Windows - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622936096/1)

That's it, now follow the [tutorials](http://www.youtube.com/embed/QkPq6KUvY7g?list=PLX8CzqL3ArzVET0IIHcCf3-JfzY8RL4xG).

## Modding Instructions

### General Instructions

* To go to a class, go to the Navigate menu and click on Open Type. From there, you can search for any class in the source code.
* When changing an item or block, delete the current item/block and press `Ctrl + Space` to pull up a list of items and blocks that are availible.

### 1. Bigger TNT explosions

**Purpose**: To make TNT explosions larger.

**Instructions**: 

* On line 91 in the class EntityTNTPrimed, there is a statement saying `float f = 4.0F;`. Change the `4.0` to whatever number you want. The bigger the number, the 

bigger the explosion.

**Gameplay**: 

* Press `E` to open your inventory. Then, click on the compass icon on the top right corner. This will bring you to a search box.
* Search for "TNT", then put it in the bar on the bottom by clicking on the TNT then clicking on one of the boxes on the bar. Then search for "Flint and Steel", and put it next to the TNT. Press `Escape` to exit your inventory. 
* Press the number corresponding to the box with the TNT in it to select it. Point at the ground with your mouse and right-click to place the TNT. Then select the Flint and Steel and right-click on the TNT to light it. It should make an explosion after four seconds.

### 2. Zombies drop diamonds
**Purpose**: To make zombies drop diamonds when killed.

**Instructions**: 

* On line 335 in the class EntityZombie, there is a statement saying `return Item.rottenFlesh.itemID;`. Change the `rottenFlesh` to `diamond`, or whatever item you
want. Remember that you can press `Ctrl + Space` to pull up a list of items.

**Gameplay**: 

* Open your inventory and go to the search box.
* Search for a "Diamond Sword", then put it in the bar on the bottom. Then search for a "Spawn Zombie", and put it next to the sword. Exit your inventory.
* Select the Spawn Zombie and right-click on the ground to spawn a zombie. Select your sword and left click on the zombie until it dies. If it doesn't drop anything, then spawn some more and kill them too. One of them should drop  the item you specified.

### 3. Snow golems make ice

**Purpose**: To make snow golems place ice underneath them wherever they go.

**Instructions**: 

* On line 78 in the class EntitySnowman, there is a statement saying `this.worldObj.setBlock(j, k, l, Block.snow.blockID);`. Change the `snow` to `ice`, or whatever block you want. Then change the `k` to `k - 1`. Remember that you can press `Ctrl + Space` to pull up a list of blocks. 
* On line 76, it says `if (this.worldObj.getBlockId(j, k, l) == 0 && this.worldObj.getBiomeGenForCoords(j, l).getFloatTemperature() < 0.8F && 
Block.snow.canPlaceBlockAt(this.worldObj, j, k, l))`. Change the `0.8F` to `100.0F`. This makes sure the snow golem can place ice in any biome.
* Change the `Block.snow.canPlaceBlockAt` to `Block.ice.canPlaceBlockAt`, or instead of ice, the block you specified.
* On line 65, change the temperature value from 1.0F to 100.0F - This makes sure your snow golem doesn't die in biomes that are too hot.

**Gameplay**: 

* Open your inventory and search for "Snow". There will be two Snows, but you want the bigger one, not the flat-looking one.
* Then, search for a "Pumpkin".
* Place a Snow on top of another one, then put a Pumpkin on top. This will spawn a snow golem, which will place the block you specified underneath it.

### 4. Witches say moo

**Purpose**: To make witches make cow sounds.

**Instructions**: 

* On line 65 in the class EntityWitch, there is a line saying `return "mob.witch.idle";`. Change `mob.witch.idle` to `mob.cow.say`. This makes the witch's living sound to that of a cow.
* On line 75 in the class EntityWitch, it says `return "mob.witch.hurt";`, which is the witch's sound it makes when hurt. Change `mob.witch.hurt` to `mob.cow.hurt`. This makes the witch's living sound to that of a cow.
* On line 83 in the class EntityWitch, there is a line saying `return "mob.witch.death";`. Change `mob.witch.death` to `mob.cow.hurt`, because cows' death sound is the same as their hurt sound. This makes the witch's death sound to the hurt sound of a cow.

**Gameplay**: 

* Open your inventory and get a "Spawn Witch".
* Spawn the witch. It should make a cow sound. Hit it, and it should make a different cow sound. When it dies, it will make a cow sound too.

### 5. New smelting recipe

**Purpose**: To add a new smelting recipe.

**Instructions**: 

* On line 50 in the class FurnaceRecipes, it says `this.addSmelting(Block.oreNetherQuartz.blockID, new ItemStack(Item.netherQuartz), 0.2F);`. Copy this onto the next line. 
* Change the `Block.oreNetherQuartz.blockID` to `Block.dirt.blockID`. This makes the item you want to smelt to a dirt block.
* Change the `Item.netheQuartz` to `Item.diamond`. This makes the item you get from smelting the dirt to a diamond.

Note that you can change the `dirt` and `diamond` to whatever item/block you want. To make the result of smelting a block, change the `Item` part to `Block`, and vice versa. If you want to make the item to smelt a gold ingot, or any other item, make it `Item.goldIngot.itemID`, or whatever item you want. Remember that you can press `Ctrl + Space` to pull up a list of blocks/items.

**Gameplay**: 

* Open your inventory and get out a "Furnace".
* Then get out a "Coal" and whatever item/block you put as the item to smelt.
* Place the Furnace on the ground, then right-click on it to open it.
* Place the item to smelt in the top-left slot.
* Place the Coal in the bottom-right slot to act as fuel. Your item will immediately start smelting.
* After 10 seconds, the first item will be smelted into the second.

### 6. Faster furnaces
<!-- Alliteration! -->

**Purpose**: To make furnaces smelt items faster.

**Instructions**: 

* In the class TileEntityFurnace, do `Ctrl + F` if you are on a Windows computer or `Command + F` to open a Find window. Put "200" into the box that says "Find". Then click on The "Find" button on the bottom of the window.
* Find the first three "200"s, and change them to "1". DO NOT change any "200"s besides the first three.

**Gameplay**: 

* Open your inventory and get out a "Furnace".
* Then get out a "Coal" and whatever item/block you put as the item to smelt in the last mod.
* Place the Furnace on the ground, then right-click on it to open it.
* Place the item to smelt in the top-left slot.
* Place the Coal in the bottom-right slot to act as fuel. Your item will immediately start smelting.
* After 1/20 of a second, the item will be smelted. This is 200 times faster than it was before!

### 7. New crafting recipe

**Purpose**: To create a new recipe.

**Instructions**: 

* On line 29 in the class RecipesCrafting, it says `par1CraftingManager.addRecipe(new ItemStack(Block.netherBrick, 1), new Object[] {"NN", "NN", 'N', Item.netherrackBrick});`. Copy this onto the next line.
* Change the `Block.netherBrick, 1` to `Item.diamond, 8`. This makes the result of the crafting recipe 8 diamonds.
* Change the `"NN", "NN"` to `"DS", "SD"`, or to whatever pattern you want. For example, putting in `"DDD", "DFD", "DDD"` gives:

D D D<br/>
D F D<br/>
D D D

* Specify the item represented by each letter by changing `'N', Item.netherrackBrick` to `'Letter', "Item/Block"`. For example, if the code is `par1CraftingManager.addRecipe(new ItemStack(Item.diamond, 8), new Object[] {"DS", "SD", 'S', Block.sand, 'D', Block.dirt});`, then the recipe would be:

DIRT SAND<br/>
SAND DIRT

and it would give you 8 diamonds.

Note that you can change the items/blocks to whatever items and blocks you want. To make the result of smelting a block, change the `Item` part to `Block`, and vice versa. If you want to make the item to smelt a gold ingot, or any other item, make it `Item.goldIngot.itemID`, or whatever item you want. Remember that you can press `Ctrl + Space` to pull up a list of blocks/items. You can also change the patter of the items to whatever you want, but it can't be bigger that 3x3.

**Gameplay**: 

* Open your inventory and get out a "Crafting Table".
* Then get out the items that are in your crafting recipe, except for the resulting item.
* Place the Crafting Table on the ground, then right-click on it to open it.
* Place the items you have in the crafting table in the pattern you specified.
* In the slot on the right side, there will be a new item. Take this out. It should be the item you specified in the code.

### 8. Flying pigs!

**Purpose**: To make pigs "fly" (hover) in the air.

**Instructions**: 

* On line 265 in the class EntityPig, type in:

		public void fly() {
			double howMuchY = this.posY - this.lastTickPosY;
			this.posY = this.posY + howMuchY;
		}

		public void onLivingUpdate() {
			fly();
		}
* On line 225 in the class EntityPig, it says:

		protected void fall(float par1)
    		{
        		super.fall(par1);

        		if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
        		{
            		((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
        		}
    		}

Get rid of the part that says:

        		super.fall(par1);

        		if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
        		{
            		((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
        		}

This makes sure the pig doesn't take fall damage while in the air. Without deleting this part, the pig would die after a while due to a glitch where the pig takes fall damage.

**Gameplay**: 

* Open your inventory and get out a "Spawn Pig" and some "Dirt".
* Make a tall tower of Dirt and spawn a pig on top of it.
* Destroy the tower of Dirt by left-clicking on the dirt. The pig should float in the air.

Note that to help you make the tower of dirt, you can fly by tapping `Space` twice in rapid succession. This will make you fly. You can hold `Space` to go up and `Shift` to go down. Double-tap `Space` again to stop flying.

## Detailed Instructions

You only need to follow these instructions if you are planning to build your own modding kit. Generally the pre-built mod kits (as explained in Quick Start above) 
would work. Building mod kits could be a significant work and may require significant understanding of the build scripts.

If you are ready to dare, then follow the instructions:

Download Src bundle from (files.minecraftforge.net). As of Jan 1, 2014 [1.6.4-Recommended](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.6.4-
9.11.1.965/forge-1.6.4-9.11.1.965-src.zip) and [1.7.2-Latest](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.2-10.12.0.982/forge-1.7.2-10.12.0.982

-src.zip) bundles are available. 1.7.x are not recommended as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/27#issuecomment-31436639).

* For 1.6.4 (recommended)
    * Unzip the downloaded bundle
    * Change directory to "forge"
    * Give the command `install.sh` (on Mac) or `install.cmd` (on Windows) to configure Forge for modding.
* For 1.7.2 (not recommended)
    * Give the command `./gradlew setupDevWorkspace --refresh-dependencies`

      On Mac, you may encounter [ForgeGradle#34](https://github.com/MinecraftForge/ForgeGradle/issues/34) and will have to manually edit `build/unpacked/dev.json` as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/34#issuecomment-31344841). And then give `./gradlew setupDecomWorkspace`
    * `./gradlew eclipse` to generate Eclipse specific project. You will have to manually edit `dev.json` once again.

