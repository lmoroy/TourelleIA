# TourelleIA

Projet Culture Maker 2020/2021 

Team:
  * Moroy Liam (chef de projet)
  * Pouget Filipe
  * Nieddu Thomas
  * Cottin Léonard

# Description

  Ce projet s'inscrit dans le cadre de l'UE Culture Maker 2020/2021. L'idée est de faire une tourelle automatique qui tire sur les gens que la tourelle détecte. Ce projet se décompose en plusieurs partie:
    * Soft: Code python pour la reconnaissance faciale et la gestion des servomoteurs via les I/O d'une raspberry 4B.
    * Méca: Socle sur lequel repose les servomoteurs, design des 2 axes de rotations et (si le temps nous le permet) un actionneur pour pousser la gachette du fusil.
  Pour ce projet nous avons utilisé la découpeuse laser du Fablab et de l'impression 3D. Les fichiers sont à disposition dans leur dossier respectif (piece3D et pieceLaser)

  # Soft
  
  Pour la détection, on utilise une Raspicam qui est controllée en python. Les images constituant le flux vidéo reçu de la raspicam est donné en entrée à un réseau de neurone (Haar Casacde) qui nous renvoie une coordonnée dxy = (x,y) correspondant au centre la box détectant le visage. on fait ensuite la différence entre dxy et cxy = (cx,cy) correspondant au coordonnée du centre de l'image.

  // Insérer un image
