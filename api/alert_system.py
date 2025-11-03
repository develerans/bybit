import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self):
        self.alerts = []
        logger.info("Система уведомлений инициализирована")
    
    def create_alert(self, alert_config: Dict[str, Any]) -> str:
        try:
            alert_id = f"alert_{len(self.alerts) + 1}"
            alert_config["id"] = alert_id
            alert_config["created_at"] = "2024-01-01T00:00:00"  # В реальности datetime.now()
            self.alerts.append(alert_config)
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Ошибка создания алерта: {e}")
            raise
    
    def get_alerts(self, active_only: bool = True) -> List[Dict[str, Any]]:
        return self.alerts