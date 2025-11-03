from contextlib import asynccontextmanager
import logging
import sys
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import os
import json
import asyncio
from typing import Dict, Any, List
from datetime import datetime

from config.settings import settings, get_all_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/trading_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

bybit_client = None
trading_engine = None
technical_analysis = None
risk_manager = None
portfolio_manager = None
alert_system = None
backtester = None
data_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bybit_client, trading_engine, technical_analysis, risk_manager
    global portfolio_manager, alert_system, backtester, data_manager
    
    logger.info("ByBit Trading Bot Pro запускается...")
    
    try:
        from api.bybit_client import ByBitClient
        from api.trading_engine import TradingEngine
        from api.technical_analysis import TechnicalAnalysis
        from api.risk_manager import RiskManager
        from api.portfolio_manager import PortfolioManager
        from api.alert_system import AlertSystem
        from api.backtester import Backtester
        from api.data_manager import DataManager
        
        bybit_client = ByBitClient(
            api_key=settings.BYBIT_API_KEY,
            api_secret=settings.BYBIT_API_SECRET,
            testnet=settings.TESTNET
        )
        
        trading_engine = TradingEngine(bybit_client)
        technical_analysis = TechnicalAnalysis()
        risk_manager = RiskManager(trading_engine)
        portfolio_manager = PortfolioManager(trading_engine, risk_manager)
        alert_system = AlertSystem()
        backtester = Backtester()
        data_manager = DataManager()
        
        if bybit_client.test_connection():
            logger.info("Подключение к ByBit API установлено")
        else:
            logger.warning("Не удалось подключиться к ByBit API - проверьте настройки")
            
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
    
    yield
    
    logger.info("ByBit Trading Bot Pro останавливается...")
    try:
        if trading_engine:
            trading_engine.stop_all_strategies()
            logger.info("Все торговые стратегии остановлены")
    except Exception as e:
        logger.error(f"Ошибка при остановке приложения: {e}")

app = FastAPI(
    title="ByBit Trading Bot Pro",
    description="Профессиональная платформа для алгоритмической торговли на ByBit",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for directory in ["static", "templates", "data/backups", "data/exports", "data/logs"]:
    os.makedirs(directory, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "settings": get_all_settings()
    })

@app.get("/api/health")
async def health_check():
    try:
        bybit_connected = False
        if bybit_client:
            bybit_connected = bybit_client.test_connection()
        
        components_status = {
            "bybit_api": bybit_connected,
            "trading_engine": trading_engine is not None,
            "technical_analysis": technical_analysis is not None,
            "risk_manager": risk_manager is not None,
            "alert_system": alert_system is not None
        }
        
        return {
            "status": "running",
            "bybit_connected": bybit_connected,
            "components": components_status,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "error",
            "bybit_connected": False,
            "error": str(e)
        }

@app.get("/api/account")
async def get_account_info():
    try:
        if not bybit_client:
            raise HTTPException(status_code=503, detail="ByBit client not initialized")
        
        balance = bybit_client.get_wallet_balance()
        positions = bybit_client.get_positions()
        
        return {
            "balance": balance,
            "positions": positions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Ошибка получения информации об аккаунте: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strategies/start")
async def start_strategy(strategy_config: Dict[str, Any]):
    try:
        if not trading_engine:
            raise HTTPException(status_code=503, detail="Trading engine not initialized")
        
        result = trading_engine.start_strategy(strategy_config)
        return {"status": "success", "strategy_id": result}
    except Exception as e:
        logger.error(f"Ошибка запуска стратегии: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strategies/stop/{strategy_id}")
async def stop_strategy(strategy_id: str):
    try:
        if not trading_engine:
            raise HTTPException(status_code=503, detail="Trading engine not initialized")
        
        trading_engine.stop_strategy(strategy_id)
        return {"status": "success", "message": f"Strategy {strategy_id} stopped"}
    except Exception as e:
        logger.error(f"Ошибка остановки стратегии: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/strategies")
async def get_strategies():
    try:
        if not trading_engine:
            return {"strategies": []}
        
        strategies = trading_engine.get_active_strategies()
        return {"strategies": strategies}
    except Exception as e:
        logger.error(f"Ошибка получения списка стратегий: {e}")
        return {"strategies": []}

@app.get("/api/market/{symbol}")
async def get_market_data(symbol: str):
    try:
        if not bybit_client:
            raise HTTPException(status_code=503, detail="ByBit client not initialized")
        
        market_data = bybit_client.get_market_data(symbol)
        return market_data
    except Exception as e:
        logger.error(f"Ошибка получения рыночных данных: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/{symbol}")
async def get_technical_analysis(symbol: str):
    try:
        if not technical_analysis:
            raise HTTPException(status_code=503, detail="Technical analysis not available")
        
        analysis = technical_analysis.analyze_symbol(symbol)
        return analysis
    except Exception as e:
        logger.error(f"Ошибка технического анализа: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/risk/assessment")
async def get_risk_assessment():
    try:
        if not risk_manager:
            raise HTTPException(status_code=503, detail="Risk manager not available")
        
        assessment = risk_manager.assess_portfolio_risk()
        return assessment
    except Exception as e:
        logger.error(f"Ошибка оценки рисков: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    return get_all_settings()

@app.post("/api/settings")
async def update_settings(settings_data: Dict[str, Any]):
    try:
        from config.settings import update_settings
        update_settings(settings_data)
        return {"status": "success", "message": "Settings updated"}
    except Exception as e:
        logger.error(f"Ошибка обновления настроек: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )