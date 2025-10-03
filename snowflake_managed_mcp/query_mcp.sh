#!/bin/bash


set -o allexport
source .env
set +o allexport
sql_alchemy_conn="$APP__SF__SQL_ALCHEMY_CONN"
access_token="$APP__SF__ACCESS_TOKEN"

# Ensure these variables are not empty
if [[ -z "$sql_alchemy_conn" || -z "$access_token" ]]; then
  echo "Required environment variables are missing in .env file"
  exit 1
fi

# Extract the section between '@' and '/' in the connection string
org_account=$(echo "$sql_alchemy_conn" | sed -n 's/.*@\([^/]*\).*/\1/p')
if [[ -z "$org_account" ]]; then
  echo "Could not extract the account identifier from the connection string"
  exit 1
fi

# Extract database and schema from the connection string
database=$(echo "$sql_alchemy_conn" | sed -n 's~.*/\([^/]*\)/.*~\1~p')
schema=$(echo "$sql_alchemy_conn" | sed -n 's~.*/[^/]*/\([^/]*\)~\1~p')

if [[ -z "$database" || -z "$schema" ]]; then
  echo "Could not extract database or schema from the connection string"
  exit 1
fi

echo "Running against:"
echo "Organization Account: $org_account"
echo "Database: $database"
echo "Schema: $schema"
echo "Sending request to: https://${org_account}.snowflakecomputing.com/api/v2/databases/${database}/schemas/${schema}/mcp-servers/MCP_SERVER"

curl -X POST "https://${org_account}.snowflakecomputing.com/api/v2/databases/${database}/schemas/${schema}/mcp-servers/MCP_SERVER" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header "Authorization: Bearer ${access_token}" \
  --data '{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "tools/list",
    "params": {}
  }'