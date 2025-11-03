import logging
from typing import Dict, Any, List
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self, bybit_client):
        self.bybit_client = bybit_client
        self.active_strategies: Dict[str, Dict[str, Any]] = {}
        logger.info("Торговый движок инициализирован")
    
    def start_strategy(self, strategy_config: Dict[str, Any]) -> str:
        try:
            strategy_id = str(uuid.uuid4())[:8]
            
            if not self._validate_strategy_config(strategy_config):
                raise ValueError("Неверная конфигурация стратегии")
            
            strategy = {
                "id": strategy_id,
                "config": strategy_config,
                "status": "running",
                "started_at": datetime.now().isoformat(),
                "performance": {
                    "trades_count": 0,
                    "total_pnl": 0.0,
                    "win_rate": 0.0
                }
            }
            
            self.active_strategies[strategy_id] = strategy
            
            logger.info(f"Стратегия {strategy_id} запущена: {strategy_config.get('name', 'Unnamed')}")
            
            return strategy_id
            
        except Exception as e:
            logger.error(f"Ошибка запуска стратегии: {e}")
            raise
    
    def stop_strategy(self, strategy_id: str) -> bool:
        try:
            if strategy_id in self.active_strategies:
                self.active_strategies[strategy_id]["status"] = "stopped"
                self.active_strategies[strategy_id]["stopped_at"] = datetime.now().isoformat()
                logger.info(f"Стратегия {strategy_id} остановлена")
                return True
            else:
                logger.warning(f"Стратегия {strategy_id} не найдена")
                return False
        except Exception as e:
            logger.error(f"Ошибка остановки стратегии: {e}")
            return False
    
    def stop_all_strategies(self) -> None:
        try:
            for strategy_id in list(self.active_strategies.keys()):
                self.stop_strategy(strategy_id)
            logger.info("Все стратегии остановлены")
        except Exception as e:
            logger.error(f"Ошибка при остановке всех стратегий: {e}")
    
    def get_active_strategies(self) -> List[Dict[str, Any]]:
        return [
            strategy for strategy in self.active_strategies.values()
            if strategy["status"] == "running"
        ]
    
    def get_all_strategies(self) -> List[Dict[str, Any]]:
        return list(self.active_strategies.values())
    
    def _validate_strategy_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ["symbol", "type", "volume"]
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Отсутствует обязательное поле: {field}")
                return False
        
        if config["volume"] <= 0:
            logger.error("Объем торгов должен быть положительным")
            return False
        
        return True