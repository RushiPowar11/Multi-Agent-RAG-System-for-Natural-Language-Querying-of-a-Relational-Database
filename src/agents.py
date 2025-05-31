from typing import List, Dict, Any, Optional
import google.generativeai as genai
from sqlalchemy import inspect, text
from config import settings
from database import get_db
from datetime import date
# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

def serialize_date(obj):
    """Convert date objects to ISO format strings."""
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


class SchemaAgent:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def get_schema_info(self) -> str:
        """Get database schema information."""
        db = next(get_db())
        inspector = inspect(db.bind)
        schema_info = []
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            col_info = [f"{col['name']} ({col['type'].__class__.__name__})" for col in columns]
            schema_info.append(f"Table: {table_name}\nColumns: {', '.join(col_info)}")
        
        return "\n\n".join(schema_info)
    
    def identify_relevant_tables(self, query: str) -> List[str]:
        """Identify relevant tables for the query."""
        schema_info = self.get_schema_info()
        prompt = f"""You are a database expert. Given a schema and a natural language query,
            identify the relevant tables needed to answer the query. Return only the table names in a comma-separated list.
            
            Schema:
            {schema_info}
            
            Query: {query}"""
        
        response = self.model.generate_content(prompt)
        return [table.strip() for table in response.text.split(",")]
        

class SQLGeneratorAgent:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def generate_sql(self, query: str, schema_info: str, relevant_tables: List[str]) -> str:
        """Generate SQL query from natural language."""
        prompt = f"""You are an SQL expert. Given a schema and a natural language query,
            generate a valid PostgreSQL query. The query should be efficient and use appropriate joins.
            Return only the SQL query, nothing else.
            
            Schema:
            {schema_info}
            
            Relevant tables: {', '.join(relevant_tables)}
            Query: {query}"""
        
        response = self.model.generate_content(prompt)
        # return response.text.strip()
        sql = response.text.strip()
        
        # Remove any markdown code block formatting if present
        sql = sql.replace('```sql', '').replace('```', '').strip()
        
        return sql

class RetrieverAgent:
    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        db = next(get_db())
        try:
            result = db.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()
            # return [dict(zip(columns, row)) for row in rows]
            return [{col: serialize_date(val) for col, val in zip(columns, row)} for row in rows]

        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

class SynthesizerAgent:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def synthesize_answer(self, query: str, sql_query: str, results: List[Dict[str, Any]]) -> str:
        """Generate natural language answer from query results."""
        prompt = f"""You are a helpful assistant that explains database query results in natural language.
            Provide a clear and concise answer based on the query results.
            
            Original question: {query}
            SQL Query used: {sql_query}
            Query results: {results}
            
            Please provide a natural language answer to the original question."""
        
        response = self.model.generate_content(prompt)
        return response.text.strip()

class MultiAgentSystem:
    def __init__(self) -> None:
        self.schema_agent = SchemaAgent()
        self.sql_generator = SQLGeneratorAgent()
        self.retriever = RetrieverAgent()
        self.synthesizer = SynthesizerAgent()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        try:
            # Step 1: Identify relevant tables
            try:
                relevant_tables = self.schema_agent.identify_relevant_tables(query)
                schema_info = self.schema_agent.get_schema_info()
            except Exception as e:
                if "quota" in str(e).lower() or "429" in str(e):
                    return {
                        "error": "Google API quota exceeded. Please check your API key and billing status.",
                        "error_type": "api_quota",
                        "original_error": str(e),
                        "intermediate_steps": {
                            "relevant_tables": None,
                            "generated_sql": None,
                            "query_results": None
                        }
                    }
                raise
            
            # Step 2: Generate SQL
            try:
                sql_query = self.sql_generator.generate_sql(query, schema_info, relevant_tables)
            except Exception as e:
                if "quota" in str(e).lower() or "429" in str(e):
                    return {
                        "error": "Google API quota exceeded while generating SQL.",
                        "error_type": "api_quota",
                        "original_error": str(e),
                        "intermediate_steps": {
                            "relevant_tables": relevant_tables,
                            "generated_sql": None,
                            "query_results": None
                        }
                    }
                raise
            
            # Step 3: Execute query
            try:
                results = self.retriever.execute_query(sql_query)
            except Exception as e:
                return {
                    "error": f"Database query execution failed: {str(e)}",
                    "error_type": "database",
                    "original_error": str(e),
                    "intermediate_steps": {
                        "relevant_tables": relevant_tables,
                        "generated_sql": sql_query,
                        "query_results": None
                    }
                }
            
            # Step 4: Synthesize answer
            try:
                answer = self.synthesizer.synthesize_answer(query, sql_query, results)
            except Exception as e:
                if "quota" in str(e).lower() or "429" in str(e):
                    # If synthesis fails but we have results, return them directly
                    return {
                        "answer": f"Raw Query Results (AI synthesis unavailable): {results}",
                        "error_type": "api_quota_partial",
                        "original_error": str(e),
                        "intermediate_steps": {
                            "relevant_tables": relevant_tables,
                            "generated_sql": sql_query,
                            "query_results": results
                        }
                    }
                raise
            
            return {
                "answer": answer,
                "error_type": None,
                "intermediate_steps": {
                    "relevant_tables": relevant_tables,
                    "generated_sql": sql_query,
                    "query_results": results
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "error_type": "unknown",
                "original_error": str(e),
                "intermediate_steps": {
                    "relevant_tables": relevant_tables if 'relevant_tables' in locals() else None,
                    "generated_sql": sql_query if 'sql_query' in locals() else None,
                    "query_results": None
                }
            }