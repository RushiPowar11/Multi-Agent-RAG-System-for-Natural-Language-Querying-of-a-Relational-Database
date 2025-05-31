# Technical Documentation: Multi-Agent RAG System

## System Architecture

### 1. Agent Components

#### SchemaAgent
- **Purpose**: Database schema analysis and table identification
- **Key Methods**:
  - `get_schema_info()`: Retrieves database schema using SQLAlchemy inspection
  - `identify_relevant_tables()`: Uses Gemini AI to identify tables needed for a query
- **Input**: Natural language query
- **Output**: List of relevant table names

#### SQLGeneratorAgent
- **Purpose**: SQL query generation from natural language
- **Key Methods**:
  - `generate_sql()`: Converts natural language to SQL using Gemini AI
- **Input**: Query, schema info, and relevant tables
- **Output**: Valid PostgreSQL query string

#### RetrieverAgent
- **Purpose**: Database interaction and query execution
- **Key Methods**:
  - `execute_query()`: Executes SQL and handles result serialization
- **Input**: SQL query string
- **Output**: List of dictionaries containing query results

#### SynthesizerAgent
- **Purpose**: Natural language response generation
- **Key Methods**:
  - `synthesize_answer()`: Converts query results to natural language
- **Input**: Original query, SQL query, and results
- **Output**: Natural language response

### 2. Database Models

#### Customer Model
```python
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    country = Column(String(100))
    join_date = Column(Date)
```

#### Employee Model
```python
class Employee(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    department = Column(String(50))
    hire_date = Column(Date)
    salary = Column(Float)
```

#### Project Model
```python
class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float)
    status = Column(String(20))
```

### 3. Error Handling

#### Error Types
1. **API Quota Errors** (402)
   - Triggered when Gemini AI API limit is reached
   - Handled in schema identification and answer synthesis

2. **Partial Results** (206)
   - When query execution succeeds but synthesis fails
   - Returns raw results with warning

3. **Database Errors** (503)
   - Connection issues
   - Query execution failures
   - Schema inspection errors

4. **General Errors** (400)
   - Invalid input
   - Malformed queries
   - Unsupported operations

### 4. API Endpoints

#### GET /
- **Purpose**: Serve web interface
- **Response**: HTML template
- **Template**: index.html

#### POST /ask
- **Purpose**: Process natural language queries
- **Request Body**:
  ```json
  {
    "question": "string"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "string",
    "error": "string",
    "error_type": "string",
    "intermediate_steps": {
      "relevant_tables": ["string"],
      "generated_sql": "string",
      "query_results": []
    }
  }
  ```

### 5. Configuration

#### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_API_KEY`: Gemini AI API key
- `MODEL_NAME`: Gemini model identifier

#### Database Configuration
- Connection pooling enabled
- Echo mode for SQL logging
- Session management with context processors

### 6. Development Guidelines

#### Adding New Features
1. Create new agent class in agents.py
2. Implement required methods
3. Update MultiAgentSystem class
4. Add error handling
5. Update documentation

#### Testing
1. Unit tests for each agent
2. Integration tests for full pipeline
3. Error handling tests
4. Performance benchmarks

#### Code Style
- Follow PEP 8
- Type hints required
- Docstrings for all classes and methods
- Error messages must be descriptive

### 7. Performance Considerations

#### Query Optimization
- Use appropriate indexes
- Limit result sets
- Optimize joins
- Cache frequent queries

#### API Usage
- Implement rate limiting
- Cache API responses
- Handle timeouts
- Batch requests when possible

### 8. Security

#### Database Security
- Use connection pooling
- Parameterized queries
- Limited permissions
- Input validation

#### API Security
- Rate limiting
- Input sanitization
- Error message sanitization
- Secure key storage

### 9. Monitoring

#### Metrics to Track
- Query response times
- API quota usage
- Error rates
- Database performance

#### Logging
- Request/response logging
- Error logging
- Performance metrics
- API usage stats

### 10. Maintenance

#### Regular Tasks
- Update dependencies
- Monitor API quotas
- Database optimization
- Log rotation
- Performance tuning

#### Troubleshooting
1. Check API quota status
2. Verify database connection
3. Review error logs
4. Monitor system resources
5. Test query performance 