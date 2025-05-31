from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import Optional

# Load environment variables from .env file
load_dotenv()

def get_env_variable(var_name: str) -> str:
    """Get an environment variable or raise an exception if it's not found."""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set. Please set it in your .env file.")
    return value

class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    # Database settings
    DATABASE_URL: str = Field(default_factory=lambda: get_env_variable("DATABASE_URL"))
    
    # Google AI settings
    GOOGLE_API_KEY: str = Field(default_factory=lambda: get_env_variable("GOOGLE_API_KEY"))
    MODEL_NAME: str = "gemini-2.0-flash"  # Using Gemini 2.0 Flash
    
    class Config:
        env_file = ".env"

# Initialize settings
try:
    settings = Settings()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please ensure all required environment variables are set in your .env file.")
    raise 