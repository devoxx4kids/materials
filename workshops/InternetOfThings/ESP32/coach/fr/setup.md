# Préparer les portables et les cartes

Faites-le la veille. Comptez environ 5 minutes par carte.

## 1. Portables

- Installez Chrome ou Edge, ou l'application MicroBlocks pour ordinateur depuis https://microblocks.fun/download (utilisez l'application si le lieu n'a pas d'internet fiable).
- Téléchargez ce dossier d'atelier sur chaque portable, ou mettez les fichiers `missions/*/starter/*.ubp` de votre langue sur une clé USB.
- Vérifiez chaque câble : un câble USB-C qui ne fait que charger est la raison la plus fréquente pour laquelle une carte « n'est pas trouvée ». Étiquetez les câbles qui fonctionnent.

## 2. Installer le firmware de l'atelier sur chaque Core2 (une seule fois)

Le firmware MicroBlocks standard ne gère pas entièrement la Core2 v1.3. Utilisez le firmware de l'atelier dans `firmware/` (MicroBlocks avec un petit correctif pour le capteur de mouvement et le moteur de vibration de la v1.3, plus les images de la bombe pour la mission 2).

1. Installez une fois Python 3 et esptool : `pip install "esptool>=5"` (les anciennes versions d'esptool utilisent d'autres noms de commandes).
2. Fermez MicroBlocks, branchez la Core2 avec un câble de données et lancez depuis le dossier de l'atelier (remplacez `<PORT>` ; sur macOS il ressemble à `/dev/cu.usbserial-…`) :

       esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin

3. Débranchez le câble, éteignez la carte (bouton de gauche maintenu 6 secondes) puis rallumez-la (2 secondes), et rebranchez le câble.
4. Ouvrez MicroBlocks (https://microblocks.fun → **Run**), connectez-vous et vérifiez que le nom de la carte est **M5StackCore2**.
5. Ouvrez `missions/01-magic-shake-ball/solution/magic-ball-done-fr.ubp`, cliquez sur ▶ et secouez la carte : une réponse apparaît, avec un bip et une vibration. La carte est prête.

L'écran reste noir et la LED verte reste éteinte tant qu'aucun programme ne dessine quelque chose : c'est normal.

## 3. Langue

Cliquez sur l'icône **globe** dans MicroBlocks et choisissez English, Français ou Nederlands. Ouvrez ensuite le projet de départ avec le même code de langue (`-en`, `-fr` ou `-nl`), pour que les blocs d'aide soient aussi dans cette langue.

## 4. Cartes

- Chargez complètement chaque carte (la batterie tient une séance ; apportez quand même les chargeurs).
- Collez un numéro au dos de chaque carte et numérotez les tables. Dans la mission 3, le numéro de la table est le groupe radio.
- Gardez deux cartes de réserve prêtes, avec le firmware installé.

## 5. Test rapide de la radio (seulement pour la mission 3)

Ouvrez `missions/03-emoji-messenger/solution/emoji-messenger-done-fr.ubp` sur deux cartes et envoyez un emoji de l'une à l'autre. Voir [animer une séance](running-a-session.md) pour les numéros de groupe.
