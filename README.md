<<<<<<< HEAD
# Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database
Multi-Agent RAG System for Natural Language Querying of a Relational Database
=======
# Multi-Agent RAG System with PostgreSQL Integration

A powerful Retrieval-Augmented Generation (RAG) system that uses multiple specialized agents to process natural language queries against a PostgreSQL database. The system combines the power of Google's Gemini AI with a robust database backend to provide intelligent, context-aware responses.

## Features

- **Natural Language Query Processing**: Convert plain English questions into SQL queries
- **Multi-Agent Architecture**:
  - Schema Agent: Analyzes database structure and identifies relevant tables
  - SQL Generator Agent: Converts natural language to SQL queries
  - Retriever Agent: Executes SQL queries and manages database interactions
  - Synthesizer Agent: Converts query results into natural language responses
- **Error Handling**: Comprehensive error handling for API quotas, database issues, and general errors
- **Interactive Web Interface**: Clean and responsive UI for query input and result display
- **Real-time Response**: Immediate feedback with detailed query execution steps

## System Requirements

- Python 3.8+
- PostgreSQL Database
- Google AI API Key (Gemini)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
GOOGLE_API_KEY=your_google_api_key
```

## Database Schema

The system works with the following tables:

- **customers**: Customer information and demographics
- **employees**: Employee records and details
- **projects**: Project tracking and status
- **project_assignments**: Employee project assignments
- **sales**: Sales transactions and records

## Usage

1. Start the server:
```bash
python src/main.py
```

2. Access the web interface at `http://localhost:8000`

3. Enter your query in natural language, for example:
   - "List all projects with 'Completed' status"
   - "Show me total sales by employee"
   - "Find customers who made purchases in the last month"

## API Endpoints

### GET /
- Returns the main web interface

### POST /ask
- Accepts natural language queries
- Returns JSON response with:
  - answer: Natural language response
  - error: Error message (if any)
  - error_type: Type of error (api_quota, database, unknown)
  - intermediate_steps: Query processing details

## Error Handling

The system handles various error types:
- API quota exceeded (402)
- Partial results available (206)
- Database errors (503)
- General errors (400)
- Server errors (500)

## Architecture

```
src/
├── main.py           # FastAPI application and routes
├── agents.py         # Multi-agent system implementation
├── config.py         # Configuration and settings
├── database.py       # Database connection and utilities
└── models.py         # SQLAlchemy models

templates/
└── index.html        # Web interface template
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Support

For support, please open an issue in the repository or contact [Your Contact Information]. 
>>>>>>> ccb15e4 (first commit)
