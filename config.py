"""Configuration management for the test automation project"""
import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration class"""
    
    # Base URLs
    BASE_URL: str = os.getenv("BASE_URL", "https://admin-test.granitestack.ai")
    LOGIN_URL: str = f"{BASE_URL}/admin/login"
    
    # Page URLs
    PAGES: Dict[str, str] = {
        "login": f"{BASE_URL}/admin/login",
        "dashboard": f"{BASE_URL}/admin/dashboard/503/Demmo",
        "organisation_listing": f"{BASE_URL}/admin/business-board",
        "platform_listing": f"{BASE_URL}/admin/platforms",
    }
    
    # Credentials
    USERNAME: Optional[str] = os.getenv("USERNAME")
    PASSWORD: Optional[str] = os.getenv("PASSWORD")
    
    # Browser settings
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1280"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "720"))
    
    # Timeouts (in milliseconds)
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    
    # Retry settings
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "1000"))
    
    # AI settings
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # Test settings
    PARALLEL_WORKERS: int = int(os.getenv("PARALLEL_WORKERS", "4"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        required_vars = ["USERNAME", "PASSWORD", "BASE_URL"]
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
