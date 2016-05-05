# cdbucket-project

##Petit Memo des commandes :
Pour chacune des commandes si dessous, 3 prefixes sont possible selon la configuration de votre machine.
Exemple avec la commande manage.py :
```
manage.py
```
ou
```
python manage.py
```
ou encore
```
./manage.py
```

A vous de voir quelle commande utiliser.
N'oubliez pas de vous placer dans le repertoire ou se trouve le fichier **manage.py**

###Lancer le serveur web Django:
    manage.py runserver

Notez que vous devez avoir au préalable **lancé vos serveurs de base de données pour que le tout fonctionne correctement**.
Vous pouvez ensuite accéder a vos pages à l'addresse [127.0.0.1:8000/](http://127.0.0.1:8000/) suivi des urls correspondantes dans le fichier **urls.py**

####Conseil pratique:
Lorsque vous réalisez des modifications de fichier, **le serveur recompile automatiquement les fichiers modifiés**. Pas besoin de le relancer, sauf dans le cas des
modifications apportés au modèles comme expliqué ci dessous.

###Enregistrer des modifications apportés au modèles:
    manage.py makemigrations

Cette commande parcours le fichier **models.py** et crée un fichier contenant les modifications a apporter lors de la prochaine migration.
Avant de lancer cette commande, **assurez vous d'avoir arrété le serveur Web Django (Ctrl+C dans la console du serveur web.)**

###Réaliser une migration:
Apres avoir enregistré des modifications du modele, il faut réaliser physiquement ces modifications sur la base de donnée.
Pour se faire, utiliser la commande
```
manage.py migrate
```

###Creer un super utilisateur:
Pour pouvoir utiliser le module d'administration de Django, il vous faudra créer un super-utilisateur. Pour se faire, utilisez la commande
```
manage.py createsuperuser
```
Renseignez ensuite les informations demandées par le prompt du terminal.
