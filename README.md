# Projet d’étude : AgroVision

---

## À propos

---

Application web proposant une solution numérique appliquée au secteur agricole, en lien avec les problématiques de suivi des cultures, de gestion des ressources et d'aide à la prise de décision.

---

## Table des matières

---

- [A propos](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)
- [Outils utilisés](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)
- [Utilisation](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)
- [Contribution](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)

## Outils utilisés

---

→ [Table des matières](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)

La réalisation de ce projet nous a demandé de le diviser en diverses étapes. Pour commencer, nous avons réalisé le frontend en HTML/CSS et brièvement en JavaScript. Nous avons fait ce choix d'outils car il s'agit des langages frontend avec lesquels nous sommes le plus à l'aise. De plus, cela permet une bonne compatibilité avec le backend en Flask, micro-framework pour Python.

Quant au backend, nous l'avons donc réalisé en Python, par l'utilisation du micro-framework Flask. Ce choix se justifie par sa simplicité et sa légèreté, comparé à Django qui impose certains choix. De plus, Flask s'intègre facilement à SQLAlchemy.

Pour SQLAlchemy, sa structure simplifie le code. En effet, SQLAlchemy permet de ne pas mélanger du SQL et du Python. De plus, SQLAlchemy simplifie le changement de système de gestion de base de données, permettant de passer facilement de SQLite à PostgreSQL. Ainsi, SQLAlchemy nous a facilité le code ainsi que le déploiement de l'application.

Finalement pour le déploiement, nous avons utilisés Render. Cela nous a permis d'héberger la base de donnée, le code et de relier le tout à notre git. De plus, Render est un outil gratuit. 

## Utilisation

---

→ [Table des matières](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)

L'application web se divise en plusieurs pages, chacune répondant aux demandes du client.

La page d’accueil se présente ainsi : 

![image.png](/ProjectOfStudy/images_readme/image.png)

![image.png](/ProjectOfStudy/images_readme/image%201.png)

![image.png](/ProjectOfStudy/images_readme/image%202.png)

La page d'accueil sert à présenter les fonctionnalités disponibles sur l'application web.

On peut retrouver l'accès à la fonctionnalité de connexion via le bouton prévu à cet effet. On peut aussi retrouver un bouton permettant d'accéder au tableau de bord. Finalement, on retrouve une liste décrivant les fonctionnalités principales et les données requises.  

En voulant accéder à la page du tableau de bord, le bouton nous redirige automatiquement vers la page de connexion. Ainsi, sans authentification, il n'est pas possible d'accéder au tableau de bord.

Pour s'authentifier, il est nécessaire de rentrer les identifiants suivants :

[jean.dupont@agrovision.fr](mailto:jean.dupont@agrovision.fr)  dupont123

![image.png](/ProjectOfStudy/images_readme/image%203.png)

Une fois connecté, celle-ci nous redirige vers le dashboard.

![image.png](/ProjectOfStudy/images_readme/image%204.png)

![image.png](/ProjectOfStudy/images_readme/image%205.png)

![image.png](/ProjectOfStudy/images_readme/image%206.png)

Le dashboard intègre une fonctionnalité de filtre pour mieux se repérer. Le tableau de bord permet de visualiser les récentes alertes et observations reçues, ainsi que l'état des parcelles.

Il est aussi possible d'accéder à la page d'observations, d'alertes et de parcelles via le header.

![image.png](/ProjectOfStudy/images_readme/image%207.png)

Grâce à l'hébergement du site, il est possible d'ajouter une observation. Cette observation sera alors transmise au dashboard, mais aussi partagée aux autres utilisateurs.

![image.png](/ProjectOfStudy/images_readme/image%208.png)

Quant à la page d'alertes, celle-ci fonctionne via une API connectée à l'application web. Lors du lancement d'une nouvelle recherche, l'application envoie une requête à l'API, récupère les informations nécessaires et affiche une alerte si les seuils sont dépassés.

![image.png](/ProjectOfStudy/images_readme/image%209.png)

Finalement, pour les parcelles, le processus est le même que pour la page d'observations.

## Contribution

---

→ [Table des matières](https://www.notion.so/Projet-d-tude-AgroVision-358c0c1ef63580d7b37dcfeeb280bd84?pvs=21)

Pour le bon déroulement du projet, nous avons analysé le projet, puis réfléchi et proposé les tâches à réaliser. De ce fait, nous avons réalisé un schéma, à partir de l'outil Trello, suivant la méthode Kanban.

![image.png](/ProjectOfStudy/images_readme/image%2010.png)

Il s'agit, globalement, des tâches définies par l'équipe.

![image.png](/ProjectOfStudy/images_readme/image%2011.png)

Ramazan a mis en place de la pipeline Git, ainsi qu'à la page d'accueil, aidé de Robin.

Wakil a contribué à la création de la page de connexion et à la réalisation du MCD/MLD, aidé de Youcef.

Youcef a contribué à la création de la base de données, aidé par Robin, ainsi qu'à la réalisation du schéma d'architecture.

Robin a contribué à la création de la page d'accueil, aidé par Ramazan, et à la création de la base de données, aidé par Youcef.

![image.png](/ProjectOfStudy/images_readme/image%2012.png)

Ramazan a contribué à la création de la page du dashboard.

Wakil a crée la page de gestion des parcelles et cultures.

Youcef a terminé la création de la BDD, et a réalisé le responsive.

Robin a contribué à la création de la page d'observations et de suivi.

![image.png](/ProjectOfStudy/images_readme/image%2013.png)

Ramazan a terminé la page de dashboard, aidé de tout le groupe. De plus, il a corrigé et nettoyé le code, aidé par Robin et Wakil.

Wakil a réalisé le README.md.

Youcef a terminé le responsive et a contribué au déploiement de la base de données sur le cloud, ainsi qu'à l'hébergement du site, aidé de Ramazan.

Robin a réalisé la page d'alertes.

![image.png](/ProjectOfStudy/images_readme/image%2014.png)

Wakil a terminé le README.md.

Le groupe a vérifié que la version finale fonctionne et a réalisé la vidéo.

![image.png](/ProjectOfStudy/images_readme/image%2015.png)

Avec plus de temps, nous aurions ajouté d'autres fonctionnalités. Ces fonctionnalités sont à prévoir pour une v2.