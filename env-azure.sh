#!/bin/bash

export gitSource="https://github.com/biconou/python-api-azure.git"
gitBranch=`git branch --show-current`
echo ${gitBranch}
export gitBranchSlug=`echo ${gitBranch} | tr -d '/'`
echo ${gitBranchSlug}

export resourceGroup="everie-${gitBranchSlug}-rg"
export appName="drop-api-${gitBranchSlug}"
export dbName="${appName}-db"
export location="francecentral"


# Sélection de l'abonnement à utiliser
export subscriptionId="72d0710a-c7cd-4924-9e3f-8a8272e2515a" # id de la souscription everie
az account set -s ${subscriptionId}
