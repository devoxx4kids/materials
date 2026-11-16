# Laptops en borden klaarmaken

Doe dit de dag ervoor. Reken op ongeveer 5 minuten per bord.

## 1. Laptops

- Installeer Chrome of Edge, of de MicroBlocks-app voor de computer via https://microblocks.fun/download (gebruik de app als de locatie geen betrouwbaar internet heeft).
- Download deze workshopmap op elke laptop, of zet de bestanden `missions/*/starter/*.ubp` van je taal op een USB-stick.
- Controleer elke kabel: een USB-C-kabel die alleen laadt is de meest voorkomende reden dat een bord "niet gevonden" wordt. Label de kabels die werken.

## 2. De workshopfirmware op elke Core2 zetten (één keer)

De standaard MicroBlocks-firmware ondersteunt de Core2 v1.3 niet helemaal. Gebruik de workshopfirmware uit `firmware/` (MicroBlocks met een kleine aanpassing voor de bewegingssensor en de trilmotor van de v1.3, plus de bomplaatjes voor missie 2).

1. Installeer één keer Python 3 en esptool: `pip install "esptool>=5"` (oudere versies van esptool gebruiken andere commandonamen).
2. Sluit MicroBlocks, sluit de Core2 aan met een datakabel en voer uit vanuit de workshopmap (vervang `<PORT>`; op macOS lijkt hij op `/dev/cu.usbserial-…`):

       esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin

3. Trek de kabel uit, zet het bord uit (linkerknop 6 seconden ingedrukt houden) en weer aan (2 seconden), en steek de kabel er weer in.
4. Open MicroBlocks (https://microblocks.fun → **Run**), maak verbinding en controleer dat de naam van het bord **M5StackCore2** is.
5. Open `missions/01-magic-shake-ball/solution/magic-ball-done-nl.ubp`, klik op ▶ en schud het bord: er verschijnt een antwoord, met een piep en een tril. Het bord is klaar.

Het scherm blijft zwart en de groene led blijft uit zolang geen programma iets tekent: dat is normaal.

## 3. Taal

Klik in MicroBlocks op het **wereldbol**-icoon en kies English, Français of Nederlands. Open daarna het startproject met dezelfde taalcode (`-en`, `-fr` of `-nl`), zodat de hulpblokken ook in die taal zijn.

## 4. Borden

- Laad elk bord helemaal op (de batterij houdt een sessie vol; neem toch laders mee).
- Plak een nummer op de achterkant van elk bord en nummer de tafels. In missie 3 is het tafelnummer de radiogroep.
- Houd twee reserveborden klaar, met de firmware erop.

## 5. Snelle test van de radio (alleen voor missie 3)

Open `missions/03-emoji-messenger/solution/emoji-messenger-done-nl.ubp` op twee borden en stuur een emoji van het ene naar het andere. Zie [een sessie leiden](running-a-session.md) voor de groepsnummers.
