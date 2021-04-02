#!/bin/bash

. ./env-azure.sh

response=$(curl --location --request POST "https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token" \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "client_id=${clientId}" \
    --data-urlencode "scope=${clientId}/.default" \
    --data-urlencode "client_secret=${clientSecret}" \
    --data-urlencode 'username=DROP-5EFF56A2AF15@everie.com' \
    --data-urlencode 'password=g5fQO3NgOwz0Wnab2pRv' \
    --data-urlencode 'grant_type=password')

echo ${response} | jq

access_token=$(echo ${response} | jq .access_token | tr -d '"')
echo ""
echo "${access_token}"
echo ""


curl -X 'GET' \
  'https://drop-api-master.azurewebsites.net/pschit/' \
  --header "Authorization: Bearer ${access_token}" \
  --header 'accept: application/json'
