# Minecraft Modding en utilisant Forge

## Instructions pour démarrer rapidement

Vous aurez besoin de downloader et d'installer les deux composants suivants :

* [JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
* Modding Kit (Un des  suivants, en fonction de votre machine)
    * [Modkit pour Mac](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/12742874198/1)
    * [Modkit pour Windows - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622594726/1)
    * [Modkit pour Windows - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622936096/1)
    * [Modkit pour Linux - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383845499/1)
    * [Modkit pour Linux - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383939033/1)

Vous pouvez maintenant suivre les [tutoriels](http://www.youtube.com/embed/QkPq6KUvY7g?list=PLX8CzqL3ArzVET0IIHcCf3-JfzY8RL4xG).

## Instructions pour faire du modding !

### Instructions Génerales

* Pour ouvrir une classe, aller sur le menu "Navigate" et clicker sur "Open Type" (raccourci clavier : `Ctrl + Shift + T`). Vous pouvez à present chercher n'importe quelle classe.
* Losrque vous changez un item ou un block dans le code, effacez sa mention et appuyez sur `Ctrl + Espace` pour faire apparaitre la liste des blocks/Items disponibles.

### 1. Explosions TNT géantes !

**But**: Rendre les explosions de la TNT plus grande.

**Instructions**: 

* A la ligne 91 de la class EntityTNTPrimed, il y a une instruction disant `float f = 4.0F;`. Changer le `4.0` par ce que vous voulez. Plus le nombre est grand plus l'explosion est grande. 

**Gameplay**: 

* Appuyer sur `E` pour ouvrir l'inventaire. Clicker sur la boussole dans le coin en haut à droite. Cela ouvre la fenetre de recherche.
* Rechercher "TNT", ensuite, placer là dans la barre en base de l'écran en cliquant sur la TNT puis sur une des boites de la barre. Rechercher ensuite le briquet et mettez le à coté de la TNT. Appuyez sur `Escape` pour quitter l'inventaire. 
* Appuyez sur le chiffre correspondant à la boite contenant la TNT pour la selectionner. Pointer vers le sol avec la souris et faire un click droit pour placer la TNT. Selectionnez le briquet et faire un click droit sur la TNT pour l'allumer. L'explosion se produit après 4 secondes.

### 2. Les Zombies lachent des diamants
**But**: Faire en sorte que les zombies laissent des diamants quand ils sont tués.

**Instructions**: 

* A la ligne 335 de la class EntityZombie, on lit `return Item.rottenFlesh.itemID;`. Changer `rottenFlesh` par `diamond`, ou par n'importe quel item. Vous pouvez appuyez sur `Ctrl + Space` pour faire apparaitre la liste des items.

**Gameplay**: 

* Ouvrez l'inventaire et allez à la recherche.
* Recherchez une épée de diamant et mettez là dans la barre en bas. Ensuite, recherchez un "Oeuf de Zombie" et mettez le à coté de l'épée. Quittez l'inventaire.
* Selectionnez l'oeuf de zombie et faites un click droit sur le sol pour faire apparaitre un zombie. Selectionnez votre épée et clickez sur le zombie jusqu'à ce qu'il meurt. S'il ne laisse rien, faites en apparaitre d'autres et tuez les tous. L'un d'entre eux devrait laisser l'item que vous avez choisi.

### 3. Les Golems des neiges produisent de la glace

**But**: Faire en sorte que les snow golems produisent de la glace derrière eux partout où ils vont.

**Instructions**: 

* Ligne 78 dans la class EntitySnowman, on lit `this.worldObj.setBlock(j, k, l, Block.snow.blockID);`. Changer le `snow` to `ice`, or le block que vous voulez. Ensuite changer le `k` en `k - 1`. Vous pouvez faire `Ctrl + Space` pour voir la liste des blocks. 
* Ligne 76, On lit `if (this.worldObj.getBlockId(j, k, l) == 0 && this.worldObj.getBiomeGenForCoords(j, l).getFloatTemperature() < 0.8F && 
Block.snow.canPlaceBlockAt(this.worldObj, j, k, l))`. Changer le `0.8F` en `100.0F`. Cela sert à être sur que le golem des neiges peut poser la glace n'importe où.
* Changer le `Block.snow.canPlaceBlockAt` en `Block.ice.canPlaceBlockAt`, ou à la place de ice, le block que vous avez choisi.
* Ligne 65, changer la valeur de temperature de 1.0F à 100.0F - Ceci permet d'être sur que le golem des neiges survit dans tous les environnements, même les plus chauds.

**Gameplay**: 

* Ouvrez l'inventaire et recherchez "Neige". Il y en a deux mais celui qui nous interesse est le plus gros, pas celui qui est tout plat.
* Ensuite, recherchez une "Citrouille".
* Placer deux Neige l'une sur l'autre sur le sol, puis la citrouille par dessus. Cela va faire apparaitre un golem des neiges, qui fera apparaitre le block specifié sous lui.

### 4. Les sorcières font meuh

**But**: Faire faire meuh aux sorcières.

**Instructions**: 

* Ligne 65 dans la class EntityWitch, on lit `return "mob.witch.idle";`. Changez `mob.witch.idle` en `mob.cow.say`. Cela transforme le son que fait la sorcière en vie en celui de la vache.
* Line 75 de la class EntityWitch, on lit `return "mob.witch.hurt";`, qui est le son que fait la sorcière quand elle est blessée. Changez `mob.witch.hurt` en `mob.cow.hurt`. Cela transforme le son de la sorcière blessée en celui de la vache.
* Line 83 de la class EntityWitch, on lit `return "mob.witch.death";`. Changez `mob.witch.death` en `mob.cow.hurt`, parce que le son de la vache qui meurt est le même que celui de la vache blessée. Cela transforme le son de la sorcière qui meurt en celui de la vache blessée.

**Gameplay**: 

* Ouvrir l'inventaire et cherchez un oeuf de sorcière.
* Faire apparaitre la sorcière. Elle devrait faire un bruit de vache. Frappez là et elle devrait faire un autre son de vache, y compris quand elle meurt.

### 5. Nouvelles recettes de cuisson

**Purpose**: Ajouter une recette de cuisson au jeu

**Instructions**: 

* Ligne 50 de la class FurnaceRecipes, on lit `this.addSmelting(Block.oreNetherQuartz.blockID, new ItemStack(Item.netherQuartz), 0.2F);`. Copier ceci sur la ligne suivante. 
* Changez le `Block.oreNetherQuartz.blockID` en `Block.dirt.blockID`. Cela permet de dire que l'item à cuisinez est un block de Terre.
* Changez le `Item.netheQuartz` en `Item.diamond`. Cela transfome l'item reçu après cuisson en un diamant.

A Noter: vous pouvez changer `dirt` et `diamond` en n'importe quel item/block de votre choix. Pour que le résultat de la cuisson soit un block, changez la partie `Item` en `Block`, et vice versa. Si vous voulez que le résultat de la cuissont soit un lingot d'or ou n'importe quel autre item, il faut écrire `Item.goldIngot.itemID`, ou l'item que vous souhaitez. Vous pouvez appuyer sur `Ctrl + Space` pour faire apparaitre la liste des blocks/items.

**Gameplay**: 

* Ouvrez votre inventaire et récuperez un "Four".
* Ensuite récuperez un  "Charbon" and et l'item/block que vous avez defini comme item à cuisiner.
* Placer le four sur le sol et faites un click droit pour l'ouvrir.
* Placer l'item/block à cuisiner sur l'espace en haut à gauche
* Placer le charbon dans l'espace en bas à droite pour le bruler. Votre item va immediatement être cuisiné.
* Après 10 secondes, le premier item va être cuisiné pour donner le second.

### 6. Des fours plus rapides

**But**: Cuisiner les items plus vite grâce à des fours plus rapides.

**Instructions**: 

* Dans la class TileEntityFurnace, faites `Ctrl + F` si vous utilisez Windows ou `Command + F` sur un mac afin d'ouvrir une fenetre de recherche (Find window). Mettre "200" dans la boite intitulé "Find". Clickez sur le bouton find en bas de la fenêtre.
* Trouvez les 3 premiers "200", et les changer en "1". NE PAS CHANGER les autres "200" après les 3 premiers !

**Gameplay**: 

* Recuperez un four dans votre inventaire.
* Récuperez un charbon et un item à cuisiner du mod précedent.
* Placer le four sur le sol et faites un click droit pour l'ouvrir.
* Placer l'item/block à cuisiner sur l'espace en haut à gauche
* Placer le charbon dans l'espace en bas à droite pour le bruler. Votre item va immediatement être cuisiné.
* Après 1/20 de seconde, l'item sera cuisiné. C'est 200 fois plus rapide qu'avant !

### 7. Nouvelles recettes de fabrication (crafting)

**But**: Créer de nouvelles recettes.

**Instructions**: 

* Ligne 29 de la class RecipesCrafting, on lit `par1CraftingManager.addRecipe(new ItemStack(Block.netherBrick, 1), new Object[] {"NN", "NN", 'N', Item.netherrackBrick});`. Recopier la ligne sur la ligne suivante.
* Changez `Block.netherBrick, 1` en `Item.diamond, 8`. Le résultat de la recette de fabrication sera 8 diamants.
* Remplacez `"NN", "NN"` par `"DS", "SD"`, ou par les lettres de votre choix. par example, mettre `"DDD", "DFD", "DDD"` donne :

D D D<br/>
D F D<br/>
D D D

* Précisez l'item representé par chaque lettre en changeant `'N', Item.netherrackBrick` en `'Letter', "Item/Block"`. Par exemple, si le code est `par1CraftingManager.addRecipe(new ItemStack(Item.diamond, 8), new Object[] {"DS", "SD", 'S', Block.sand, 'D', Block.dirt});`, alors la recette sera :

DIRT SAND<br/>
SAND DIRT

et elle produira 8 diamants.

Vous pouvez changer les items et les blocks en n'importe quel item ou block que vous souhaitez. Pour que le résultat de la recette soit un block, changer la partie `Item` en `Block`, et vice versa.  Si vous voulez que le résultat de la cuissont soit un lingot d'or ou n'importe quel autre item, il faut écrire `Item.goldIngot.itemID`, ou l'item que vous souhaitez. Vous pouvez appuyer sur `Ctrl + Space` pour faire apparaitre la liste des blocks/items. Vous pouvez également changer la disposition des items dans la recette en ce que vous souhaitez mais cela ne peut pas être plus grand que 3x3.

**Gameplay**: 

* Ouvrez votre inventaire et récuperez un Etabli
* Prenez ensuite les items/blocks qui font partie de votre recette mais pas le résultat de celle-ci.
* Placez l'établi sur le sol et faites un click droit pour l'ouvrir.
* Placer les items dans l'établi en respectant la disposition que vous avez specifié.
* Un nouvel item va apparaitre dans l'emplacement à droite. Récuperez le, cela doit être l'item que vous avez specifié dans le code.

### 8. Cochons volants!

**But**: Faire voler les cochons dans les airs!

**Instructions**: 

* Ligne 265 dans la class EntityPig, tapez le code suivant:

		public void fly() {
			double howMuchY = this.posY - this.lastTickPosY;
			this.posY = this.posY + howMuchY;
		}

		public void onLivingUpdate() {
			fly();
		}
* Ligne 225 dans la class EntityPig, on lit:

		protected void fall(float par1)
    		{
        		super.fall(par1);

        		if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
        		{
            		((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
        		}
    		}

Enlever la partie qui dit:

        		super.fall(par1);

        		if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
        		{
            		((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
        		}

Il faut enlever ce code pour être sur que le cochon ne reçoit pas de dégats dans les airs. Si on ne l'enleve pas, le cochon va mourir au bout d'un moment à cause d'un bug qui lui fait prendre des dégats de chute.

**Gameplay**: 

* Ouvrez votre inventaire et récuperez un "Oeuf de cochon" et de la "Terre".
* Faites une grande tour de Terre et mettez un cochon tout en haut.
* Detruisez la tour de Terre en cliquant dessus. Le cochon doit flotter dans les airs!

Afin de construire facilement la tour de Terre, vous pouvez volez en tapant `Espace` deux fois de suite très rapidement. Cela vous fera voler. Vous pouvez garder `Espace` enfoncé pour aller vers le haut et `Shift` pour aller vers le bas. Tapez deux fois rapidement sur `Espace` encore une fois pour arreter de voler.

### 9. Fleche avec projection

**But** Lorsque l'on tire sur un ennemi avec une flêche, celui-ci est projeté

**Instructions**:
Dans la classe EntityArrow, à la ligne 559 on lit :`knockBackStrength = par1;` 
Rajouter une valeur pour augmenter la force de projection d'une flêche : `knockBackStrength = par1 + 100;`. Plus la valeur rajouter est grande plus le personnage qui recevra la flêche sera projeté loin.

**Gameplay**

* Dans l'inventaire selectionnez l'arc et les flêches.
* Faire apparaitre un personnage (villageois, Golem, Zombie ou autre...)
* Selectionnez l'arc, faire un click droit pour tirer avec l'arc sur le personnage
* Celui-ci est projeté très loin !

### 10. Les golems de neige tirent des oeufs !

**But** Losrqu'un golem de neige attaque, il tire des oeufs à la place des boules de neiges.

**Instructions**:
Dans la class EntitySnowman chercher la méthode attackEntityWithRangedAttack et dans celle-ci remplacer la ligne : 
`EntitySnowball entitySnowball = new EntitySnowball(this.worldObj, this);` par
`EntityEgg entitysnowball = new EntityEgg(this.worldObj, this);`

**Gameplay**

* Construire un Golem des neiges
* Faire apparaitre un Zombie (avec un oeuf de zombie) non loin du golem pour que celui-ci attaque le zombie.
* Le golem des neiges tire des oeufs sur le zombie.

### 11. Modifier la vitesse des golems

**But** Faire bouger les golems très vite.

**Instructions**:
Pour modifier la vitesse d'un Golem de Fer ouvrir la classe EntityIronGolem. Pour modifier la vitesse d'un Golem des neiges ouvrir la classe EntitySnowman. Le principe est le même pour les deux golems.
Dans la classe que vous avez ouverte, cherchez `SharedMonsterAttributes.movementSpeed`. Augmentez la valuer contenue dans la méthode `setAttribute` pour augmenter la vitesse du golem. (Essayez en passant de 0.25 à 1.25 donne déjà des résultats amusants). 

**Gameplay**

* Construire un Golem des neiges/Golem de fer
* Faire apparaitre un Zombie (avec un oeuf de zombie) assez loin du golem pour que celui-ci se déplace vers le zombie.
* Le golem va aller très vite vers le zombie.

**Astuce**
Cette modification est à combiner avec la modification #3 pour obtenir une patinoire géante produite par un Golem des Neiges !

### 12. Modifier la vie des golems

**But** Rendre les golems quasi invincibles

**Instructions**:
Pour modifier la vie d'un Golem de Fer ouvrir la classe EntityIronGolem. Pour modifier la vie d'un Golem des neiges ouvrir la classe EntitySnowman. Le principe est le même pour les deux golems.
Dans la classe que vous avez ouverte, cherchez `SharedMonsterAttributes.maxHealth`. Augmentez la valuer contenue dans la méthode `setAttribute` pour augmenter la vie du golem. (Essayer en mettant la valeur à 1000 le rend presque invulnérable). 

**Gameplay**

* Construire un Golem des neiges/Golem de fer
* Essayez de le tuer avec la meilleur épée est quasi impossible... 

D'ou la modification suivante :

### 13. Réaliser une épée surpuissante

**But** Pouvoir tuer le golem crée avec la modification #12 :) 

**Instructions**
Ouvrir la class ItemSword. A la ligne 27 on lit : 
`this.weaponDamage = 4.0F + par2EnumToolMaterial.getDamageVsEntity();` 
Remplacer le 4.0 par une valeur plus elevée (aux alentours de 1000). 

**Gameplay**
* Ouvrir l'inventaire et chercher une épée. Notez que les dégats de l'épée sont très élévés et correspondent a la valeur que l'on a mise.
* Créez un golem de fer ou des neiges et tuez le avec l'épée. Vous n'aurez besoin que d'un coup ! 
* Créez des zombies et tuez les en un coup grâce à votre super épée !


## Instructions detaillées

Cette partie ne concerne que ceux qui veulent aller plus loin et construire leur propre modding kit.En général,les mod kits pré-construits (comme expliqué au-dessus) sont suffisants. Créer un mod kits peut être un travail plutôt important et peut nécessiter de bien comprendre comment fonctionne les scripts de builds.
Si tout ça ne vous fait pas peur, alors voici les instructions :

Download Src bundle from (files.minecraftforge.net). As of Jan 1, 2014 [1.6.4-Recommended](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.6.4-9.11.1.965/forge-1.6.4-9.11.1.965-src.zip) and [1.7.2-Latest](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.2-10.12.0.982/forge-1.7.2-10.12.0.982-src.zip) bundles are available. 1.7.x are not recommended as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/27#issuecomment-31436639).

* For 1.6.4 (recommended)
    * Unzip the downloaded bundle
    * Change directory to "forge"
    * Give the command `install.sh` (on Mac) or `install.cmd` (on Windows) to configure Forge for modding.
* For 1.7.2 (not recommended)
    * Give the command `./gradlew setupDevWorkspace --refresh-dependencies`

      On Mac, you may encounter [ForgeGradle#34](https://github.com/MinecraftForge/ForgeGradle/issues/34) and will have to manually edit `build/unpacked/dev.json` as [explained here](https://github.com/MinecraftForge/ForgeGradle/issues/34#issuecomment-31344841). And then give `./gradlew setupDecomWorkspace`
    * `./gradlew eclipse` to generate Eclipse specific project. You will have to manually edit `dev.json` once again.
