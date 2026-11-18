# Mission 1 : La boule magique 🎱

Transforme ta carte en boule magique qui répond à toutes les questions. Pose-lui une question, secoue-la, et elle décide pour toi !

**Il te faut :** une carte Core2, un portable avec MicroBlocks et le projet [magic-ball-start-fr.ubp](../starter/magic-ball-start-fr.ubp) (ton coach l'a ouvert).

**Rôles :** le **pilote** tient la souris, le **copilote** lit cette page à voix haute. Changez de rôle à chaque 🔄.

Nos blocs spéciaux sont dans la bibliothèque **Core2Buttons**, dans la liste des blocs à gauche.

## ⭐1 La boule parle

1. Va dans **Contrôle** et glisse un bloc **quand** dans l'espace vide.
2. Dans **Core2Buttons**, glisse **bouton du milieu touché ?** dans le trou du bloc **quand**.
3. Dans **Core2Buttons**, glisse **afficher grand texte _ couleur _** en dessous.
4. Clique dans la case de texte et tape `Pose-moi une question !`. Choisis une couleur qui te plaît.

**🧪 Essaie !** Touche le **cercle rouge du milieu** sous l'écran. Le texte apparaît-il ?

**🔄 Change de rôle**

## ⭐2 Une réponse au hasard

Une boule magique a besoin de réponses. On les range dans une **liste**.

1. Va dans **Variables**, clique sur **Ajouter une variable** et appelle-la `réponses`.
2. Sous **au démarrage** (il est déjà là), ajoute **mettre réponses à _**.
3. Mets un bloc **liste** (dans **Donnée**) dans le trou. Clique sur la flèche de la liste jusqu'à avoir 4 cases et tape : `Oui !`, `Pas question !`, `Possible...`, `Redemande`.
4. Clique une fois sur le script **au démarrage**, pour que la liste soit créée.
5. Dans ton script **quand**, remplace le texte `Pose-moi une question !` par **élément _ de _** (dans **Donnée**) : dans le premier trou mets **nombre aléatoire entre 1 et _** (dans **Opérateurs**), et dans le dernier trou de ce bloc mets **longueur de réponses** (dans **Donnée**). Dans le deuxième trou de **élément** mets **réponses**.

**🧪 Essaie !** Touche le cercle du milieu plusieurs fois. Obtiens-tu des réponses différentes ?

**🔄 Change de rôle**

## ⭐3 Secoue-la !

Une vraie boule magique, ça se secoue.

1. Dans **Opérateurs**, prends un bloc **_ ou _**.
2. Déplace **bouton du milieu touché ?** dans son côté gauche, et mets **carte secouée ?** (de **Core2Buttons**) dans son côté droit.
3. Mets le bloc **ou** dans le trou de ton bloc **quand**.

**🧪 Essaie !** Tiens la carte à deux mains et secoue-la fort. Une réponse apparaît-elle ?

**🔄 Change de rôle**

## ⭐4 Couleurs, bips et vibrations

1. Dans **Variables**, mets **définir n à** tout en haut du script **quand** et règle-le sur **nombre aléatoire entre 1 et longueur de réponses**. Utilise maintenant **élément n de réponses** pour afficher la réponse.
2. Ajoute un bloc **si** (Contrôle) et clique sur sa flèche jusqu'à voir **si … sinon, si … sinon**. Ensuite : **si n = 1** affiche la réponse en vert, **sinon, si n = 2** en rouge, **sinon** en jaune.
3. Sous le **si**, ajoute **bip 880 Hz pendant 150 ms** et **vibrer pendant 200 ms**.
4. Ajoute **attendre 1500 millisecondes**, puis **afficher grand texte** `Pose-moi une question !` en blanc.

**🧪 Essaie !** Pose une question à voix haute, puis secoue. La carte bipe-t-elle, vibre-t-elle et affiche-t-elle une réponse en couleur ?

**🔄 Change de rôle**

## 🎉 Bravo !

Tu as construit une boule magique avec des **événements** (quand), une **liste**, des nombres **au hasard**, un **capteur** (la secousse) et des **sorties** (écran, son, vibration). Choisis une [carte bonus](bonus-cards.md) pour la rendre encore meilleure !
