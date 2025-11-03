from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class StrategyType(str, Enum):
    GRID = "grid"
    MEAN_REVERSION = "mean_reversion"
    MOMENTUM = "momentum"

class AlertType(str, Enum):
    PRICE = "price"
    TECHNICAL = "technical"
    RISK = "risk"

class StrategyConfig(BaseModel):
    name: str = Field(..., description="Название стратегии")
    symbol: str = Field(..., description="Торговая пара")
    type: StrategyType = Field(..., description="Тип стратегии")
    volume: float = Field(..., gt=0, description="Объем торговли")
    leverage: int = Field(default=10, ge=1, le=100, description="Кредитное плечо")
    risk_per_trade: float = Field(default=0.02, ge=0.001, le=0.1, description="Риск на сделку")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Параметры стратегии")

class AlertConfig(BaseModel):
    symbol: str = Field(..., description="Торговая пара")
    condition: str = Field(..., description="Условие срабатывания")
    value: float = Field(..., description="Значение для условия")
    alert_type: AlertType = Field(default=AlertType.PRICE, description="Тип алерта")
    enabled: bool = Field(default=True, description="Включен ли алерт")

class BacktestRequest(BaseModel):
    strategy: str = Field(..., description="Название стратегии")
    symbol: str = Field(..., description="Торговая пара")
    period: str = Field(..., description="Период тестирования")
    initial_balance: float = Field(default=1000, gt=0, description="Начальный баланс")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Параметры стратегии")