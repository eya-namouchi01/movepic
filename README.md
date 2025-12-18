**« Classement de photos » en Python**

Le but de ce projet consiste à rechercher tous les photos (.jpg ou .png) à partir du dossier dont le
nom est donné en paramètre au script et les classer (c’est à dire les déplacer) dans des dossiers (par
années) et des sous-dossiers (par mois) qui seront créés à l’occasion (et non au préalable).
Un fichier récapitulatif au format csv (listePhotos.csv) doit être aussi créé répertoriant à quel endroit
chaque photo a été déplacée (et qui laissera la possibilité de rajouter des commentaires).
Un bonus serait que les photos apparaissent par ordre chronologique dans ce fichier.


***Contraintes techniques :***
Le projet doit se faire en python et n’utiliser aucun module hormis sys, os, PIL (et potentiellement,
car ce n’est pas obligatoire, re).
Le parcours des dossiers doit se faire via une fonction récursive utilisant les fonctions os.listdir() et
os.path.isdir() comme vues en cours (en fait ce projet a les mêmes bases que le troisième TP). La
fonction os.walk() ne doit pas être utilisée, ni l’utilisation indirecte de commande comme ls -R.
