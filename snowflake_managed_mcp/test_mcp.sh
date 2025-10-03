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
echo "Sending requests to: https://${org_account}.snowflakecomputing.com/api/v2/databases/${database}/schemas/${schema}/mcp-servers/MCP_SERVER"


echo -e "\n\n################################################################################"
echo -e "################################################################################"
echo -e "--- Stage 1: Checking Available MCP Server Tools ---"
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

echo -e "\n\n################################################################################"
echo -e "################################################################################"
echo -e "--- Stage 2: Querying Cortex Search Service ---"
curl --location "https://${org_account}.snowflakecomputing.com/api/v2/databases/${database}/schemas/${schema}/cortex-search-services/feature_request_search:query" \
	--header 'X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN' \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--header "Authorization: Bearer ${access_token}" \
	--data '{
		"query": "Show me the feature requests that ask for UI enhancements.",
		"columns": ["MESSAGE", "USER_ID", "CREATED_AT"],
		"limit": 10
	}'

echo -e "\n\n################################################################################"
echo -e "################################################################################"
echo -e "--- Stage 3: Calling the MCP Tool ---"
curl -X POST "https://${org_account}.snowflakecomputing.com/api/v2/databases/${database}/schemas/${schema}/mcp-servers/MCP_SERVER" \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--header "Authorization: Bearer ${access_token}" \
  --data '{
             "jsonrpc": "2.0",
             "id": 123456,
             "method": "tools/call",
             "params": {
                 "name": "Get_Feature_Requests",
                 "arguments": {
                     "query": "Show me the feature requests that ask for an update of the UI."
                 }
             }
       }'