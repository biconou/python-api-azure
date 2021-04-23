#!/bin/bash
. ../env-azure.sh  # Provides appName

. ./get_token.sh  # Provides access_token

endpoint='/config/'

curl -X 'POST' \
  "https://${appName}.azurewebsites.net${endpoint}" \
  --header "Authorization: Bearer ${access_token}" \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  -d '{
    "target_drops": [
      "test",
    ],
    "config": {
      "version": "test-config",
      "config": {
        "DropQtyToDeliver": "4",
        "MaxDeliveryDelay": "3",
        "TransmissionPeriod": "2000"
      }
    }
  }'

curl -X 'GET' \
  "https://${appName}.azurewebsites.net${endpoint}?drop=test" \
  --header "Authorization: Bearer ${access_token}" \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
