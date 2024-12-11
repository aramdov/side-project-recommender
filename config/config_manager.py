# config/config_manager.py
from pydantic import BaseSettings, Field
from typing import Optional
from functools import lru_cache
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """
    This class is used to manage the application settings. 
    It uses Pydantic's BaseSettings class to define the settings schema and load the settings from environment variables or a .env file.

    Args:
        BaseSettings (_type_): _description_

    Returns:
        _type_: _description_
    """
    # API Keys
    pinecone_api_key: str = Field(..., env='PINECONE_API_KEY')
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    anthropic_api_key: str = Field(..., env='ANTHROPIC_API_KEY')
    
    # Pinecone Settings
    pinecone_environment: str = Field(..., env='PINECONE_ENVIRONMENT')
    pinecone_index_name: str = Field('project-recommender', env='PINECONE_INDEX_NAME')
    
    # OpenAI Settings
    openai_model: str = Field('gpt-4', env='OPENAI_MODEL')
    anthropic_api_key: str = Field(..., env='ANTHROPIC_API')
    embedding_model: str = Field('text-embedding-ada-002', env='EMBEDDING_MODEL')
    
    # Application Settings
    debug: bool = Field(False, env='DEBUG')
    environment: Environment = Field(Environment.DEVELOPMENT, env='ENVIRONMENT')
    max_upload_size: int = Field(5 * 1024 * 1024, env='MAX_UPLOAD_SIZE')  # 5MB default
    
    # Optional Features
    enable_caching: bool = Field(True, env='ENABLE_CACHING')
    cache_ttl: int = Field(3600, env='CACHE_TTL')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        use_enum_values = True

    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

@lru_cache()
def get_settings() -> Settings:
    """
    Create cached settings instance.
    Usage:
        settings = get_settings()
        pinecone_api_key = settings.pinecone_api_key
    """
    return Settings()

# Example usage in other files:
"""
from config.config_manager import get_settings

settings = get_settings()
if settings.is_development():
    print(f"Running in development mode")
"""