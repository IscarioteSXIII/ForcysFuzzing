# Main GUI - Regroupement des différents bout de code.

Features intégrées:
- Interface Graphique (Enzo P)
- Network Scanner (Enzo P)
- Crawler HTTP(s) (Enzo P)
- DDOS (Julien D)

Dépendances :
- NMAP 7.92 - /!\ La version 7.93 n'est pas compatible
- Librairie "requests"
- Librairie "bs4"
- Librairie "scapy"

```
python -m pip install [librairie]
```

Les codes sources Fuzzing Web et Fuzzing SQL n'ont pas été implémentés au code Main.py.

La mise en place graphique ayant été faite sur Windows, certaines librairies n'ont pas été installées empêchant le code de fonctionner. Les codes sources sont néanmoins disponible dans le repo GitHub.


# Utilisation de l'application

Network Scanner :
- Définir la cible (Host ou Network)
- Sélectionner le type de scan ---> La commande est modifiable au besoin
- Lancer le scan et attendre le résultat
![image](https://user-images.githubusercontent.com/102690258/202221652-b8b53db3-01dc-4726-b728-3b5c03063e62.png)

Crawler HTTP(s) :
- Définir l'URL cible
- Choisir une option de crawling ---> Une option à la fois
![image](https://user-images.githubusercontent.com/102690258/202222026-84f3e002-26b8-4a4e-a47e-f910eddbe922.png)

DDOS :
- Définir l'IP cible
- Enjoy :)
![image](https://user-images.githubusercontent.com/102690258/202222221-837e871a-1484-4f53-9523-1a6ef8b0e87c.png)

