
# Introduction

Ce code est basé sur : https://docs.microsoft.com/fr-fr/samples/azure-samples/azure-sql-db-python-rest-api/azure-sql-db-python-rest-api/


# Instruction pour les développeurs


## Installer AZURE cli

## Initialiser l'environnement

Après avoir cloné le repo il faut initialiser l'environnement en lançant le script

```
./install.sh
```

Le fichier .pre-commit-config.yaml est untlise


## lancer l'application

Il faut d'abord charger les variables d'environnement locales pour l'interaction avec la base de donnée MongoDB
```
./env-local.sh
```

Puis lancer le script de démarrage
```
./startup.sh
```

# Déploiement sur AZURE

## Se loguer sur AZURE
```
az login
```

## Initialiser les variables d'environnement et la souscription courante
```
./env-azure.sh
```

## Créer le groupe de ressources
```
./azure-rg.sh
```

## Créer le compte CosmosDB

Le nom du compte CosmosDB se trouve dans la variable d'environnement __${dbName}__

Dans le portail AZURE créer un compte Cosmos DB en s'inspirant de la compie d'écrans suivante :

![](./docs/ecran-creation-cosmodb.png)

Créer la collection en lançant le script suivant

```
./azure-cosmodb.sh
```

Documentation sur la chaine de connextion
https://docs.microsoft.com/en-us/azure/cosmos-db/scripts/cli/common/keys

## Déployer l'application

```
./azure-app.sh
```

## Paramétrer l'application

Voir la documentation suivante :
https://docs.microsoft.com/en-us/azure/app-service/configure-common#application-settings


## Mettre à jour l'application

- Dans le portail AZURE aller sur l'application puis dans le "Centre de déploiement"
- Cliquer sur Redéployer/synchroniser
