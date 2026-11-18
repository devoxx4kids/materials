# Animer une séance de 45 minutes

## Avant l'arrivée des enfants

- Chaque portable a MicroBlocks ouvert, une carte connectée et le **projet de départ** de la mission du jour ouvert dans la bonne langue.
- Le projet solution de la mission est sur votre propre portable.
- Pour la mission 2, marquez sur chaque table un point de départ et une zone de sécurité (une feuille de papier) à environ 3 mètres l'un de l'autre. Les enfants portent la carte à deux mains, en marchant.

## Déroulement

| Minutes | Ce qui se passe | Votre rôle |
|---|---|---|
| 0–5 | Accueil, montrez le projet fini sur votre carte | Restez bref et amusant ; laissez-les deviner comment ça marche |
| 5–30 | Le binôme suit `mission.md`, étapes ⭐1 à ⭐4 | Circulez ; posez des questions au lieu de prendre la souris |
| 30–40 | Cartes bonus, choisies par le binôme | Distribuez les cartes ; félicitez leurs propres idées |
| 40–45 | Présentation : chaque binôme montre sa carte à la table voisine | Demandez à chaque binôme ce qu'il a changé |

Un binôme plus lent, ce n'est pas grave : finir ⭐3 donne déjà une boule magique / un jeu qui fonctionne.

## Binômes

- **Pilote** : tient la souris et construit les blocs.
- **Copilote** : lit la page de mission à voix haute et vérifie chaque étape.
- Ils échangent les rôles à chaque ⭐. La page de mission le leur rappelle avec 🔄.

## Groupes radio (mission 3)

Chaque table utilise son propre numéro de groupe, à partir de 1, pour que 20 cartes dans la même salle ne reçoivent pas toutes les messages des autres. Écrivez le numéro sur la table. Les binômes le règlent dans le premier bloc de leur projet de départ. Pour la carte bonus « envoyer à une autre table », deux tables se mettent d'accord sur un groupe commun.

## Problèmes fréquents

| Symptôme | Solution |
|---|---|
| Carte introuvable | Rebranchez ; utilisez un câble USB-C de données ; rechargez la page ou redémarrez l'application |
| Écran noir | Appuyez sur le bouton d'alimentation sur le côté gauche ; chargez la carte |
| Les boutons ne réagissent pas | Ouvrez le projet de départ, pour que la bibliothèque d'aide soit chargée |
| Les messages n'arrivent pas | Les deux cartes doivent utiliser le même numéro de groupe |
| Pas de son | Vérifiez que le bloc bip est utilisé ; utilisez plutôt le bloc vibrer |
| **carte secouée ?** n'est jamais vrai, pas de vibration | Une mise à jour a remplacé le firmware de l'atelier : réinstallez-le (voir [préparation](setup.md)) |
| Mission 2 : la barre de danger apparaît, mais rien d'autre ne se passe | `enJeu` a reçu le mot tapé `vrai` : utilisez le bloc interrupteur de **Opérateurs** |
| Images de la bombe absentes | Réinstallez le firmware de l'atelier avec les deux fichiers (voir [préparation](setup.md)) |

Quand un binôme est bloqué plus de deux minutes, ouvrez le projet solution sur votre portable et comparez son script avec le leur, bloc par bloc.

## Limites connues

- Accents : les minuscules accentuées (é, è, ê, à, ç, ù…) s'affichent correctement avec le firmware de l'atelier ; les majuscules ne gardent leur accent que là où la petite police de l'écran a de la place.
- Radio : testée avec deux cartes. ESP Now ne garantit pas la livraison, donc dans une salle pleine un message peut parfois se perdre ; il suffit de le renvoyer.
- Sans `firmware/bomb-images.bin`, la bombe fonctionne toujours, mais sans images (voir [préparation](setup.md)).
