# Projet_WEB_ETRS711

Projet Web Conception et Programmation Orientée Objet d’une application web (Cave à Vin)

# Diagramme UML

![test.png](Projet_WEB_ETRS711%20aa50fe36c8d74659898eccebaf32468a/test.png)

1. La classe **`Utilisateur`** est associée à la classe **`Cave`** avec une relation d'agrégation (agrégation composite). Cela signifie qu'un utilisateur peut posséder plusieurs caves, et chaque cave appartient à un utilisateur. L'association est représentée par une flèche entre les deux classes avec le losange noir du côté de la classe **`Utilisateur`**.
2. La classe **`Cave`** est associée à la classe **`Etagere`** avec une relation d'agrégation (agrégation composite). Cela signifie qu'une cave peut contenir plusieurs étagères, et chaque étagère appartient à une cave. L'association est représentée par une flèche entre les deux classes avec le losange noir du côté de la classe **`Cave`**.
3. La classe **`Etagere`** est associée à la classe **`Bouteille`** avec une relation d'agrégation (agrégation composite). Cela signifie qu'une étagère peut contenir plusieurs bouteilles, et chaque bouteille est stockée sur une étagère. L'association est représentée par une flèche entre les deux classes avec le losange noir du côté de la classe **`Etagere`**.
4. La classe **`Bouteille`** a des méthodes pour ajouter, supprimer, obtenir et mettre à jour des bouteilles sur une étagère, ce qui est reflété par les flèches pointant vers les opérations de ces méthodes.
5. Les classes **`Utilisateur`**, **`Cave`**, **`Etagere`**, et **`Bouteille`** sont associées à la classe **`EtagereBouteille`** avec une relation d'agrégation (agrégation composite). Cela signifie qu'il existe une table de liaison **`EtagereBouteille`** pour gérer les associations entre ces classes. L'association est représentée par une flèche entre les classes principales et la classe **`EtagereBouteille`** avec le losange noir du côté de chaque classe principale.

# Structure du projet

## Définition des Classes

Les classes sont présentes dans le dossier models du projet.

Les actions faits en DB sont développées dans ces fichiers

il y a 5 fichiers **[init.py](http://init.py), bouteille.py, cave.py, [etagere.py](http://etagere.py) et utilisateur.py**

## Application Route

les routes de l’application sont définies dans le dossier views

C’est dans ces différents fichiers que sont définies les routes contenant les fonctionnalités de l’application.

### Bouteille.py

contient une route `@bouteille_routes.route("/ajouter_bouteille", methods=["GET", "POST"])` afin d’ajouter une bouteille a la liste Globale de bouteilles présentes dans l’application.

contient une route `@bouteille_routes.route("/supprimer_bouteille/<int:id_bouteille>", methods=["GET", "POST"])` permettant de supprimer une bouteille de liste Globale de bouteilles présentes dans l’application. (il faut entrer l’url a la main pour l’instant)

### Cave.py

contient une route `@cave_routes.route("/creer_cave", methods=["GET", "POST"])` afin de créer une cave et une route `@cave_routes.route("/supprimer_cave/<int:id_cave>", methods=["GET", "POST"])` afin de supprimer une cave 

### Etagere.py

contient une route pour `@etagere_routes.route("/creer_etagere", methods=["GET", "POST"])` pour créer une etagère et une route `@etagere_routes.route("/supprimer_etagere/<int:id_etagere>", methods=["GET", "POST"])` pour la supprimer

deux autres routes afin d’ajouter une bouteille à une étagère spécifique et inversement :
`@etagere_routes.route("/etagere/<int:id_etagere>/ajouter", methods=["GET", "POST"])`

`@etagere_routes.route("/etagere/<int:id_etagere>/supprimer", methods=["GET", "POST"])`

### Utilisateur.py

contient la route pour se connecter :

`@utilisateur_routes.route("/login", methods=["GET", "POST"])`

la route pour se déconnecter : `@utilisateur_routes.route("/deconnexion", methods=["GET"])`

la route pour créer un compte client `@utilisateur_routes.route("/register", methods=["GET", "POST"])`

la route pour supprimer un utilisateur : `@utilisateur_routes.route("/supprimer_utilisateur", methods=["GET", "POST"])` (fonctionnelle mais pas de formulaire créé encore)

### Sécurité

Pour chaque page il faut etre authentifié avant tout accès grace a `logged_in`

Les mots de passe sont hachés à l’aide de bcrypt avant d’etre stockés en base de donnée

 L’authentification se fait donc en comparant le hash du mot de passe entré avec celui en base de donnée 

# Evolutivité

-Pouvoir afficher les commentaires sur chaque bouteille

-Afficher une page informative sur les bouteilles, la note moyenne, image, description etc…

-Faire un système d’archivage de bouteille

-Afficher les infos en json

-Avoir un panel Admin

-Système de tri des bouteilles