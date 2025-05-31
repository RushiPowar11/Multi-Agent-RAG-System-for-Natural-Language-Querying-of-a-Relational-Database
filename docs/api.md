# API Documentation

## Base URL
`http://localhost:8000`

## Authentication
Currently, no authentication is required for API endpoints. However, you need to have valid API keys configured in your environment variables.

## Endpoints

### 1. Get Web Interface
```http
GET /
```

Returns the HTML web interface for interacting with the system.

#### Response
- **Content-Type**: `text/html`
- **Status Code**: 200 OK

### 2. Process Query
```http
POST /ask
```

Process a natural language query and return structured results.

#### Request Body
```json
{
  "question": "string"
}
```

#### Response Body
```json
{
  "answer": "string",
  "error": "string | null",
  "error_type": "api_quota | database | unknown | null",
  "intermediate_steps": {
    "relevant_tables": ["string"],
    "generated_sql": "string",
    "query_results": [
      {
        "column1": "value1",
        "column2": "value2"
      }
    ]
  }
}
```

#### Status Codes
- **200**: Successful query execution
- **206**: Partial content (when synthesis fails but results available)
- **400**: Bad request
- **402**: API quota exceeded
- **500**: Server error
- **503**: Database error

#### Example Request
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "List all projects with Completed status"}'
```

#### Example Response
```json
{
  "answer": "There are 17 completed projects. Here are their details...",
  "error_type": null,
  "intermediate_steps": {
    "relevant_tables": ["projects"],
    "generated_sql": "SELECT * FROM projects WHERE status = 'Completed';",
    "query_results": [
      {
        "project_id": 4,
        "name": "Front-line mission-critical groupware",
        "start_date": "2025-02-22",
        "end_date": "2025-03-16",
        "budget": 258004.28,
        "status": "Completed"
      }
    ]
  }
}
```

## Error Handling

### 1. API Quota Error
```json
{
  "error": "Google API quota exceeded. Please check your API key and billing status.",
  "error_type": "api_quota",
  "original_error": "Error details...",
  "intermediate_steps": {
    "relevant_tables": null,
    "generated_sql": null,
    "query_results": null
  }
}
```

### 2. Database Error
```json
{
  "error": "Database query execution failed: ...",
  "error_type": "database",
  "original_error": "Error details...",
  "intermediate_steps": {
    "relevant_tables": ["table1", "table2"],
    "generated_sql": "SELECT ...",
    "query_results": null
  }
}
```

### 3. Partial Results
```json
{
  "answer": "Raw Query Results (AI synthesis unavailable): ...",
  "error_type": "api_quota_partial",
  "original_error": "Error details...",
  "intermediate_steps": {
    "relevant_tables": ["table1"],
    "generated_sql": "SELECT ...",
    "query_results": [...]
  }
}
```

## Query Examples

### 1. Simple Queries
```json
{"question": "How many employees are in the Sales department?"}
{"question": "List all completed projects"}
{"question": "Show me total sales for this year"}
```

### 2. Complex Queries
```json
{"question": "What is the average sale amount per customer in each country?"}
{"question": "Show me employees who have worked on more than 3 completed projects"}
{"question": "List top 5 customers by total purchase amount in the last quarter"}
```

## Rate Limiting
- Maximum of 60 requests per minute per IP
- Quota tracking for API usage
- Response headers include remaining quota information

## Best Practices

1. **Error Handling**
   - Always check error_type in responses
   - Handle partial results appropriately
   - Implement exponential backoff for retries

2. **Query Optimization**
   - Be specific in your questions
   - Include relevant time periods
   - Use appropriate filters

3. **Performance**
   - Cache frequently used queries
   - Implement request batching
   - Monitor response times

## Support
For API support or to report issues, please contact [Your Contact Information] 