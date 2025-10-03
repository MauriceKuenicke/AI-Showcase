import requests
from crewai.tools import tool
import os
import json
from dotenv import load_dotenv
import re

load_dotenv()

# Extract connection details from environment variables
sql_alchemy_conn = os.getenv("APP__SF__SQL_ALCHEMY_CONN")
if not sql_alchemy_conn:
    raise ValueError("Environment variable 'APP__SF__SQL_ALCHEMY_CONN' is not set.")

# Extract the organization account (text between '@' and '/')
org_account_match = re.search(r"@([^/]+)", sql_alchemy_conn)
org_account = org_account_match.group(1) if org_account_match else None
if not org_account:
    raise ValueError("Could not extract the account identifier from the connection string")

# Extract database (text after '/' but before the next '/')
database_match = re.search(r"@[^/]+/([^/]+)", sql_alchemy_conn)
database = database_match.group(1) if database_match else None

# Extract schema (text after the database '/' section)
schema_match = re.search(r"/([^/]+)$", sql_alchemy_conn)
schema = schema_match.group(1) if schema_match else None


MCP_BASE_URL = f"https://{org_account}.snowflakecomputing.com/api/v2/databases/{database}/schemas/{schema}/mcp-servers/MCP_SERVER"
OAUTH_TOKEN = os.getenv("APP__SF__ACCESS_TOKEN")
if not OAUTH_TOKEN:
    raise ValueError("Environment variable 'APP__SF__ACCESS_TOKEN' is not set.")
HEADERS = {
    "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
    "Authorization": f"Bearer {OAUTH_TOKEN}",
    "Content-Type": "application/json"
}

@tool("Invoke Search Query on MCP")
def call_mcp_analyst(query: str, filter: dict = None, limit: int = 5) -> str:
    """
    Use this tool to search the user feature requests using keyword search.
    This tool does not support SQL-based queries. This tool only supports keyword searches.
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "Get_Feature_Requests",
            "arguments": {
                "query": query,
                "filter": filter or {},
                "limit": limit,
                "columns": ["user_id", "message", "created_at"]
            }
        }
    }
    
    try:
        response = requests.post(MCP_BASE_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "result" in result:
            if "content" in result["result"] and isinstance(result["result"]["content"], list):
                if result["result"]["content"] and "text" in result["result"]["content"][0]:
                    return result["result"]["content"][0]["text"]
            elif "text" in result["result"]:
                return result["result"]["text"]
            elif isinstance(result["result"], str):
                return result["result"]
            else:
                return json.dumps(result["result"], indent=2)
        else:
            return f"Unexpected response format: {json.dumps(result, indent=2)}"
            
    except Exception as e:
        return f"Error calling MCP Analyst tool: {str(e)}"
