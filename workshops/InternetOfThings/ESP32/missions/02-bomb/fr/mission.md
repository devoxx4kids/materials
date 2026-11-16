# Mission 2 : La bombe 💣

Tu fais partie de l'équipe de déminage ! Porte la bombe jusqu'à la zone de sécurité sans la secouer... sinon BOUM !

**Il te faut :** une carte Core2, un portable avec MicroBlocks, le projet [bomb-start-fr.ubp](../starter/bomb-start-fr.ubp) et une zone de sécurité sur la table (ton coach la marque).

**Rôles :** le **pilote** tient la souris, le **copilote** lit cette page à voix haute. Changez de rôle à chaque 🔄. **Porte toujours la carte à deux mains, et marche.**

## ⭐1 La bombe apparaît

1. Va dans **Variables** et ajoute une variable `enJeu`. Sous **au démarrage**, ajoute **mettre enJeu à** faux (l'interrupteur éteint) et **afficher la bombe calme** (de **Core2Buttons**).
2. Fais un script **quand** avec **bouton du milieu touché ?**. Dedans : **réinitialiser le minuteur**, **afficher la barre de danger 0** et **mettre enJeu à** vrai (l'interrupteur allumé).

**🧪 Essaie !** Clique sur ▶. Vois-tu la bombe ? Touche le cercle du milieu : la barre de danger apparaît en bas, la partie a commencé.

**🔄 Change de rôle**

## ⭐2 À quel point bouges-tu ?

1. Fais un deuxième script **quand**, cette fois avec la variable **enJeu** dans le **quand** (il tourne donc pendant la partie). Dedans : **afficher grand texte (secousse)** en blanc et **attendre 30 millisecondes**.
2. Clique sur ▶, touche le cercle du milieu et bouge la carte lentement, puis plus vite.

**🧪 Essaie !** Quel nombre obtiens-tu quand tu la tiens immobile ? Quand tu marches ? Quand tu la cognes ?

**🔄 Change de rôle**

## ⭐3 Le compteur de danger

1. Ajoute les variables `danger` et `humeur`. Dans le script du cercle du milieu, ajoute aussi **mettre danger à 0** et **mettre humeur à 0**.
2. Dans le script **quand enJeu**, enlève le texte de la secousse. D'abord **définir j à (secousse)**, pour mesurer une seule fois. Puis utilise **si / sinon** : si **j > 15**, change danger par **(j − 15) / 2** ; sinon, si **j < 10** et danger > 0, change danger par -1. Astuce : quand la bombe devient nerveuse, **reste immobile** pour la calmer.
3. Ensuite un bloc **si** (clique sur sa flèche jusqu'à voir **si … sinon, si … sinon**) : **si danger >= 100** : **mettre enJeu à** faux, **afficher la bombe explose**, **vibrer pendant 800 ms**, **afficher grand texte** `BOUM !` en rouge. **Sinon, si danger >= 50** : **afficher la bombe nerveuse**, **bip 880 Hz pendant 40 ms** et **mettre humeur à 1**. **Sinon** : seulement **si humeur = 1**, **afficher la bombe calme** et **mettre humeur à 0** (dessiner la bombe prend du temps, alors on ne la dessine que quand elle change).
4. À la fin du script : **afficher la barre de danger (danger)** et **attendre 30 millisecondes**.

**🧪 Essaie !** Marche jusqu'à la zone de sécurité. La bombe devient-elle nerveuse quand tu la cognes ?

**🔄 Change de rôle**

## ⭐4 En sécurité !

1. Transforme le script du cercle du milieu en **si enJeu / sinon** :
   - **si enJeu** (la bombe est dans la zone de sécurité) : **mettre enJeu à** faux, **afficher la bombe en sécurité**, puis **afficher grand texte (joindre `BRAVO ! ` (minuteur / 1000) ` s`)** en vert ;
   - **sinon** (commencer une nouvelle partie) : tout ce que le script faisait avant (réinitialiser le minuteur, danger 0, humeur 0, **afficher la bombe calme**, barre de danger 0, **mettre enJeu à** vrai).

**🧪 Essaie !** En combien de temps peux-tu mettre la bombe en sécurité sans la faire exploser ? (Attends que `BOUM !` ou `BRAVO !` s'affiche avant de toucher à nouveau le cercle du milieu.)

**🔄 Change de rôle**

## 🎉 Bravo !

Tu as construit un jeu avec un **capteur** (le mouvement), une **variable qui change avec le temps** (le compteur de danger), des **limites** (50 et 100), des images et un **minuteur**. Essaie une [carte bonus](bonus-cards.md) !

*Animations de la bombe et de l'explosion : Noto Animated Emoji de Google, CC BY 4.0.*
