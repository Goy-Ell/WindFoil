# WindFoil

- Application qui donne en temps réel les dernières mesures sur 3 stations locales disposant d’un anémomètre.
- La base de données locale est mise à jour toute les 15 min 
- Stockage max = 10 derniers enregistrements.
- Backup de la bdd tous les 5 enregistrements).
- BDD sur SQLite 
- Données  récupérées depuis API des stations : http://developers.pioupiou.fr/api/live/

## projetFoil.py
fichier principal comportant le main et les fonctions

## projetFoil_class.py
fichier comportant les classes

## script_bd.sql
script sql pour la creation des tables en bdd


