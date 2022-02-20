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

### Output files
This script generates 2 output files :
* output.csv
It contains :
  * Data from the custom's files :
    * The CVI number associated to the parcel (a customs' id number referencing the wine grower)
    * The locality (lieu-dit in French)
    * INSEE code of the parcel (départment number + Town number + (Former town number) + Section + Parcel number)
    * The kind of wine that can be produced
    * The grape variety
    * The area (in hectares)
    * Year of planting
    * Density
  * Geographical data, with polygon coordinates in WKT format, wich allows use with GIS software
* output_fail.csv
This file contains data that could not be associated to land registry information

### Known causes of failure during data association
Parcels can be written in the "output_fail.csv" file for several reasosn :
* The town file is not in the CADASTRE repertory :
* In this case, just add it to repertory. **Make sure the file is decompressed** and that it has a .json extensin.

* Main reason of failure during data association is that the Customs' file may not be up-to-date, sometimes, it can lack updates from over few years (Public service excellence, my friend !). Here are some more or less common cases :
  * The parcel changed number because the winegrower modified it (parcel splitted for example). New references can be used using Geoportail (geoportail.gouv.fr). If this happens for very little parcels, you can try drawing them with your GIS software and manually enter data. If the parcel was moodified recently, you can try downloading a older version of the land registry and place it in the CADASTRE folder.
  * Land Registry info changed for the whole town (or whole sections). Here your best option is to find a previous version of the land registry information.
  * Town does not exist anymore: This usually happens when 2 towns merge into one (usually, around municipal elections). You can either try to download an older version of the land registry, hen the town existed, or try using this piece of code into the script (after line 29) :
  `if row[1][3:6] == "XXX" :
                        insee_code = row[1][:2] + "YYY" + row[1][3:6] + row[1][-6:]`
  **Where "XXX" is the INSEE code of disappeared town and "YYY" is the code of the new town**.

### A word about the parcel generated
Data in the customs's document references vines, wich can be planted (they usually are) only in certain parts of a land regstry parcel.
This means that the output file can have several overlapped parcels. 
This is inconvinient, but (my) experience has shown (me) that having this task automated up to this limit makes it way easier and faster to generate a complete parcel file by just modifieng layer corners with GIS software.
Also, for some tasks, the output data can be directly used since the area column (surface) has the proper information from the customs' file.

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
Ce fichier contient les informations du parcellaire qui n'ont pas pu être associées aux informations du cadastre

### Causes possibles d'échec dans l'association des données
Les parcelles peuvent être inscrites dans le fichier "output_fail.csv" pour plusieurs raisons :
* Il manque la commune dans le répertoire CADASTRE
Il suffit donc de rajouter la commune (ou le département entier) dans le répertoire. **Vérifiez que le document téléchargé a bien été dézippé** et que son extension est ".json"
* La principale raison d'échec dans l'Association des parcelles reste la mise à jour du document parcellaire douanier. L'information contenue dans les ficiers peut parfois avoir des non-mises à jour de plusieurs années (c'est de l'administration publique, my friend !). Voici quelques écarts communs et des pistes pour y remédier (+/- solutions manuelles...)
  * La parcelle a été recadastrée par le vigneron (par exemple, suite à une division de la parcelle) : Vous pouvez trouver les nouvelles référence en utilisant le Geoportail (geoportail.gouv.fr). S'il s'agit de très peu de parcelles, vous pouvez les dessiner à la main avec un logiciel SIG. Si la modification est récente, peut-être pouvez-vous télécharger une verion plus ancienne du cadastre de la commune.
  * La commune a été recadastrée : Dans ce cas, toutes les sectins et les pas parcelles d'une commune (ou partie de commune) ont changé. La meilleur option est d'essayer de retrouver une version du cadastre d'avant le changement
  * La commune n'exite plus : Dans ce cas, la commune a probablement fusionné avec d'autres (les dates correspondent généralement aux élections municipales). Il faut essayer de retrouver une version ancienne de la commune ou essayer d'ajouter ce bout de code au script (après la ligne 29) :
  `if row[1][3:6] == "XXX" :
                        insee_code = row[1][:2] + "YYY" + row[1][3:6] + row[1][-6:]`
   **où "XXX" est le code de la commune ayant disparu et "YYY" est le code de la nouvelle commune**.
   **Pensez aussi au "else" juste après...**.

### Au sujets des parcelles générées par le programme
Les données dans le document des douanes référence des parcelles de vigne, qui peuvent être plantées (et c'est souvent le cas) dans des parties précises de la parcelle cadastrale. Une même parcelle cadastrale peut donc accueillir plusieurs bouts de parcelle de vigne...
Ceci veut donc dire que le fichier de sortie put avoir beaucoup de parcelles superposées.
C'est un inconvénient notable, mais mon expérience me montre qu'il vaut mieux avoir automatisé la tâche jusque là car elle rend le résultat final (générer un parcellaire complet) plus rapide s'il ne reste plus que des bouts de polygone à modifier avec un logiciel SIG.
D'autre part, pour certaines utilisation, le résultat final est suffisant car les données de surface sont celles extraites dans le parcellaire des douanes.
This means that the output file can have several overlapped parcels. 

## Test output opened with QGis / Sortie du test ouverte avec QGis

![Output 1](https://github.com/enarroied/cvi_geometry/blob/main/test/out1.png)

![Output 2](https://github.com/enarroied/cvi_geometry/blob/main/test/out2.png)
