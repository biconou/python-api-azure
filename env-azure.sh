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

# Pour l'authentification
export clientId="0077cc8c-b2a3-4ec0-bd91-784fdf4f5f3d" # id de l'application cliente
export clientSecret="dhLy3AlgW3S_MpTfnEZ-_05g_G-Oy2LT1o"
export tenantId="eadd0adf-e413-414f-a21a-86169869dcb1" # id du locataire Active Directory
