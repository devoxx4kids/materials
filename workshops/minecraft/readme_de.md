# Minecraft Modding mit Forge

## Schnellstart

Zuerst musst du die folgenden Komponenten herunterladen:

* [JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
* Modding Kit (wähle aus der Liste den zu deinem Betriebssystem passenden Download)
    * [Modkit für Mac](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/12742874198/1)
    * [Modkit für Windows - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622594726/1)
    * [Modkit für Windows - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/14622936096/1)
    * [Modkit für Linux - 32 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383845499/1)
    * [Modkit für Linux - 64 bit](https://delucaconsulting.app.box.com/d4kminecraft/1/1415067806/15383939033/1)

Das war's schon. Schau dir für den Einstieg die [Tutorials](http://www.youtube.com/embed/QkPq6KUvY7g?list=PLX8CzqL3ArzVET0IIHcCf3-JfzY8RL4xG) an.

## Modding-Anleitung

## Grundsätzliches

* Um zu einer Klasse zu springen musst du das _Navigate_-Menü öffnen und dann _Open Type_ auswählen. Dort kannst du nach jeder Klasse suchen.
* Wenn du den aktuell ausgewählten Block/Gegenstand ersetzen willst, dann lösche diesen und drücke `Ctrl + Space` um eine Liste aller verfügbaren Blöcke und Gegenstände anzuzeigen.

### 1. Grössere TNT-Explosionen

**Ziel**: TNT-Explosionen sollen größer werden.

**Anleitung**:

* In Zeile 96 der Klasse EntityTNTPrimed steht `float f = 4.0F;`. Ersetze `4.0` durch eine andere Zahl. Je größer die Zahl desto größer die Explosion.

**Gameplay**:

* Drücke `E` um dein Inventar zu öffnen. Klicke auf den Kompass in der oberen rechten Ecke an.
* Suche nach "TNT" in dem sich öffnenden Eingabefeld. 
* Klicke auf das TNT und zieh es in die untere Leiste.
* Suche jetzt nach "Feuerzeug" und leg es neben dem TNT ab. 
* Drücke `Escape` um das Inventar zu schliessen.
* Um das TNT auszuwählen drücke jetzt die Zahl die dem Slot entspricht in dem du es abgelegt hast. Zeige mit der Maus auf den Boden und führe einen Rechtsklick aus um es abzulegen. 
* Wähle jetzt das Feuerzeug auf die gleiche Art aus und führe einen Rechtsklick auf das TNT aus.
* Nach 4 Sekunden sollte es explodieren.

### 2. Zombies verlieren Diamanten

**Ziel**: Zombies sollen Diamanten verlieren wenn sie erschlagen werden.

**Anleitung**:

* In Zeile 335 der Klasse EntityZombie steht `return Item.rottenFlesh.itemID;`. Ändere `rottenFlesh` zu `diamond`, oder welchen Gegenstand auch immer du willst. Erinnere dich daran, dass du mit `Ctrl + Space` eine Liste aller Gegenstände bekommst.

**Gameplay**

* Öffne dein Inventar und geh zur Suchen-Maske.
* Suche nach "Diamantschwert" und bewege es in die untere Leiste. 
* Suche als nächstes nach "Erschaffe Zombie" und leg es neben dem Schwert ab.
* Verlasse das Inventar.
* Jetzt wählst du "Erschaffe Zombie" aus und machst einen Rechtsklick auf die Stelle an der ein Zombie erscheinen soll. 
* Nimm jetzt das Schwert und führe so lange Linksklicks auf den Zombie aus bis er stirbt. 
* Wiederhole das Ganze bis einer einen Diamanten verliert.

### 3. Schneegolems machen Eis

**Ziel**: Überall wo ein Schneegolem hintritt soll Eis entstehen.

**Anleitung**:

* In Zeile 78 der Klasse EntitySnowman steht  `this.worldObj.setBlock(j, k, l, Block.snow.blockID);`. Ersetze  `snow` durch `ice` oder einen beliebigen anderen Block. Ändere jetzt noch `k` zu `k - 1`. Denk daran, dass du mit `Ctrl + Space` eine Liste der Blöcke anzeigen kannst.
* In Zeile 76 steht `if (this.worldObj.getBlockId(j, k, l) == 0 && this.worldObj.getBiomeGenForCoords(j, l).getFloatTemperature() < 0.8F && 
Block.snow.canPlaceBlockAt(this.worldObj, j, k, l))`. Ersetze `0.8F` durch `100.0F`. Das sorgt dafür, dass der Schneegolem auch wirklich in jedem Biom Eis platzieren kann.
* Ändere jetzt `Block.snow.canPlaceBlockAt` zu `Block.ice.canPlaceBlockAt`. Hast du dich statt _ice_ für einen anderen Block entschieden musst du natürlich diesen verwenden.
* Als nächstes muss noch in Zeile 65 die Temperatur von 1.0F auf 100.0F angehoben werden damit der Golem nicht stirbt wenn er ein Biom betritt das eigentlich zu heiß ist.

**Gameplay**

* Suche in deinem Inventar nach "Schnee". Es gibt zwei Schnee aber du brauchst den Block, nicht den flach aussehenden.
* Suche jetzt nach "Kürbis".
* Staple zwei Schnee übereinander und leg einen Kürbis oben drauf. Daraus entsteht ein Schneegolem der nun eine Spur des von dir ausgewählten Blöcken zieht.

### 4. Muhende Hexen

**Ziel**: Hexen sollen Muhen.

**Anleitung**:

* In Zeile 65 der Klasse EntityWitch gibt es eine Zeile `return "mob.witch.idle";`. Ändere `mob.witch.idle` zu `mob.cow.say`. Dies ändert den Standardton der Hexe zu dem einer Kuh.
* Ändere Zeile 75 der Klasse EntityWitch von `return "mob.witch.hurt";` zu `return "mob.moo.hurt";`. Ab jetzt macht die Hexe "Muh" wenn sie verletzt wird.
* Bleibt noch der Todes-Sound in Zeile 83 der selben Klasse. Hier musst du `return "mob.witch.death";` zu `return "mob.cow.hurt";` ändern. Dies ändert den Todes-Sound der Hexe zu dem einer verletzten Kuh.

**Gameplay**

* Öffne dein Inventar und hol dir "Erschaffe Hexe"
* Lass die Hexe erscheinen. Wenn sie erscheint macht sie einen Kuh-Sound. 
* Wenn du sie schlägst macht sie einen anderen Kuh-Sound und wenn sie stirbt wieder einen anderen.

### 5. Neues Ofen-Rezept

**Ziel**: Ein neues Ofen-Rezept hinzufügen.

**Anleitung**:

* In Zeile 50 der Klasse FurnaceRecipes steht `this.addSmelting(Block.oreNetherQuartz.blockID, new ItemStack(Item.netherQuartz), 0.2F);`. Kopiere diese Zeile in die nächste.
* Ändere `Block.oreNetherQuartz.blockID` zu `Block.dirt.blockID`. Ab jetzt ist Dirt das Ausgangsmaterial für das Rezept.
* Ersetze jetzt `Item.netheQuartz` durch `Item.diamond`. Ab jetzt wird im Ofen aus Dirt ein Diamant.

Anmerkung: Du kannst statt `dirt` oder `diamond` jeden beliebigen Gegenstand oder Block verwenden. Möchtest du statt eines Gegenstands einen Block haben musst du nur `Ìtem` durch `Block` ersetzen. Möchtest du z.B. aus einem Gegenstand ein Golfnugget herstellen musst du nur `Item.diamond` durhc`Item.goldNugget` ersetzen. 
Und denk daran: Mit `Ctrl + Space` kannst du dir eine Liste der verfügbaren Blöcke/Gegenstände anzeigen lassen.

**Gameplay**

* Öffne dein Inventar und hol dir einen Ofen
* Dann hol dir Koble und welchen Gegenstand/Block du als Ausgangsmaterial für das Rezept festgelegt hast (Dirt in diesem Beispiel)
* Platziere den Ofen auf dem Boden und öffne ihn mit einem Rechtsklick.
* Platziere das Ausgangsmaterial im Slot links-oben
* Lege die Kohle in den Slot unten links um den Ofen zu befeuern. 
* Nach 10 Sekunden wird der Ausgangsgegenstand in den Zielgegenstand verwandelt. 

### 6. Schnellerer Ofen

**Ziel**: Öfen sollen Gegenstände schneller herstellen.

**Anleitung**:

* Öffne die Klasse TileEntityFurnace und nutze die Suchfunktion um nach der Zahl "200" zu suchen. Öffne dazu das Suchen-Fenster (`Ctrl + F` unter Windows und `Command + F` unter Mac)  und gib "200" in dem mit "Find" bezeichneten Feld ein. Klicke jetzt den "Find"-Button am unteren Rand.
* Suche die ersten drei "200" und ersetze sie durch "1". __Ändere auf keinen Fall andere "200"-Einträge außer den angegebenen 3!__ 

**Gameplay**

* Öffne dein Inventar und hol dir einen "Ofen"
* Danach brauchst du wieder "Kohle" und den Gegenstand/Block den du im letzten Mod als Ausgangsmaterial festgelegt hast.
* Benutze dein Ausgangsmaterial und die Kohle wie im letzten Beispiel.
* Nach 1/20 Sekunde ist der Gegenstand fertig. 200 mal schneller asl zuvor!

### 7. Neues Crafting-Rezept

**Ziel**: Ein neues Rezept herstellen.

**Anleitung**:

* In Zeile 29 der Klasse RecipesCrafting steht `par1CraftingManager.addRecipe(new ItemStack(Block.netherBrick, 1), new Object[] {"NN", "NN", 'N', Item.netherrackBrick});`. Kopiere diese in die nächste Zeile.
* Ersetze `Block.netherBrick, 1` durch `Item.diamond, 8`. Dies ändert das Ergebnis dieses Rezepts in 8 Diamanten.
* Ändere `"NN", "NN"` in `"DS", "SD"`, oder ein beliebiges anderes Muster. `"DDD", "DFD", "DDD"` würde z.B. folgendes Muster ergeben:

D D D<br/>
D F D<br/>
D D D

* Lege fest welcher Gegenstand durch welchen Buchstaben dargestellt wird indem du `'N', Item.netherrackBrick` zu `'Buchstabe', "Gegenstand/Block"` änderst. Beispiel: `par1CraftingManager.addRecipe(new ItemStack(Item.diamond, 8), new Object[] {"DS", "SD", 'S', Block.sand, 'D', Block.dirt});`
Hier wird dem Sand-Block der Buchstabe 'S' zugewiesen und dem Dirt-Block der Buchstabe 'D'. Mit den Einträgen "DS" und "SD" ergibt sich dann folgendes muster:

DIRT SAND<br/>
SAND DIRT

das Resultat dieses Rezepts sind 8 Diamanten.

Natürlich kannst du auch hier wieder Gegenstände/Blöcke nach deinem Geschmack variieren. Möchtest du z.B. Goldnuggets haben musst du einfach `Item.goldNugget.itemID` einsetzen. Drücke `Ctrl + Space` für eine Liste verfügbarer Gegenstände/Blöcke. 
Du kannst auch das Muster der Gegenstände ändern, allerdings kann es nie größer als 3x3 werden.

**Gameplay**:

* Öffne dein Inventar und besorg dir eine Werkbank.
* Hol dir auch die Bestandteile deines Rezepts, außer dem Gegenstand den du erzeugen möchtest.
* Platziere die Werkbank vor dir auf dem Bodem und öffne sie mit einem Rechtsklick
* Plaziere alle Zutaten in der von dir festgelegten Art
* Im Slot auf der rechten Seite sollte der von dir festgelegte Gegenstand auftauchen.

### 8. Fliegende Schweine!

**Ziel**: Schweine zum Fliegen (Schweben) bringen.

**Anleitung**:

* Gib folgendes in Zeile 265 der Klasse EntityPig ein:

        public void fly() {
            double howMuchY = this.posY - this.lastTickPosY;
            this.posY = this.posY + howMuchY;
        }

        public void onLivingUpdate() {
            fly();
        }
* Ab Zeile 225 in der Klasse EntityPig findest du folgenden Abschnitt:

        protected void fall(float par1)
            {
                super.fall(par1);

                if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
                {
                    ((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
                }
            }

Entferne diesen Teil:

                super.fall(par1);

                if (par1 &gt; 5.0F &amp;&amp; this.riddenByEntity instanceof EntityPlayer)
                {
                    ((EntityPlayer)this.riddenByEntity).triggerAchievement(AchievementList.flyPig);
                }

So sorgst du dafür, dass das Schwein keinen Aufprallschaden erleidet wärend es fliegt. Ohne diesen Teil zu löschen würde das Schwein nach kurzer Zeit wegen eines kleinen Bugs sterben.

### 9. Pfeile die den Gegner zurückwerfen

**Ziel** Gegner zurückwerfen wenn sie von einem Pfeil getroffen werden.

**Anleitung**:

In Zeile 559 der Klasse EntityArrow steht: `knockBackStrength = par1;`
Addiere einen Wert um den knockBack-Effekt (das Zurückwerfen) eines Pfeils (Arrow) zu erhöhen: `knockBackStrength = par1 + 100;`. Je höher der Wert desto weiter wird der Gegner zurückgeworfen.

**Gameplay**

* Wähle Pfeil und Bogen im Inventar aus
* Erschaffe einen Gegner (Zombie, Golem, ...)
* Wähle den Bogen aus und schieße mit einem Rechtsklick auf den Gegener
* Er sollte weit zurückgeworfen werden!

### 10. Schneegolem schiesst Eier!

**Ziel** Schneegolems greifen mit Eiern statt Schneebällen an.

**Anleitung**:

Suche die Methode `attackEntityWithRangedAttack` in der Klasse EntitySnowman und ersetze dort die Zeile `EntitySnowball entitySnowball = new EntitySnowball(this.worldObj, this);` durch `EntityEgg entitysnowball = new EntityEgg(this.worldObj, this);`

**Gameplay**

* Erschaffe einen Schneegolem
* Lass einen Zombie (mit einem Zombie-Ei) nicht weit weg von dem Golem erscheinen damit er ihn angreifen kann
* Der Schneegolem sollte mit Eiern werfen.

### 11. Ändere die Golem-Geschwindigkeit

**Ziel** Mach den Golem schnell.

**Anleitung**:

Um die Geschwindigkeit des IronGolem zu ändern musst du die Klasse EntityIronGolem öffnen. Für einen Schneegolem entsprechend EnitySnowman. 
Die Anpassung ist die Gleiche in beiden Fällen.
Such nach `SharedMonsterAttributes.movementSpeed` und verändere den in `setAttribute` angegbenen Wert nach oben. (z.B. von 0.25 aif 1.25)

**Gameplay**

* Erschaffe einen Schneegolem oder einen Eisengolem
* Lass einen Zombie nicht zu nah bei dem Golem erscheinen damit dieser sich auf den Zombie zubewegen muss.
* Dor Golem wird sich sehr schnell bewegen und den Zombie angreifen.

**Tips**
Kombiniere das Ganze mit Mod #3 und lass den Schneegolem eine grosse Eisbahn erzeugen!

### 12. Der unbesiegbare Golem

**Ziel**: Mache Golems fast unbesiegbar.

**Anleitung**:

Wie schon in Mod #11 kannst du dich auch hier entscheiden ob du den Schneegolem oder den IronGolem verbessern willst. Die Änderungen sind in beiden Fällen identisch.
Suche `SharedMonsterAttributes.maxHealth` in der geöffnet Klasse und erhöhe dort den Wert in `setAttribute` (z.B. von 100 auf 1000, was sie fast unbesiegbar macht)

**Gameplay**

* Erschaffe einen Golem (Snow oder Iron)
* Versuch ihn mit deinem besten Schwert zu töten. Es ist beinahe unmöglich

... und deshalb gibt es das nächste Mod!

### 13. Erschaffe ein Superschwert

**Ziel** Ermögliche es den Golem aus Mod #12 zu töten.

**Anleitung**:

Öffne die Klasse ItemSword. In Zeile 27 steht:
`this.weaponDamage = 4.0F + par2EnumToolMaterial.getDamageVsEntity();` 
Ersetze 4.0 durch einen größeren Wert (so ca. 1000)

**Gameplay**

* Öffne das Inventar und suche nach einem Schwert. 
* Erschaffe einen Golem und versuch ihn mit dem Schwert zu töten. 
* Er wird nach einem Angriff sterben.
* Lass Zombies erscheinen und töte sie mit einem einzigen Schlag!

##Genau Anleitung
Du musst diesen Anweisungen nur folgen wenn du deinen eigenen Modding Kit erzeugen willst. Normalerweise sollten die vorbereiteten Mod-Kits (siehe Quick Start) reichen. 
Wenn du bereit bistuen kann viel Arbeit bedeuten und ein gutes Verständnis der Build Skripten voraussetzen.

Wenn du es wirklich versuchen willst dann folge diesen Schritten:

Lade Src-Paket von (files.minecraftforge.net). Seit 1. Jan 2014 [1.6.4-Recommended](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.6.4-
9.11.1.965/forge-1.6.4-9.11.1.965-src.zip) und [1.7.2-Latest](http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.2-10.12.0.982/forge-1.7.2-10.12.0.982

-src.zip) Pakete sind verfügbar. Von den Versionen 1.7.x wird abgeraten. [Erklärung hier](https://github.com/MinecraftForge/ForgeGradle/issues/27#issuecomment-31436639).

* Für 1.6.4 (empfohlen)
    * Entpacke das heruntergeladenen Paket
    * Ändere das Verzeichnis zu "forge"
    * Führe `install.sh` (auf Mac) oder `install.cmd` (auf Windows) aus, um das Forge-Modding zu konfigurieren.
* For 1.7.2 (not recommended)
    * Führe folgendes Kommando aus `./gradlew setupDevWorkspace --refresh-dependencies`

      Auf einem Mac könntest du in folgendes Problem laufen[ForgeGradle#34](https://github.com/MinecraftForge/ForgeGradle/issues/34). Du wirst `build/unpacked/dev.json` per Hand so wie [hier beschrieben](https://github.com/MinecraftForge/ForgeGradle/issues/34#issuecomment-31344841) anpassen müssen. Führe dann `./gradlew setupDecomWorkspace` aus
    * `./gradlew eclipse` um Eclipse spezifische Dateien/Verzeichnisse zu erzeugen. Du wirst auch wieder `dev.json` anpassen müssen..

