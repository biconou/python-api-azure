#!/bin/bash

set -euo pipefail

# Inspiré de :
# https://docs.microsoft.com/fr-fr/azure/cosmos-db/scripts/cli/mongodb/create



# Variables for MongoDB API resources
resourceGroupName=${resourceGroup}
accountName=${dbName}
serverVersion='3.6' #3.2 or 3.6
databaseName='drops'
collectionName='pschit'



# Create a Cosmos account for MongoDB API
# D'après la documentation suivante https://docs.microsoft.com/en-us/azure/cosmos-db/serverless#using-serverless-resources
# on ne peut pas créer de compte Cosmos DB par script. Il faut passer par le portail pour créer le compte.
# " During the preview release, the only supported way to create a new serverless account is by using the Azure portal."
# Manifestement c'est un mode de fonctionnement tout neuf
# az cosmosdb create \
#     -n $accountName \
#     -g $resourceGroupName \
#     --kind MongoDB \
#     --server-version $serverVersion \
#     --default-consistency-level Eventual \
#     --locations regionName=${location} isZoneRedundant=False
#     # --locations regionName='West US 2' failoverPriority=0 isZoneRedundant=False \
#     # --locations regionName='East US 2' failoverPriority=1 isZoneRedundant=False

echo "Vérifier qu'il existe un compte CosmosDB type mongo en mode serverless"
echo "nom du compte : ${accountName}"
echo "Appuyez sur Enter si c'est ok ou ctrl-c sinon"
read

# Create a MongoDB API database
az cosmosdb mongodb database create \
    -a $accountName \
    -g $resourceGroupName \
    -n $databaseName

# # Define the index policy for the collection, include unique index and 30-day TTL
# idxpolicy=$(cat << EOF 
# [ 
#     {
#         "key": {"keys": ["user_id", "user_address"]}, 
#         "options": {"unique": "true"}
#     },
#     {
#         "key": {"keys": ["_ts"]},
#         "options": {"expireAfterSeconds": 2629746}
#     }
# ]
# EOF
# )
# # Persist index policy to json file
# echo "$idxpolicy" > "idxpolicy-$uniqueId.json"

# Create a MongoDB API collection
az cosmosdb mongodb collection create \
    -a $accountName \
    -g $resourceGroupName \
    -d $databaseName \
    -n $collectionName
    # --shard 'user_id' \
    # --throughput 400 \
    # --idx @idxpolicy-$uniqueId.json

# # Clean up temporary index policy file
# rm -f "idxpolicy-$uniqueId.json"

echo "Done."

