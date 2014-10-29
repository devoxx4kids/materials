# Minecraft Modding met Forge

## Snelle Start Instructies

Je moet enkel de volgende twee componenten downloaden en installeren:

* [JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
    * Installeer jdk-7u67 (JDK 1.8 is niet compatibel met Minecraft!)
    * Zet de JAVA_HOME environment variabele op de installatie directory van de net geinstallareerde JDK bv. "C:\Program Files\Java\jdk1.7.0_67"
    * Voeg de paden naar de %JAVA_HOME%\bin en %JAVA_HOME%\jre\bin toe aan de PATH environment variabele.
    * Onder Windows is voor Eclipse ook de 32-bit jre nodig.
* Ontwikkelomgeving
    * Pak de Modding Kit voor jouw systeem uit. In de Modding Kit zit zowel Minecraft Forge als Eclipse (maak een keuze op basis van het besturingssystem dat je gebruikt)
        * [Modkit voor Mac](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/12742874198/1)
        * [Modkit voor Windows - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622594726/1)
        * [Modkit voor Windows - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622936096/1)
        * [Modkit voor Linux - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383845499/1)
        * [Modkit voor Linux - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383939033/1)
    * Eclipse inrichten
        * Eclipse heeft onder Windows een 32-bit jre nodig om op te starten. Voeg in modkit-windows-1.6.4-64bit\eclipse\eclipse.ini volgende 2 regels toe:
            * -vm
            * <pad naar java>\jdk1.7.0_67\jre\bin\server\jvm.dll
        * Open Eclipse. Bij het opstarten zal deze een fout geven omdat een onbekende workspace is opgegeven. Stel de workspace default in op modkit-windows-1.6.4-64bit\forge\mcp\eclipse.
        * Voeg een nieuw project toe
            * File > Import Project > General > Existing projects into workspace
            * Kies modkit-windows-1.6.4-64bit\forge\mcp\eclipse
    * Backup de Minecraft source zodat deze voor elke workshop teruggezet kan worden
        * Kopieer modkit-windows-1.6.4-64bit\forge\mcp\src naar modkit-windows-1.6.4-64bit\backup\src. 
    * Maak snelkoppelingen op je bureaublad zodat alles snel beschikbaar is tijdens de workshop
        * snelkoppeling minecraft-eclipse die verwijst naar modkit-windows-1.6.4-64bit\eclipse\eclipse.exe
        * snelkoppeling minecraft-modkit die verwijst naar de map modkit-windows-1.6.4-64bit
* Vóór elke workshop
    * Overschrijf modkit-windows-1.6.4-64bit\forge\mcp\src met modkit-windows-1.6.4-64bit\backup\src.
    * Start Minecraft vanuit Eclipse 
    * Kies Singleplayer
    * Create New World
    * Game Mode Creative
    * More World Options > World Type: Superflat
    * Kies een naam bv. D4K_denhaag en 'Create New World' 

Dat is alles. Ga nu naar youtube en bekijk de Minecraft [handleidingen](http://www.youtube.com/embed/QkPq6KUvY7g?list=PLX8CzqL3ArzVET0IIHcCf3-JfzY8RL4xG). (Engels gesproken)

## Modding Instructies

### Algemene Instructies

* **Om een klasse te openen**, klik op het menu item `Navigate` en klik op `Open Type`. (Snel toets op Windows `Ctrl + Shift + T` of op Mac `⌘⇧T`.) Vanuit de popup kan je zoeken naar iedere klasse in source code.
* **Om naar een lijn te gaan** in een klasse, klik op het menu item `Navigate` en klik op `Go to Line...`. (Snel toets op Windows `Ctrl + L` of op Mac `⌘L`.)
* **Om te zoeken** in een klasse, klik op het menu item `Edit` en klik op `Find/Replace...`. (Snel toets op Windows `Ctrl + F` of op Mac `⌘F`.)
* Wanneer je een item of blok wilt wijzigen, of het huidige geselecteerde item/blok wilt verwijderen, druk de toetsen op Windows `Ctrl + Space` of op Mac `⌃ + Space` in en kies een andere item of blok uit de getoonde lijst. 

### Opzetten van Eclipse en Minecraft

* Open de eclipse toepassing vanuit de eclipse folder en kies als workspace **'forge/mcp/eclipse'**
* Wacht eventjes tot alle fouten verdwenen zijn in de 'Problems' tab onderaan en druk dan op het groene cirkeltje met de witte driehoek ('run'). Minecraft start nu op.
* Kies **'Single player'** en daarna **'Create New World'**. Geef een naam aan je wereld en klik zolang op de 'Game Mode' knop tot je **'Game Mode Creative'** ziet staan. Klik vervolgens op **'Create New World'**.
* Tussen twee oefeningen door mag je niet vergeten om de wereld  op te slaan (**'Save and Quit to Title'**) en het spel af te sluiten (**'Quit Game'**). Anders riskeer je meerdere keren Minecraft op te starten.


### 1. Grotere TNT explosies

**Doel**: Grotere TNT explosies maken.

**Instructies**: 

* Op regel 96 in de class EntityTNTPrimed, staat een instructie `float f = 4.0F;`. Verander de `4.0` in een getal naar keuze. Hoe hoger het getal, hoe groter de explosie.

**Spel spelen**: 

* Druk op de toets `E` om je voorraad te openen. Vervolgens klik je op het kompas icoon in de rechter bovenhoek. Dit zal een zoek veld openen.
* Zoek naar "TNT", voeg deze toe aan de balk onder in het scherm. Klik op het TNT icoon en vervolgens klik je op een van de vakjes in de balk onder in het scherm. 
* Zoek vervolgens naar "Flint and Steel", en voeg deze toe aan de balk onder in het scherm. Klik op het Flint and Steel icoon en vervolgens klik je op een leeg vakje in de balk onder in het scherm.
* Druk op de `Escape` toets om het voorraad scherm te sluiten.
* Druk nu op het nummer van het vak waar de TNT in de balk zit om hem te selecteren. Wijs naar de grond en met een rechtermuis klik plaats je de TNT op de grond. Selecteer vervolgens het nummer van het vakje waar de Flint and Steel in de balk zit en plaats die naast de TNT. Na vier seconden zul je een gigantische explosie zien.

### 2. Zombies veranderen in diamanten
**Doel**: Om zombies in diamanten te veranderen wanneer ze worden gedood.

**Instructies**: 

* Op regel 335 in de class EntityZombie, staat een instructie `return Item.rottenFlesh.itemID;`. Verander het woord `rottenFlesh` in `diamond`, of een ander item naar keuze. Onthou dat je door `Ctrl + Space` het keuze menu opent met mogelijkheden.

**Spel spelen**: 

* Open je voorraad (toets `E`) en ga naar het zoek veld.
* Zoek naar "Diamond Sword", en plaats het in een vakje van de balk onder in het scherm. Zoek vervolgens naar "Spawn Zombie", en plaats ook deze in een vakje van de balk. Druk op de `Escape` toets om het voorraad scherm te sluiten.
* Kies het nummer dat bij het vakje van Spawn Zombie hoort en vervolgens gebruik je de rechtermuis toets om de zombie op de grond te plaatsen. Kies het nummer van het vakje van het zwaard en gebruik je linkermuis toets om de zombie te doden. Wanneer hij dood gaat zullen er diamanten verschijnen (of andere items als je iets anders in de code hebt geselecteerd)

### 3. Sneeuw golems maken ijs

**Doel**: Om sneeuw golems een spoor van ijs te laten achterlaten wanneer ze gaan lopen.

**Instructies**: 

* Op regel 78 in de class EntitySnowman, staat een instructie `this.worldObj.setBlock(j, k, l, Block.snow.blockID);`. Verander `snow` to `ice`, of welk block je wilt. Vervolgens verander je de `k` naar `k - 1`. Onthou dat je door `Ctrl + Space` het keuze menu opent met mogelijkheden.
* Op regel 76, staat `if (this.worldObj.getBlockId(j, k, l) == 0 && this.worldObj.getBiomeGenForCoords(j, l).getFloatTemperature() < 0.8F && Block.snow.canPlaceBlockAt(this.worldObj, j, k, l))`. Verander de `0.8F` naar `100.0F`. Dit zorgt ervoor dat de sneeuw golem ijs kan achterlaten in elk type landschap.
* Verander `Block.snow.canPlaceBlockAt` naar `Block.ice.canPlaceBlockAt`, of wanneer je geen ijs hebt gekozen, het blok van jouw keuze.
* Op regel 65, verander de temperatuur waarde van 1.0F naar 100.0F - Dit zorgt ervoor dat de sneeuw golem niet sterft in te warme omgevingen.

**Spel spelen**: 

* Open je voorraad (toets `E`) en zoek naar "Snow" en plaats hem in een vakje van je balk. Je zult drie typen Snows vinden, kies de grote vierkanten, niet de platte of de sneeuwbal.
* Vervolgens, zoek op "Pumpkin" en plaats hem in je balk.
* Druk op de `Escape` toets om het voorraad scherm te sluiten.
* Plaats twee sneeuwblokken bovenop elkaar. Doe dit door nummer van het vakje te kiezen en vervolgens plaats je de blokken met je rechtermuis knop. Plaats er vervolgens een Pumpkin bovenop. Na een tijdje zal er een snow golem ontstaan. Wanneer hij gaat lopen zal hij een spoor van ijs (of wat je hebt gekozen in de code) achterlaten.

### 4. Heksen zeggen boe

**Doel**: Om heksen een koeien geluid te laten maken.

**Instructies**: 

* Op regel 67 in de class EntityWitch, staat een instructie `return "mob.witch.idle";`. Verander `mob.witch.idle` naar `mob.cow.say`. Dit zal de heks koe geluiden laten maken zolang ze leeft.
* Op regel 75 in de class EntityWitch, staat `return "mob.witch.hurt";`, dit is het geluid dat de heks maakt wanneer ze wordt verwond. Verander `mob.witch.hurt` naar `mob.cow.hurt`.
* Op regel 83 in de class EntityWitch, staat een instructie `return "mob.witch.death";`. Verander `mob.witch.death` naar `mob.cow.hurt`, omdat het geluid voor een verwonding het zelfde geluid is voor sterven. Nu zal de heks het geluid van de verwonde koe maken wanneer ze sterft.

**Spel spelen**: 

* Open je voorraad (toets `E`) en zoek naar "Spawn Witch" en plaats hem in een vakje van je balk.
* Druk op de `Escape` toets om het voorraad scherm te sluiten.
* Kies het nummer van het vakje van de heks en plaats de heks op de grond. Ze zou nu het geluid van een koe moeten maken. Sla de heks en ze zal het geluid van een gewonde koe maken. Wanneer ze sterft zal ze ook het geluid van een gewonde koe maken.

### 5. Nieuw smelt recept.

**Doel**: Om een nieuw smelt recept toe te voegen.

**Instructies**: 

* Op regel 50 in de class FurnaceRecipes, staat `this.addSmelting(Block.oreNetherQuartz.blockID, new ItemStack(Item.netherQuartz), 0.2F);`. Kopieer deze regel op de volgende regel. 
* Verander `Block.oreNetherQuartz.blockID` naar `Block.dirt.blockID`. Dit zorgt ervoor dat je een aarde blok kunt smelten naar het item dat je bij de volgende stap kiest.
* Verander `Item.netheQuartz` naar `Item.diamond`. Dit zorgt ervoor dat je oven nu diamanten gaat maken uit aarde.

Opmerking: Je kan voor `dirt` en `diamond` natuurlijk andere dingen kiezen. Bijvoorbeeld, `snow` en `bakedPotato`, sneeuw verandert in gebakken aardappel.

**Spel spelen**: 

* Open je voorraad en voeg een "Furnace" toe aan je balk.
* Vervolgens voeg "Coal" toe of een ander item dat je wilt gebruiken om vuur te maken.
* Voeg "Dirt" toe aan je balk. (Of een andere item als je iets anders in de code hebt gekozen)
* Plaats de Furnace op de grond en gebruik de rechtermuis knop om hem te openen.
* Plaats het item, "Dirt", dat je wilt smelten in het vakje linksboven.
* Plaats de "Coal" in het vakje rechtsonder. Deze dient als brandstof voor het process. Er zal direct worden begonnen met het smelten van je item.
* Na 10 seconden, zal het item linksboven smelten naar een diamant. Deze verschijnt in het vakje rechts.

### 6. Ovens smelten sneller.

**Doel**: Om ovens sneller te laten smelten.

**Instructies**: 

* In de class TileEntityFurnace, gebruik de toetsen `Ctrl + F` als je op een windows computer werkt of `⌘F` op een Mac computer, om het zoek venster te openen. Type "200" in het veld waar staat "Find". Druk nu op de knop met de tekst "Find" onder in het zoek venster.
* Zoek de eerste 3 "200"s, en verander deze in "1". VERANDER ER NIET MEER alleen deze eerste 3.

**Spel spelen**: 

* Open je voorraad en voeg een "Furnace" toe aan je balk.
* Vervolgens voeg "Coal" toe of een ander item dat je wilt gebruiken om vuur te maken.
* Voeg "Dirt" toe aan je balk. (Of een andere item als je iets anders in de code hebt gekozen)
* Plaats de Furnace op de grond en gebruik de rechtermuis knop om hem te openen.
* Plaats het item, "Dirt", dat je wilt smelten in het vakje linksboven.
* Plaats de "Coal" in het vakje rechtsonder. Deze dient als brandstof voor het process. Er zal direct worden begonnen met het smelten van je item.
* Na 1/20 seconden, zal het eerste item smelten naar het tweede. Dit is 200 keer sneller dan voorheen.

### 7. Nieuw handwerk recept

**Doel**: Om een nieuw handwerk recept te maken.

**Instructies**: 

* On regel 29 in de class RecipesCrafting, staat de instructie `par1CraftingManager.addRecipe(new ItemStack(Block.netherBrick, 1), new Object[] {"NN", "NN", 'N', Item.netherrackBrick});`. Kopieer deze regel naar de volgende regel.
* Verander `Block.netherBrick, 1` naar `Item.diamond, 8`. Dit zorgt ervoor dat het handwerk recept 8 diamanten maakt.
* Verander `"NN", "NN"` naar `"DS", "SD"`, of een patroon dat je wilt. Bijvoorbeeld, `"DDD", "DFD", "DDD"` maakt:

D D D<br/>
D F D<br/>
D D D

* Geef aan wat de letters betekenen. Verander `'N', Item.netherrackBrick` in `'S', Block.sand, 'D', Block.dirt`. Het recept zal nu worden:

DIRT SAND<br/>
SAND DIRT

en het zal 8 diamanten maken.

Opmerking: Je kan de items/blokken veranderen in iedere items/blokken die je wilt. Om een blok te smelten, verander het `Item` gedeelte naar `Block`, en vice versa. Wanneer je een item wilt smelten naar een goud staaf, of ieder ander item, verander het in `Item.goldIngot.itemID`, of het item dat je wilt. Onthou dat je door `Ctrl + Space` het keuze menu opent met mogelijkheden. Je kan ook het patroon wijzigen naar jouw keuze, maar dit kan niet groter zijn dan 3x3.

**Spel spelen**: 

* Open je voorraad en zoek naar "Crafting Table".
* Vervolgens zoek je de items die in jouw nieuw handwerk recept zitten, behalve het eindresultaat.
* Plaats de Crafting Table op de grond, en gebruik de rechtermuisknop om hem te openen.
* Plaats de items op je Crafting Table volgens het patroon dat jij hebt gekozen.
* Je ziet meteen de 8 diamanten in het rechtervakje verschijnen.

### 8. Vliegende varkens!

**Doel**: Om varkens te laten "vliegen" (zweven) in de lucht.

**Instructies**: 

* Op regel 265 in de class EntityPig, plaats de volgende regels code vlak voor de laatste '}':

		public void fly()
		{
			double howMuchY = this.posY - this.lastTickPosY;
			this.posY = this.posY + howMuchY;
		}

		public void onLivingUpdate()
		{
			fly();
		}
* Op regel 225 in de class EntityPig, staat het volgende:

		protected void fall(float par1)
    	{
        	super.fall(par1);

        	if (par1 > 5.0F && this.riddenByEntity instanceof EntityPlayer)
        	{
            	((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
        	}
    	}

* Haal het volgende stuk code weg:

    	super.fall(par1);

    	if (par1 > 5.0F && this.riddenByEntity instanceof EntityPlayer)
    	{
    		((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
    	}

Dit zorgt ervoor dat varkens geen verwondingen oplopen terwijl ze in de lucht zweven. Zonder deze code weg te halen, zou een varken na verloop van tijd sterven.

**Spel spelen**: 

* Open je voorraad en zoek naar "Spawn Pig" en enkele "Dirt" items en voeg ze toe aan de balk.
* Maak een hoge toren van "Dirt" items en plaats een "Spawn Pig" er bovenop.
* Verwijder de blokken "Dirt" door met je linkermuis knop op de "Dirt" blokken te klikken. Het varken zou nu in de lucht moeten blijven zweven.

Opmerking: Om je toren van "Dirt" makkelijker te maken, kan je vliegen door de `Space` 2 keer snel achter elkaar in te drukken. Dit zal je laten vliegen. Door de `Space` ingedrukt te houden zal je stijgen en met de `Shift` toets zal je dalen. Dubbel klik weer `Space` om te stoppen met vliegen.

### 9. Pijlen die vijanden ver weg slaan.

**Goal** Om vijanden ver weg te slaan waneer ze geraakt worden door een pijl van jou.

**Instructies**:
Op regel 559 in de class EntityArrow, staat de instructie :`knockBackStrength = par1;` 
Voeg een getal toe om het effect van afweren van een pijl te verhogen : `knockBackStrength = par1 + 100;`. Hoe hoger het getal hoe verder de vijand wordt afgeslagen.

**Spel spelen**

* Open je voorraad en zoek naar "Bow" en enkele "Arrow" items en voeg ze toe aan de balk.
* Creëer een vijand (Zombie, Golem...)
* Selecteer de boog, richt en met behulp van een rechtermuisklik schiet je op de vijand.
* Als het goed is, sla je de vijand ver van je af.

### 10. Snow Golem die eieren schiet!

**Goal** Laat een Snow Golem eieren schieten in plaats van sneeuwballen.

**Instructies**:
Op regel 110 in de class EntitySnowman, staat de instructie: `EntitySnowball entitySnowball = new EntitySnowball(this.worldObj, this);` verander dit naar: `EntityEgg entitysnowball = new EntityEgg(this.worldObj, this);`
Druk de toesten "Ctrl + Shift + O" in om de foutmelding te laten verdwijnen.

**Spel spelen**

* Open je voorraad (toets `E`) en zoek naar "Snow" en plaats hem in een vakje van je balk. Je zult drie typen Snows vinden, kies de grote vierkanten, niet de platte.
* Vervolgens, zoek op "Pumpkin" en plaats hem in je balk.
* Druk op de `Escape` toets om het voorraad scherm te sluiten.
* Plaats twee sneeuwblokken bovenop elkaar. Doe dit door nummer van het vakje te kiezen en vervolgens plaats je de blokken met je rechtermuis knop. Plaats er vervolgens een Pumpkin bovenop. Na een tijdje zal er een snow golem ontstaan.
* Creëer een Zombie niet ver van de Snow Golem.
* De Snow Golem zal nu eieren gaan afvoeren op de Zombie.

### 11. Verander de snelheid van de Golem

**Goal** Laat een Golem rennen.

**Instructies**:
 Om de snelheid van een "Iron Golem" aan te passen, open de class EntityIronGolem. Om de snelheid van een "Snow Golem" aan te passen, open de class EntitySnowman. Het maakt niet uit welke je kiest, de wijzigingen zijn voor beide het zelfde.
 Op regel 98 van EntityIronGolem staat: `this.getEntityAttribute(SharedMonsterAttributes.movementSpeed).setAttribute(0.25D);`, verander de waarde 0.25D in een waarde tussen 0.25D en 1.25D voor het gaafste resultaat.
 Op regel 46 van EntitySnowman staat: `this.getEntityAttribute(SharedMonsterAttributes.movementSpeed).setAttribute(0.20000000298023224D);`, verander de waarde 0.20000000298023224D in een waarde tussen 0.25D en 1.25D voor het gaafste resultaat.

**Spel spelen**

* Open je voorraad en zoek de items voor een "Snow Golem" (2 sneeuw blokken en 1 pompoen) of een "Iron Golem" (4 ijzerblokken en 1 pompoen of pompoenlantaarn) en voeg ze toe aan de balk.
* Maak een "Snow Golem" of "Iron Golem" (Een "Iron Golem" maak je door: 4 IJzerblokken in een T-vorm plaatsen, en er dan een Pompoen of Pompoenlantaarn midden op zetten.)
* Creëer een Zombie, niet te dichtbij zodat de golem moet bewegen om dichter bij de Zombie te komen.
* De golem zal super snel naar de zombie rennen om hem aan te vallen.

**Tips**
Combineer deze mod met de mod in opdracht 3 om de golem een gigantische ijsbaan te laten maken!

### 12. Maak de Golem (bijna) onverslaanbaar.

**Goal** Om de Golem bijna onverslaanbaar te maken.

**Instructies**:
Om de "Iron Golem" bijna onverslaanbaar te maken open de class EntityIronGolem. Om de "Snow Golem" bijna onverslaanbaar te maken, open de class EntitySnowman. Het maakt niet uit welke je kiest, de wijzigingen zijn voor beide het zelfde.
Op regel 97 van EntityIronGolem staat: `this.getEntityAttribute(SharedMonsterAttributes.maxHealth).setAttribute(100.0D);`, verander de waarde 100.0D in een hogere waarde. 1000.0D maakt hem praktisch onverslaanbaar.
Op regel 45 van EntitySnowman staat: `this.getEntityAttribute(SharedMonsterAttributes.maxHealth).setAttribute(4.0D);`, verander de waarde 4.0D in een hogere waarde. 1000.0D maakt hem praktisch onverslaanbaar.

**Spel spelen**

* Open je voorraad en zoek de items voor een "Snow Golem" (2 sneeuw blokken en 1 pompoen) of een "Iron Golem" (4 ijzerblokken en 1 pompoen of pompoenlantaarn) en voeg ze toe aan de balk.
* Maak een "Snow Golem" of "Iron Golem" (Een "Iron Golem" maak je door: 4 IJzerblokken in een T-vorm plaatsen, en er dan een Pompoen of Pompoenlantaarn midden op zetten.)
* Probeer hem maar te verslaan met je beste zwaard. Je zult merken dat dit niet zal lukken. 

...vandaar de volgende mod : 

### 13. Het onoverwinnelijke zwaard

**Goal** Geef mij een zwaard waarmee ik een bijna onoverwinnelijke Golem versla. (Zie mod 12)

**Instructies**
Op regel 27 van class ItemSword staat: `this.weaponDamage = 4.0F + par2EnumToolMaterial.getDamageVsEntity();` 
Wijzig 4.0 in een hogere waarde (rond 1000). 

**Spel spelen**
* Open je voorraad en zoek naar een "Sword" en zoek de items voor een "Snow Golem" (2 sneeuw blokken en 1 pompoen) of een "Iron Golem" (4 ijzerblokken en 1 pompoen of pompoenlantaarn) en voeg ze toe aan de balk.
* Maak een "Snow Golem" of "Iron Golem" (Een "Iron Golem" maak je door: 4 IJzerblokken in een T-vorm plaatsen, en er dan een Pompoen of Pompoenlantaarn midden op zetten.)
* Bouw een Golem en probeer deze met je zwaard te verslaan. Dit moet nu heel makkelijk gaan.
* Creëer wat Zombies en versla deze eveneens met je fantastische zwaard.


## Gedetailleerde instructies

Met deze instructies kan je je eigen mods bouwen. Let op, het bouwen van een mod is veel werk en het kan zijn dat je veel moet leren over de gebruikte scripts.

Als je het aandurft, lees dan verder.

Download de source van http://files.minecraftforge.net/. Het is raadzaam om de sources van de [versie 1.6.4](http://adf.ly/673885/http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.6.4-9.11.1.965/forge-1.6.4-9.11.1.965-src.zip) te gebruiken. De [nieuwere 1.7 versies](http://adf.ly/673885/http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.0.1208/forge-1.7.10-10.13.0.1208-src.zip) zijn niet aan te raden omdat ze veel gebruik maken van Gradle, een programma om automatisch software mee te bouwen. Verschillende gebruikers melden dat de meegeleverde scripts niet altijd goed werken. [hier meer informatie](https://github.com/MinecraftForge/ForgeGradle/issues/27#issuecomment-31436639).

Voor versie 1.6.4 (aanbevolen)
Unzip de gedownloade versie
Verander de naam naar “forte”
Voer het `instal.sh` script uit op een Mac of `install.cmd` op Windows om de bestanden te configureren

Voor versie 1.7.x (als je van een uitdaging houdt)
Voer het commando `gradlew setupDevWorkspace --refresh-dependencies` uit
(Op een Mac kan je de volgende foutmelding zien [ForgeGradle#34](https://github.com/MinecraftForge/ForgeGradle/issues/34). Je moet dan zelf het bestand `build/unpacked/dev.json` aanpassen, zoals [hier](https://github.com/MinecraftForge/ForgeGradle/issues/34#issuecomment-31344841) wordt uitgelegd. Vervolgens voer je het commando `./gradlew setupDecomWorkspace` uit.)
De structuur van de source code ziet er ook anders uit dan dat je met deze tutorial gezien hebt. 

Je moet nu zelf uitzoeken hoe je een mod bouwt. Veel succes!
