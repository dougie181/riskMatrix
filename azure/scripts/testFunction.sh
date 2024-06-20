#!/bin/bash

# Variables
RESOURCE_GROUP="ResourceGroup"  # Resource group name - change as needed
FUNCTION_APP_NAME="riskMatrixFn"        # Function app name - change as needed
FUNCTION_NAME="HttpTriggerFunction"

DATA_FILE="data.json"

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Construct the full path to the data file
DATA_FILE_PATH="${SCRIPT_DIR}/${DATA_FILE}"

# Retrieve the base URL
BASE_URL=$(az functionapp function show --resource-group $RESOURCE_GROUP --name $FUNCTION_APP_NAME --function-name $FUNCTION_NAME --query 'invokeUrlTemplate' --output tsv)

# Retrieve the function key
FUNCTION_KEY=$(az functionapp function keys list --resource-group $RESOURCE_GROUP --name $FUNCTION_APP_NAME --function-name $FUNCTION_NAME --query 'default' --output tsv)

# Construct the full URL
FULL_URL="${BASE_URL}?code=${FUNCTION_KEY}"

echo "Testing function..."
curl -X POST $FULL_URL -H 'Content-Type: application/json' -d @$DATA_FILE_PATH --output example_risk_matrix.png

echo "Image saved as example_risk_matrix.png"

echo "done."