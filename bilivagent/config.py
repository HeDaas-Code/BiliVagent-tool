"""Configuration management"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # SiliconFlow API
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
    SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    
    # Models
    LLM_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-32B-Instruct")
    VLM_MODEL = os.getenv("VLM_MODEL", "OpenGVLab/InternVL2-26B")

    # Vosk
    VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "./model/vosk-model-cn-0.22")

    # Directories
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    TEMP_DIR = os.getenv("TEMP_DIR", "./temp")
    
    # Debug mode - show detailed info like transcription
    DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    @classmethod
    def debug_print(cls, *args, **kwargs):
        """Print only when DEBUG mode is enabled"""
        if cls.DEBUG:
            print(*args, **kwargs)

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.SILICONFLOW_API_KEY:
            raise ValueError("SILICONFLOW_API_KEY is required")
        
        # Create directories if they don't exist
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
