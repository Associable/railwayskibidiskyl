# Skibidi Data API Documentation

**Base URL**: `https://railwayskibidiskyl-production.up.railway.app`  
**Authentication**: API Key (`X-API-KEY: zyniscool`)

## Table of Contents
1. [API Overview](#api-overview)
2. [Endpoints](#endpoints)
3. [Authentication](#authentication)
4. [Data Formats](#data-formats)
5. [Error Handling](#error-handling)
6. [Rate Limits](#rate-limits)
7. [Examples](#examples)

## API Overview <a name="api-overview"></a>
A simple REST API for storing and retrieving map configuration data with:
- JSON request/responses
- API key authentication
- Persistent storage
- Filtering capabilities

## Authentication <a name="authentication"></a>
Include API key in either:
```http
X-API-KEY: zyniscool
```
or as query parameter:
```
?apikey=zyniscool
```

## Endpoints <a name="endpoints"></a>

### 1. Status Check
```http
GET /status
```
**Response**
```json
{
  "status": "OK",
  "environment": "production",
  "data_entries": 15
}
```

### 2. Store Data
```http
POST /store
```
**Request Body**
```json
{
  "map_name": "desert",
  "act_name": "exploration",
  "preferred_units": "imperial"
}
```
**Successful Response (201)**
```json
{
  "message": "Data stored successfully",
  "id": 16
}
```

### 3. Retrieve Data
```http
GET /retrieve
```
**Query Parameters**
| Parameter | Description |
|-----------|-------------|
| map_name | Filter by map name |
| act_name | Filter by act name |
| preferred_units | Filter by units |

**Response (200)**
```json
{
  "count": 3,
  "results": [
    {
      "map_name": "desert",
      "act_name": "exploration",
      "preferred_units": "imperial",
      "timestamp": "2023-09-15T14:30:00Z"
    }
  ]
}
```

## Data Formats <a name="data-formats"></a>
**Data Object**
```json
{
  "map_name": "string (required)",
  "act_name": "string (required)",
  "preferred_units": "string (required)",
  "timestamp": "ISO 8601 (auto-generated)"
}
```

## Error Handling <a name="error-handling"></a>
**Common Errors**
```json
{
  "error": "Invalid API key",
  "code": 401
}

{
  "error": "Missing required fields",
  "code": 400
}

{
  "error": "Data file corrupted",
  "code": 500
}
```

**Status Codes**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

## Rate Limits <a name="rate-limits"></a>
- 60 requests/minute
- Burst: 10 requests/5 seconds

## Examples <a name="examples"></a>

**Lua (using LuaSocket)**
```lua
local http = require("socket.http")
local json = require("json")

local data = {
  map_name = "caves",
  act_name = "mining",
  preferred_units = "metric"
}

local response, status = http.request{
  url = "https://railwayskibidiskyl-production.up.railway.app/store",
  method = "POST",
  headers = {
    ["X-API-KEY"] = "zyniscool",
    ["Content-Type"] = "application/json"
  },
  source = ltn12.source.string(json.encode(data))
}
```

**Python**
```python
import requests

response = requests.get(
  "https://railwayskibidiskyl-production.up.railway.app/retrieve",
  headers={"X-API-KEY": "zyniscool"},
  params={"map_name": "desert"}
)
```

**cURL**
```bash
# Store data
curl -X POST \
  -H "X-API-KEY: zyniscool" \
  -H "Content-Type: application/json" \
  -d '{"map_name":"forest","act_name":"hunting","preferred_units":"metric"}' \
  https://railwayskibidiskyl-production.up.railway.app/store

# Retrieve filtered data
curl "https://railwayskibidiskyl-production.up.railway.app/retrieve?map_name=forest&apikey=zyniscool"
```

---


**Version**: 1.0.0  
```
