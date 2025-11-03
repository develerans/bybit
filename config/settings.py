import os
from pydantic_settings import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY", "")
    BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET", "")
    TESTNET: bool = os.getenv("TESTNET", "True").lower() == "true"
    
    DEFAULT_LEVERAGE: int = int(os.getenv("DEFAULT_LEVERAGE", "10"))
    RISK_PER_TRADE: float = float(os.getenv("RISK_PER_TRADE", "0.02"))
    MAX_OPEN_POSITIONS: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    DAILY_LOSS_LIMIT: float = float(os.getenv("DAILY_LOSS_LIMIT", "100.0"))
    GLOBAL_STOP_LOSS: float = float(os.getenv("GLOBAL_STOP_LOSS", "5.0"))
    
    ENABLE_GRID_STRATEGY: bool = os.getenv("ENABLE_GRID_STRATEGY", "True").lower() == "true"
    ENABLE_MEAN_REVERSION: bool = os.getenv("ENABLE_MEAN_REVERSION", "True").lower() == "true"
    ENABLE_MOMENTUM: bool = os.getenv("ENABLE_MOMENTUM", "False").lower() == "true"
    GRID_LEVELS: int = int(os.getenv("GRID_LEVELS", "5"))
    GRID_SPACING: float = float(os.getenv("GRID_SPACING", "0.01"))
    
    ENABLE_TRAILING_STOP: bool = os.getenv("ENABLE_TRAILING_STOP", "False").lower() == "true"
    TRAILING_STOP_DISTANCE: float = float(os.getenv("TRAILING_STOP_DISTANCE", "1.0"))
    TAKE_PROFIT_RATIO: float = float(os.getenv("TAKE_PROFIT_RATIO", "2.0"))
    
    ENABLE_TELEGRAM_NOTIFICATIONS: bool = os.getenv("ENABLE_TELEGRAM_NOTIFICATIONS", "False").lower() == "true"
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    AUTO_RESTART: bool = os.getenv("AUTO_RESTART", "True").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()

def get_all_settings() -> Dict[str, Any]:
    return {
        "bybit_api": {
            "BYBIT_API_KEY": settings.BYBIT_API_KEY[:10] + "..." if settings.BYBIT_API_KEY else "",
            "BYBIT_API_SECRET": "***",
            "TESTNET": settings.TESTNET
        },
        "trading": {
            "DEFAULT_LEVERAGE": settings.DEFAULT_LEVERAGE,
            "RISK_PER_TRADE": settings.RISK_PER_TRADE,
            "MAX_OPEN_POSITIONS": settings.MAX_OPEN_POSITIONS,
            "DAILY_LOSS_LIMIT": settings.DAILY_LOSS_LIMIT,
            "GLOBAL_STOP_LOSS": settings.GLOBAL_STOP_LOSS
        },
        "strategies": {
            "ENABLE_GRID_STRATEGY": settings.ENABLE_GRID_STRATEGY,
            "ENABLE_MEAN_REVERSION": settings.ENABLE_MEAN_REVERSION,
            "ENABLE_MOMENTUM": settings.ENABLE_MOMENTUM,
            "GRID_LEVELS": settings.GRID_LEVELS,
            "GRID_SPACING": settings.GRID_SPACING
        },
        "risk_management": {
            "ENABLE_TRAILING_STOP": settings.ENABLE_TRAILING_STOP,
            "TRAILING_STOP_DISTANCE": settings.TRAILING_STOP_DISTANCE,
            "TAKE_PROFIT_RATIO": settings.TAKE_PROFIT_RATIO
        },
        "notifications": {
            "ENABLE_TELEGRAM_NOTIFICATIONS": settings.ENABLE_TELEGRAM_NOTIFICATIONS,
            "TELEGRAM_BOT_TOKEN": settings.TELEGRAM_BOT_TOKEN,
            "TELEGRAM_CHAT_ID": settings.TELEGRAM_CHAT_ID
        },
        "application": {
            "DEBUG": settings.DEBUG,
            "LOG_LEVEL": settings.LOG_LEVEL,
            "AUTO_RESTART": settings.AUTO_RESTART
        }
    }

def update_settings(new_settings: Dict[str, Any]) -> None:
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Settings updated: {new_settings}")