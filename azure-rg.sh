#!/bin/bash

set -euo pipefail

# Make sure these values are correct for your environment
resourceGroup="dm-api-01"
location="WestUS2" 


echo "Creating Resource Group...";
az group create \
    -n $resourceGroup \
    -l $location


echo "Done."