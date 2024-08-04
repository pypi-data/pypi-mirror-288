# MIT Docs

Qu'es que veut dire CHC ?

sa veut dire **Client_server Http_server and Screen_sharing_server.**

## Client_server 

Client_server est un hébergeur de serveur tcp local.

Pour éxécuter le serveur faite un environement de variable systeme sur votre pc avec le chemin qui va au fichier python de client_server.

Puis executer cette commande :

```bash
    py {votre_nom_de_variable_environement}
```

## Http_server

Http_server et pour héberger des site web local et pouvoir les partager a tout le monde ne faisent que 2 cmd.

Voici le menu qui s'affiche a l'éxécution :

```
------ Menu -------  
1. start server
2. start héberger

entrer votre choix: 
```

faite le 1 pour commencer a héberger votre server localement.

Si vous voulais faire un server local accesible a tous vous devrez faire 2 dans une deuxième console (cmd) et quand vous retomber sur ce menu tapé 2.

Verifier sur vous avez bien installez [ngrok](https://ngrok.com) pour faire cette options

## Screen_sharing

Vous permet de faire un partage d'écran avec une personne local (chez vous). Si vous voulais partager votre camera en ligne tapez cette commandes et installez ngrok avant d'éxécuter la commande

```bash
ngrok tcp 9999
```


## Les prérequis avant l'éxecutions

1. Vous devrez installez les packages en faisent :

```bash
pip install -r requirements.txt
```

2. Installer [ngrok](https://ngrok.com)

3. Installer [git](https://git-scm.com) pour update le dépôt github

## Installez les updates 

Pour installez les updates entrer la commandes suivante : 

```bash
python install_update.py
```