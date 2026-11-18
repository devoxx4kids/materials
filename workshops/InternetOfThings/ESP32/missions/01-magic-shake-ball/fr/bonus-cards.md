# Mission 1 : cartes bonus 🃏

Choisis n'importe quelle carte. Chacune fonctionne toute seule.

---

## 🃏 Carte A : Tes propres réponses

**But :** la boule donne tes propres réponses rigolotes.

**Comment :** clique sur la flèche du bloc **liste** pour ajouter des cases, et tape de nouvelles réponses, comme `Demande à ton chat` ou `Seulement le mardi`.

**Astuce :** les longues réponses sont coupées sur plusieurs lignes, donc elles tiennent quand même sur l'écran.

---

## 🃏 Carte B : Une tête pour chaque réponse

**But :** dessiner une tête à côté de la réponse.

**Comment :** ajoute la bibliothèque **TFT** (**Ajouter une bibliothèque** → **Graphics and Displays** → **TFT**). Utilise **dessiner un cercle sur TFT** pour la tête et deux petits cercles remplis pour les yeux. Dessine un sourire pour oui, une grimace pour non.

**Conseil pour le coach :** l'écran fait 320 de large et 240 de haut ; dessinez après **afficher grand texte**, car ce bloc efface l'écran.

---

## 🃏 Carte C : Le bouton secret de triche

**But :** quand *toi* tu touches le cercle de gauche, la boule dit toujours oui. Tes amis n'en sauront rien !

**Comment :** fais un nouveau script **quand** avec **bouton gauche touché ?** qui affiche `Oui !` en vert.

---

## 🃏 Carte D : Compteur de questions

**But :** la boule compte combien de questions elle a répondues.

**Comment :** ajoute une variable `compteur`. Mets-la à 0 dans **au démarrage**. Ajoute **changer compteur par 1** dans ton script **quand**. Affiche-la avec **joindre** (dans **Donnée**) `Questions : ` **et** **compteur**.

**Conseil pour le coach :** affichez le compteur après la réponse, après l'attente.
