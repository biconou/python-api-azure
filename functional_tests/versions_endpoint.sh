#!/bin/bash
. ../env-azure.sh  # Provides appName

. ./get_token.sh  # Provides access_token

endpoint="/versions/"
curl -X 'GET' \
  "https://${appName}.azurewebsites.net${endpoint}?drop=test" \
  --header "Authorization: Bearer ${access_token}" \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
