#!/bin/bash

export gitSource="https://github.com/biconou/python-api-azure.git"
gitBranch=`git branch --show-current`
export gitBranchSlug=`echo ${gitBranch} | tr -d '/'`
echo "gitBranchSlug=${gitBranchSlug}"

export resourceGroup="everie-${gitBranchSlug}-rg"
export appName="drop-api-${gitBranchSlug}"
export dbName="${appName}-db"
export location="francecentral"


# Sélection de l'abonnement à utiliser
export subscriptionId="a9fb73c8-d5b0-4bb7-812a-9da746a410e4" # id de la souscription everie
az account set -s ${subscriptionId}
