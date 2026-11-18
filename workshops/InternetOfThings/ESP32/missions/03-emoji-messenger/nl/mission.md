# Missie 3: Emoji-berichten 📡

Stuur emoji's van je bord naar andere borden, via de radio. Geen internet, geen wifi-router: de borden praten rechtstreeks met elkaar.

**Je hebt nodig:** een Core2-bord, een laptop met MicroBlocks, het project [emoji-messenger-start-nl.ubp](../starter/emoji-messenger-start-nl.ubp) en een ander duo aan je tafel.

**Rollen:** de **bestuurder** gebruikt de muis, de **navigator** leest deze pagina hardop voor. Wissel bij elke 🔄.

## ⭐1 Hallo, radio!

1. Verander in **wanneer gestart** het groepsnummer `1` in je **tafelnummer**. Alleen borden met hetzelfde nummer horen elkaar.
2. Verander `Team 1` in de naam van je team (kort, zonder het teken `|`).
3. Klik één keer op **wanneer gestart**.
4. Maak een script **wanneer** met **middelste knop aangeraakt?** en voeg **espNow send pair mijnNaam = 1** toe.
5. Maak nog een script **wanneer** met **espNow pair received?** en voeg **toon grote tekst (espNow last string)** in het geel toe.

**🧪 Probeer het!** Beide duo's aan de tafel raken de middelste cirkel aan. Zie je de naam van het andere team?

**🔄 Wissel**

## ⭐2 Kies een emoji

De lijst `emojis` zit al in je project: `:-)` `:-D` `;-)` `<3` `:-O` `:-(` `B-)` `:-P`. Kantel je hoofd naar links om de gezichtjes te zien!

1. Maak een script **wanneer** met **rechterknop aangeraakt?**: **verander keuze met 1**, **als keuze > lengte van emojis** maak keuze 1, dan **toon grote tekst (item keuze van emojis)** (**item** en **lengte van** zitten in **Data**).
2. Doe hetzelfde met **linkerknop aangeraakt?**: verander keuze met -1, en als keuze < 1 maak keuze **lengte van emojis**.
3. Stuur in het script van de middelste knop **keuze** in plaats van 1: **espNow send pair mijnNaam = keuze**.

**🧪 Probeer het!** Blader met links en rechts. Verandert de emoji?

**🔄 Wissel**

## ⭐3 Toon wat er aankomt

1. Voeg in het script **espNow pair received?** het blok **initialiseer lokaal n naar (espNow last number)** toe.
2. **Als n >= 1 en n <= lengte van emojis**: toon **item n van emojis** groot in het geel, **piep 660 Hz gedurende 100 ms** en wacht 2000 ms. Andere getallen worden genegeerd: zo blijft je bord veilig voor rare berichten.
3. Toon op het einde weer je eigen emoji: **toon grote tekst (item keuze van emojis)**.

**🧪 Probeer het!** Stuur elkaar emoji's. Hoor je de piep als er een aankomt?

**🔄 Wissel**

## ⭐4 Schud voor een feestje!

Elk bord in je groep hoort elk bericht. Dat heet een **broadcast** (een bericht voor iedereen).

1. Maak een script **wanneer** met **bord geschud?** en voeg **espNow send pair mijnNaam = 0**, **toon grote tekst** `Verstuurd!` in het groen en **wacht 500 milliseconden** toe (zo stuurt één keer schudden één bericht, geen tientallen). Toon daarna weer je emoji: **toon grote tekst (item keuze van emojis)**.
2. Voeg in het ontvangstscript vóór de andere test toe: **als n = 0**, **herhaal 3**: toon `FEEST!` in het roze, **tril 250 ms**, toon `FEEST!` in het lichtblauw, wacht 100 ms.

**🧪 Probeer het!** Schud je bord. Viert de hele tafel feest?

**🔄 Wissel**

## 🎉 Gelukt!

Je hebt een radioberichtendienst gebouwd met **groepen**, **lijsten**, **berichten** van een naam en een getal, en een **broadcast**. Probeer een [bonuskaart](bonus-cards.md)!
