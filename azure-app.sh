#!/bin/bash

set -euo pipefail

. ./env-azure.sh

echo "Creating Application Service Plan...";
az appservice plan create \
    -g $resourceGroup \
    -n "linux-plan" \
    --sku B1 \
    --is-linux

echo "Creating Application Insight..."
az resource create \
    -g $resourceGroup \
    -n $appName-ai \
    --resource-type "Microsoft.Insights/components" \
    --properties '{"Application_Type":"web"}'

echo "Reading Application Insight Key..."
aikey=`az resource show -g $resourceGroup -n $appName-ai --resource-type "Microsoft.Insights/components" --query properties.InstrumentationKey -o tsv`

echo "Creating Web Application...";
az webapp create \
    -g $resourceGroup \
    -n $appName \
    --plan "linux-plan" \
    --runtime "PYTHON|3.7" \
    --deployment-source-url $gitSource \
    --deployment-source-branch $gitBranch \
    --startup-file startup.sh

COSMOSDB_PRIMARY_CONNECTION_STRING=`./azure-cosmosdb-connection-string.sh`

echo "Configuring Application Insights...";
az webapp config appsettings set \
    -g $resourceGroup \
    -n $appName \
    --settings \
        APPINSIGHTS_KEY="$aikey" \
        COSMOSDB_PRIMARY_CONNECTION_STRING="${COSMOSDB_PRIMARY_CONNECTION_STRING}"

echo "Done."
