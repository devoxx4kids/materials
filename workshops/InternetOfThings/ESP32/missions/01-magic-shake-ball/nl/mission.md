# Missie 1: De magische schudbal 🎱

Maak van je bord een magische bal die op elke vraag antwoordt. Stel een vraag, schud het bord, en het beslist voor jou!

**Je hebt nodig:** een Core2-bord, een laptop met MicroBlocks en het project [magic-ball-start-nl.ubp](../starter/magic-ball-start-nl.ubp) (je coach heeft het geopend).

**Rollen:** de **bestuurder** gebruikt de muis, de **navigator** leest deze pagina hardop voor. Wissel bij elke 🔄.

Onze speciale blokken zitten in de bibliotheek **Core2Buttons**, in de lijst met blokken links.

## ⭐1 De bal spreekt

1. Ga naar **Besturen** en sleep een blok **wanneer** naar de lege ruimte.
2. Sleep uit **Core2Buttons** het blok **middelste knop aangeraakt?** in het gat van het blok **wanneer**.
3. Sleep uit **Core2Buttons** het blok **toon grote tekst _ kleur _** eronder.
4. Klik in het tekstvak en typ `Stel me een vraag!`. Kies een kleur die je mooi vindt.

**🧪 Probeer het!** Raak de **middelste rode cirkel** onder het scherm aan. Verschijnt de tekst?

**🔄 Wissel**

## ⭐2 Een willekeurig antwoord

Een magische bal heeft antwoorden nodig. We bewaren ze in een **lijst**.

1. Ga naar **Variabelen**, klik op **Voeg een variabele toe** en noem ze `antwoorden`.
2. Voeg onder **wanneer gestart** (dat staat er al) het blok **maak antwoorden _** toe.
3. Zet een blok **lijst** (uit **Data**) in het gat. Klik op het pijltje van de lijst tot hij 4 vakjes heeft en typ: `Ja!`, `Echt niet!`, `Misschien...`, `Vraag opnieuw`.
4. Klik één keer op het script **wanneer gestart**, zodat de lijst gemaakt wordt.
5. Vervang in je script **wanneer** de tekst `Stel me een vraag!` door **item _ van _** (uit **Data**): zet in het eerste gat **willekeurig getal tussen 1 en _** (uit **Functies**), en zet in het laatste gat van dat blok **lengte van antwoorden** (uit **Data**). Zet in het tweede gat van **item** het blok **antwoorden**.

**🧪 Probeer het!** Raak de middelste cirkel een paar keer aan. Krijg je verschillende antwoorden?

**🔄 Wissel**

## ⭐3 Schud maar!

Een echte magische bal moet je schudden.

1. Neem uit **Functies** een blok **_ of _**.
2. Verplaats **middelste knop aangeraakt?** naar de linkerkant ervan, en zet **bord geschud?** (uit **Core2Buttons**) aan de rechterkant.
3. Zet het blok **of** in het gat van je blok **wanneer**.

**🧪 Probeer het!** Houd het bord met twee handen vast en schud het stevig. Verschijnt er een antwoord?

**🔄 Wissel**

## ⭐4 Kleuren, piepjes en trillen

1. Zet uit **Variabelen** het blok **initialiseer lokaal n naar** bovenaan het script **wanneer** en stel het in op **willekeurig getal tussen 1 en lengte van antwoorden**. Gebruik nu **item n van antwoorden** om het antwoord te tonen.
2. Voeg een blok **als** (Besturen) toe en klik op het pijltje tot je **als … anders als … anders** ziet. Dan: **als n = 1** toon je het antwoord in het groen, **anders als n = 2** in het rood, **anders** in het geel.
3. Voeg onder de **als** de blokken **piep 880 Hz gedurende 150 ms** en **tril 200 ms** toe.
4. Voeg **wacht 1500 milliseconden** toe en daarna **toon grote tekst** `Stel me een vraag!` in het wit.

**🧪 Probeer het!** Stel hardop een vraag en schud dan. Piept het bord, trilt het en toont het een gekleurd antwoord?

**🔄 Wissel**

## 🎉 Gelukt!

Je hebt een magische bal gebouwd met **gebeurtenissen** (wanneer), een **lijst**, **willekeurige** getallen, een **sensor** (schudden) en **uitvoer** (scherm, geluid, trillen). Kies een [bonuskaart](bonus-cards.md) om hem nog beter te maken!
