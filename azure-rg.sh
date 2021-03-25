#!/bin/bash

set -euo pipefail


echo "Creating Resource Group...";
az group create \
    -n $resourceGroup \
    -l $location


echo "Done."
