# Mission 3 : La messagerie emoji 📡

Envoie des emojis de ta carte vers d'autres cartes, par radio. Pas d'internet, pas de routeur Wi-Fi : les cartes se parlent directement.

**Il te faut :** une carte Core2, un portable avec MicroBlocks, le projet [emoji-messenger-start-fr.ubp](../starter/emoji-messenger-start-fr.ubp) et un autre binôme à ta table.

**Rôles :** le **pilote** tient la souris, le **copilote** lit cette page à voix haute. Changez de rôle à chaque 🔄.

## ⭐1 Allô, la radio !

1. Dans **au démarrage**, remplace le numéro de groupe `1` par ton **numéro de table**. Seules les cartes avec le même numéro s'entendent.
2. Remplace `Equipe 1` par le nom de ton équipe (court, sans le signe `|`).
3. Clique une fois sur **au démarrage**.
4. Fais un script **quand** avec **bouton du milieu touché ?** et ajoute **espNow envoyer la paire monNom = 1**.
5. Fais un autre script **quand** avec **espNow paire reçue ?** et ajoute **afficher grand texte (espNow dernière chaîne)** en jaune.

**🧪 Essaie !** Les deux binômes de la table touchent le cercle du milieu. Vois-tu le nom de l'autre équipe ?

**🔄 Change de rôle**

## ⭐2 Choisis un emoji

La liste `emojis` est déjà dans ton projet : `:-)` `:-D` `;-)` `<3` `:-O` `:-(` `B-)` `:-P`. Penche la tête vers la gauche pour voir les visages !

1. Fais un script **quand** avec **bouton droit touché ?** : **changer choix par 1**, **si choix > longueur de emojis** mettre choix à 1, puis **afficher grand texte (élément choix de emojis)** (**élément** et **longueur de** sont dans **Donnée**).
2. Fais pareil avec **bouton gauche touché ?** : changer choix par -1, et si choix < 1 mets-le à **longueur de emojis**.
3. Dans le script du bouton du milieu, envoie **choix** au lieu de 1 : **espNow envoyer la paire monNom = choix**.

**🧪 Essaie !** Fais défiler avec la gauche et la droite. L'emoji change-t-il ?

**🔄 Change de rôle**

## ⭐3 Affiche ce qui arrive

1. Dans le script **espNow paire reçue ?**, ajoute **définir n à (espNow dernier nombre)**.
2. **Si n >= 1 et n <= longueur de emojis** : affiche **élément n de emojis** en grand et en jaune, **bip 660 Hz pendant 100 ms** et attends 2000 ms. Les autres nombres sont ignorés : ça protège ta carte des messages bizarres.
3. À la fin, affiche à nouveau ton propre emoji : **afficher grand texte (élément choix de emojis)**.

**🧪 Essaie !** Envoyez-vous des emojis. Entends-tu le bip quand un emoji arrive ?

**🔄 Change de rôle**

## ⭐4 Secoue pour faire la fête !

Toutes les cartes de ton groupe entendent tous les messages. C'est ce qu'on appelle une **diffusion** (en anglais *broadcast*).

1. Fais un script **quand** avec **carte secouée ?** et ajoute **espNow envoyer la paire monNom = 0**, **afficher grand texte** `Parti !` en vert et **attendre 500 millisecondes** (pour qu'une secousse envoie un seul message, pas des dizaines). Puis affiche à nouveau ton emoji : **afficher grand texte (élément choix de emojis)**.
2. Dans le script de réception, ajoute avant l'autre test : **si n = 0**, **répéter 3 fois** : affiche `FIESTA !` en rose, **vibrer pendant 250 ms**, affiche `FIESTA !` en bleu clair, attends 100 ms.

**🧪 Essaie !** Secoue ta carte. Toute la table fait-elle la fête ?

**🔄 Change de rôle**

## 🎉 Bravo !

Tu as construit une messagerie radio avec des **groupes**, des **listes**, des **messages** faits d'un nom et d'un nombre, et une **diffusion**. Essaie une [carte bonus](bonus-cards.md) !
