# cvi_geometry
## Description - English
This script creates Geographic Polygon layers, as WKT CSV format, by associating information contained in two kinds of files :
* The "Fiche de compte" file, in pdf format, from the "CVI", wich is a document all wine growers have, edited by the French customs
* Geographic layers from the French Registry Land office (Cadastre) in Geo JSON format


### Input files
* Inside "cvis" directory:
Introduce your parcel files from the CVI. French winegrowers can generate them from their personnal space in the Customs (Douane) website (https://www.douane.gouv.fr).
* Inside CADASTRE directory:
Download there all required JSON files from the open data platform of the French Land Registry office (cadastre) (https://cadastre.data.gouv.fr/datasets/cadastre-etalab).
This data can be whole "departments" (Départements - a French administrative division) or single towns.
Size of the files can be important (espacially for whole departments) and can impact performace. Data downloaded into this repertory should match the one from the pdfs files, wich is usually very easy to determine before starting the task by looking where the parcels are located (usually one single department).

## Description - Français
Ce script génère des couches de polygones, au format CSV/WKT, en associant l'information contenue dans deux types de fichiers :
* La Fiche de compte du CVI 'Casier Viticole Informatisé), en format pdf, qui est un document que tous les vignerons doivent avoir, édité par le service de la viticulture des Douanes
* Des couches géographiques du cadastre, au format GeoJSON

### Fichiers d'entrée
* Dans le répertoire "cvis" :
Introduire le ou les pdfs avec les parcellaires issus du CVI. Les vignerons peuvent les générer dans leur espace personnel sur le portail de la Douane (https://www.douane.gouv.fr)
* Dans le répertoire CADASTRE
Introduire le ou les fichiers JSON extraits du portail de données ouvertes du cadastre (https://cadastre.data.gouv.fr/datasets/cadastre-etalab).
Ces données peuvent être des départements entiers ou des communes individuelles. La taille de ces fichiers peut être importante (spécialeent pour les données des département) et peut impacter la performance. Les données dans ce répertoire doivent correspondre à celles des fiches de compte en pdf, ce qui est assez facile de déterminer en regardant dans le pdf dans quel département ou communes sont les parcelles (généralement, un seul département)

### Fichiers de sortie
Le script génère deux fichiers de sortie :
* output.csv
Ce fichier contient :
  * les données parcellaires primordiales du parcellaire douanier, c'est à dire :
    * Le numéro CVI associé à la parcelle
    * Le lieu-dit
    * Le code INSEE de la parcelle (Numéro de département + Numéro de commune + (Numéro ancienne commune) + Section + Numéro de parcelle)
    * Le vin qui peut-être produit
    * Le cépage
    * La surface (en hectares)
    * La campagne de plantation
    * La densité de plantation
  * Les données géographiques, avec les coordonnées des polygones au format WKT, ce qui permet d'utiliser le fichier avec des logiciels SIG.
* output_fail.csv

