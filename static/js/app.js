// Управление вкладками
function openTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// API функции
async function checkHealth() {
    try {
        addLog('Запрос статуса системы...');
        const response = await fetch('/api/health');
        const data = await response.json();
        
        document.getElementById('appStatus').textContent = data.status === 'running' ? 'Работает' : 'Ошибка';
        document.getElementById('appStatus').className = 'status-value ' + 
            (data.status === 'running' ? 'connected' : 'disconnected');
        
        document.getElementById('bybitStatus').textContent = 
            data.bybit_connected ? 'Подключено' : 'Отключено';
        document.getElementById('bybitStatus').className = 'status-value ' + 
            (data.bybit_connected ? 'connected' : 'disconnected');
            
        addLog('Статус системы получен');
        
    } catch (error) {
        addLog('Ошибка при проверке статуса: ' + error.message);
    }
}

async function getStrategies() {
    try {
        addLog('Запрос списка стратегий...');
        const response = await fetch('/api/strategies');
        const data = await response.json();
        
        document.getElementById('strategiesCount').textContent = data.strategies.length;
        addLog('Список стратегий получен: ' + data.strategies.length + ' активных');
        
    } catch (error) {
        addLog('Ошибка при получении стратегий: ' + error.message);
    }
}

async function getAccountInfo() {
    try {
        addLog('Запрос информации об аккаунте...');
        const response = await fetch('/api/account');
        const data = await response.json();
        addLog('Информация об аккаунте получена');
    } catch (error) {
        addLog('Ошибка получения информации об аккаунте: ' + error.message);
    }
}

async function getTechnicalAnalysis() {
    try {
        addLog('Запрос технического анализа...');
        const response = await fetch('/api/analysis/BTCUSDT');
        const data = await response.json();
        
        const resultsDiv = document.getElementById('analysisResults');
        resultsDiv.innerHTML = `
            <h3>Анализ ${data.symbol}</h3>
            <p>RSI: ${data.rsi}</p>
            <p>Тренд: ${data.trend}</p>
            <p>Уровни поддержки: ${data.support_levels.join(', ')}</p>
        `;
        
        addLog('Технический анализ получен');
    } catch (error) {
        addLog('Ошибка получения технического анализа: ' + error.message);
    }
}

async function loadSettings() {
    try {
        addLog('Загрузка настроек...');
        const response = await fetch('/api/settings');
        const data = await response.json();
        
        const settingsDiv = document.getElementById('settingsContent');
        settingsDiv.innerHTML = `
            <h3>Текущие настройки</h3>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
        
        addLog('Настройки загружены');
    } catch (error) {
        addLog('Ошибка загрузки настроек: ' + error.message);
    }
}

// Обработка формы стратегии
document.getElementById('strategyForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const strategyConfig = {
        name: document.getElementById('strategyName').value,
        symbol: document.getElementById('strategySymbol').value,
        type: document.getElementById('strategyType').value,
        volume: parseFloat(document.getElementById('strategyVolume').value)
    };
    
    try {
        addLog('Запуск стратегии: ' + strategyConfig.name);
        const response = await fetch('/api/strategies/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(strategyConfig)
        });
        
        const result = await response.json();
        if (result.status === 'success') {
            addLog('Стратегия успешно запущена с ID: ' + result.strategy_id);
            this.reset();
            getStrategies();
        } else {
            addLog('Ошибка запуска стратегии');
        }
    } catch (error) {
        addLog('Ошибка запуска стратегии: ' + error.message);
    }
});

function addLog(message) {
    const logContainer = document.getElementById('logContainer');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = '[' + new Date().toLocaleTimeString() + '] ' + message;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Автоматическая проверка при загрузке
document.addEventListener('DOMContentLoaded', function() {
    checkHealth();
    getStrategies();
    addLog('Панель управления загружена');
});

// Периодическое обновление статуса
setInterval(checkHealth, 30000);