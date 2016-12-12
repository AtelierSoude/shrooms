# Cahier des charges SHROOMS

**Self Hostable Reticulate Open-source Organisations Management (eco-)System**

## Besoins

Nécessité d’un outil de type ERP **associatif**,  **collaboratif** (au niveau des individus et des organisations), facilitant la **communication** et la **mise en commun** des informations et des moyens. 

Placer l’**utilisateur au centre** du système, avec pour objectif un maximum de transparence et d’implication au sein des structures.

Gérer le **fonctionnement interne des organisation**s (conciergerie numérique, gestion des stocks etc...)

**Décentralisé** : chaque organisation héberge une instance ; mais **connecté** : chaque instance peut communiquer avec les autres instances connues.

## Contenu

### Fonctionnalités

*   **Modules** : choix de modules à activer à l’installation, idéalement pouvoir customiser le contenu d’un module (ex : de quelles données a-t-on besoin sur une pièce ?)
    *   Personnes
    *   Stocks
    *   Réparations
    *   Projets
    *   Evenements
    *   Localisations
    *   Comptabilité / Cotisations
    *   CMS Django
    *   Notifications mail
    *   Blog wordpress
    *   Forum
    *   Liste extensible...
*   **Intégration web**
    *   Front end public (pour l’Atelier Soudé)
        *   Responsive (Bootstrap)
    *   Dashboard personnel
    *   **API Web**
    *   Analytics (SEO)
    *   Pluggable avec des outils collaboratifs : utiliser un PaaS type Dies, Sandstorm...
        *   Kanboard/Wekan
        *   Etherpad
        *   Rocket Chat
        *   Git (projets) : Jenkins ? 
        *   Hello Asso pour les cotisations ?
        *   Roundcube (mails)
        *   Partage de fichiers (cloud ? )
*   Tracabilité, suivi des actions, gestion de projets
*   Partageable entre les instances (cf [Cahier des charges SI Atelier Soud:](/1kkx4KRDSPu#:h=Interactions)) Interactions)

### Caractéristiques

*   Modulaire
*   Distribuable
*   Libre et open source
*   Sécurisé (SSL)

### Interactions entre instances

Chaque association dispose d’une instance de l’outil. Les admins décident quelles instances sont liées à leur propre système de données par un système d’invitation à partager ses données entre organisations. Chaque utilisateur peut alors choisir parmi toutes les instances liées à partir desquelles obtenir les données (ex : recherche de matériel chez différentes assos). Ce fonctionnement permet à l’utilisateur de paramétrer sa propre UX dans une certaine mesure.

*   Partage des utilisateurs (LDAP)
    *   Un seul compte utilisateur pour accéder à toutes les instances (type stack exchange).
    *   Gestion des accès, droits type UNIX.
*   Partage du matériel (pièces, appareils, outils, kits de réparation...)
*   Gestion des prêts, localisation du matériel
*   Idéalement unification des plugins collaboratifs pour un utilisateur (faisable ?)

## Contraintes

### Développement

*   Utiliser du libre et open source au maximum
*   Temps humain
*   Equipe restreinte
*   Code modulaire, respectant l’architecture MVC
    *   Séparation backend / frontend (django backend, frontend angularJS + boostrap + Sass)

### Fonctionnement

*   Simple d’utilisation, intuitif
    *   Proposer un installateur pour le choix des modules à activer pour chaque instance
*   Personnalisable (thème, contenu du dashboard)
*   Workflows : l’ensemble des fonctionnalités devrait être trackable par un système de commentaires, changement de statuts

## Roadmap

### Base 0.1

* **Backend**

    * Gestion des utilisateurs + workflow
    * Gestion des droits
    * Gestion des instances
    * Gestion des adresses
    * Partage de données entre instances (LDAP)
    * Inscription + validation mail

* **Frontend**
    * Interface de gestion des utilisateurs (ADMIN)
    * Interface de l’utilisateur (USER)
    * Invitations cross-instances
    * Workflow des modifications utilisateur
    * Integration GMaps (like ?)

![hackpad.com_1kkx4KRDSPu_p.372236_1481477948549_maquette-loginPlan de travail 1.jpg](https://bitbucket.org/repo/KEoX8d/images/847385315-hackpad.com_1kkx4KRDSPu_p.372236_1481477948549_maquette-loginPlan%20de%20travail%201.jpg)

### Base 0.2
*   **Backend**
    * Gestion de facturation (cotisations) automatique

*   **Frontend**
    * Interface de gestion et édition de facturation + devis 
    * Export PDF facturation (voire automatique sur cloud)

### Base 0.3
*   **Backend**
*   **Frontend**
