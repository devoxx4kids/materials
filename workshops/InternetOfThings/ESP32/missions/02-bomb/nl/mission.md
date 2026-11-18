# Missie 2: De bom 💣

Jullie zijn de ontmijningsdienst! Breng de bom naar de veilige zone zonder hem te schokken... anders BOEM!

**Je hebt nodig:** een Core2-bord, een laptop met MicroBlocks, het project [bomb-start-nl.ubp](../starter/bomb-start-nl.ubp) en een veilige zone op de tafel (je coach duidt die aan).

**Rollen:** de **bestuurder** gebruikt de muis, de **navigator** leest deze pagina hardop voor. Wissel bij elke 🔄. **Draag het bord altijd met twee handen, en wandel.**

## ⭐1 De bom verschijnt

1. Ga naar **Variabelen** en voeg een variabele `speelt` toe. Voeg onder **wanneer gestart** de blokken **maak speelt** onwaar (de schakelaar uit) en **toon bom kalm** (uit **Core2Buttons**) toe.
2. Maak een script **wanneer** met **middelste knop aangeraakt?**. Daarin: **timer resetten**, **toon gevarenbalk 0** en **maak speelt** waar (de schakelaar aan).

**waar / onwaar:** neem het schakelaarblok uit **Functies** en zet het in het gat van **maak**. Klik op de schakelaar om hem uit te zetten: dat is onwaar. Aan is waar. Typ niet het woord `waar`: dan is het alleen tekst, en begint het spel nooit.

**🧪 Probeer het!** Klik op ▶. Zie je de bom? Raak de middelste cirkel aan: onderaan verschijnt de gevarenbalk, het spel is begonnen.

**🔄 Wissel**

## ⭐2 Hoe hard beweeg je?

1. Maak een tweede script **wanneer**, deze keer met de variabele **speelt** in de **wanneer** (zo loopt het tijdens het spel). Daarin: **toon grote tekst (schok)** in het wit en **wacht 30 milliseconden**.
2. Klik op ▶, raak de middelste cirkel aan en beweeg het bord langzaam, dan sneller.

**🧪 Probeer het!** Welk getal krijg je als je het stil houdt? Als je wandelt? Als je ertegen stoot?

**🔄 Wissel**

## ⭐3 De gevarenmeter

1. Voeg de variabelen `gevaar` en `stemming` toe. Voeg in het script van de middelste cirkel ook **maak gevaar 0** en **maak stemming 0** toe.
2. Haal in het script **wanneer speelt** de schoktekst weg. Eerst **initialiseer lokaal j naar (schok)**, zodat je maar één keer meet. Gebruik dan **als / anders**: als **j > 15**, verander gevaar met **(j − 15) / 2**; anders, als **j < 10** en gevaar > 0, verander gevaar met -1. Tip: als de bom nerveus wordt, **sta stil** om hem te kalmeren.
3. Dan een blok **als** (klik op het pijltje tot je **als … anders als … anders** ziet): **als gevaar >= 100**: **maak speelt** onwaar, **toon bom ontploft**, **tril 800 ms**, **toon grote tekst** `BOEM!` in het rood. **Anders als gevaar >= 50**: **toon bom nerveus**, **piep 880 Hz gedurende 40 ms** en **maak stemming 1**. **Anders**: alleen **als stemming = 1**, **toon bom kalm** en **maak stemming 0** (de bom tekenen duurt even, dus we tekenen hem alleen als hij verandert).
4. Op het einde van het script: **toon gevarenbalk (gevaar)** en **wacht 30 milliseconden**.

**🧪 Probeer het!** Wandel naar de veilige zone. Wordt de bom nerveus als je ertegen stoot?

**🔄 Wissel**

## ⭐4 Veilig!

1. Maak van het script van de middelste cirkel een **als speelt / anders**:
   - **als speelt** (de bom is in de veilige zone): **maak speelt** onwaar, **toon bom veilig**, dan **toon grote tekst (samenvoegen `VEILIG! ` (timer / 1000) ` s`)** in het groen;
   - **anders** (een nieuw spel beginnen): alles wat het script eerst deed (timer resetten, gevaar 0, stemming 0, **toon bom kalm**, gevarenbalk 0, **maak speelt** waar).

**🧪 Probeer het!** Hoe snel kun je de bom in veiligheid brengen zonder dat hij ontploft? (Wacht tot `BOEM!` of `VEILIG!` op het scherm staat voor je de middelste cirkel opnieuw aanraakt.)

**🔄 Wissel**

## 🎉 Gelukt!

Je hebt een spel gebouwd met een **sensor** (beweging), een **variabele die verandert met de tijd** (de gevarenmeter), **grenzen** (50 en 100), plaatjes en een **timer**. Probeer een [bonuskaart](bonus-cards.md)!

*Animaties van de bom en de ontploffing: Noto Animated Emoji van Google, CC BY 4.0.*
