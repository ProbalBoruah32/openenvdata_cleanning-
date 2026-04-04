import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application Settings"""
    
    # API Configuration
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    # Environment Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "7860"))
    
    # Data Configuration
    DATA_PATH: str = os.getenv("DATA_PATH", "./data")
    TASK_CONFIG_PATH: str = os.getenv("TASK_CONFIG_PATH", "./env/tasks.py")
    
    # Validation
    def validate(self):
        """Validate critical settings"""
        if not self.OPENAI_API_KEY and self.ENVIRONMENT == "production":
            raise ValueError("OPENAI_API_KEY is required in production")
        return True

settings = Settings()
