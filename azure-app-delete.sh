#!/bin/bash


. ./env-azure.sh

echo "Deleting Web Application...";
az webapp delete \
    -g $resourceGroup \
    -n $appName

echo "Deleting Application Insight..."
az resource delete \
    -g $resourceGroup \
    -n $appName-ai \
    --resource-type "Microsoft.Insights/components"


echo "Done."
