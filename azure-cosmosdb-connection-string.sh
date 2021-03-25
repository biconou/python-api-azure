#!/bin/bash

# Inspired by : https://docs.microsoft.com/en-us/azure/cosmos-db/scripts/cli/common/keys

resourceGroupName=${resourceGroup}
accountName=${dbName}

# List connection strings
az cosmosdb keys list \
    -n $accountName \
    -g $resourceGroupName \
    --type connection-strings \
| jq '.connectionStrings[] | select(.description=="Primary MongoDB Connection String").connectionString' \
| tr -d '\"'
