import logging
from pybit.unified_trading import HTTP
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ByBitClient:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        try:
            self.rest_client = HTTP(
                testnet=testnet,
                api_key=api_key,
                api_secret=api_secret,
            )
            logger.info("ByBit клиент инициализирован")
        except Exception as e:
            logger.error(f"Ошибка инициализации ByBit клиента: {e}")
            self.rest_client = None
    
    def test_connection(self) -> bool:
        try:
            if not self.rest_client:
                return False
                
            result = self.rest_client.get_wallet_balance(accountType="UNIFIED")
            logger.info("Успешное подключение к ByBit REST API")
            return True
        except Exception as e:
            error_msg = str(e).replace('→', '->')
            logger.error(f"Ошибка подключения к ByBit API: {error_msg}")
            
            if "401" in str(e):
                logger.error("Ошибка 401: Проверьте API ключи и секреты")
            elif "403" in str(e):
                logger.error("Ошибка 403: Проверьте разрешения API ключей")
                
            return False
    
    def get_wallet_balance(self) -> Dict[str, Any]:
        try:
            if not self.rest_client:
                raise Exception("REST клиент не инициализирован")
                
            response = self.rest_client.get_wallet_balance(accountType="UNIFIED")
            return response
        except Exception as e:
            error_msg = str(e).replace('→', '->')
            logger.error(f"Ошибка получения баланса: {error_msg}")
            raise
    
    def get_positions(self) -> Dict[str, Any]:
        try:
            if not self.rest_client:
                raise Exception("REST клиент не инициализирован")
                
            response = self.rest_client.get_positions(
                category="linear",
                settleCoin="USDT"
            )
            return response
        except Exception as e:
            error_msg = str(e).replace('→', '->')
            logger.error(f"Ошибка получения позиций: {error_msg}")
            raise
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        try:
            if not self.rest_client:
                raise Exception("REST клиент не инициализирован")
                
            ticker = self.rest_client.get_tickers(
                category="linear",
                symbol=symbol
            )
            
            orderbook = self.rest_client.get_orderbook(
                category="linear",
                symbol=symbol
            )
            
            return {
                "ticker": ticker,
                "orderbook": orderbook,
                "symbol": symbol
            }
        except Exception as e:
            error_msg = str(e).replace('→', '->')
            logger.error(f"Ошибка получения рыночных данных: {error_msg}")
            raise