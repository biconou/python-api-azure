#!/bin/bash
. ../env-azure.sh  # Provides appName

. ./get_token.sh  # Provides access_token

endpoint='/events/'
# Events endpoint
curl -X 'POST' \
  "https://${appName}.azurewebsites.net${endpoint}" \
  --header "Authorization: Bearer ${access_token}" \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  -d '{
    "drop": "test",
    "data": [
      {
        "time": 1618844679,
        "type": "Battery",
        "Battery1State": "Empty",
        "Battery2State": "Active"
      }
    ]
  }'
