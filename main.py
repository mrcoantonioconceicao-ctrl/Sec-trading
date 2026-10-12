import time
import json
import urllib.request
import logging
from strategy.trend_follower import TrendFollowerStrategy
from services.risk_service import RiskManagementService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class TradingOrchestrator:
    def __init__(self, symbol='BTCUSDT'):
        self.symbol = symbol
        self.url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval=1m&limit=50"
        self.strategy = TrendFollowerStrategy()
        self.risk_service = RiskManagementService(capital_total=1000.0)

    def fetch_market_data(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                highs = [float(x[2]) for x in data]
                lows = [float(x[3]) for x in data]
                closes = [float(x[4]) for x in data]
                return highs, lows, closes
        except Exception as e:
            logging.error(f"Erro na comunicação SOA com a Binance: {e}")
            return None, None, None

    def run(self):
        logging.info(f"Orquestrador de Trading iniciado para {self.symbol} (Arquitetura DDD/SOA)...")
        try:
            while True:
                highs, lows, closes = self.fetch_market_data()
                if closes and len(closes) > 25:
                    sinal, preco, stop, alvo = self.strategy.analyze(highs, lows, closes)
                    
                    if sinal == "COMPRA":
                        tamanho = self.risk_service.calcular_tamanho_posicao(preco, stop)
                        logging.info(f">> [SINAL COMPRA] Preço: {preco:.2f} | Stop: {stop:.2f} | Alvo: {alvo:.2f} | Posição: {tamanho:.4f}")
                    else:
                        logging.info(f">> [AGUARDANDO] Preço Atual: {preco:.2f} | Tendência Neutra/Baixa")

                time.sleep(10)
        except KeyboardInterrupt:
            logging.info("Sistema encerrado com segurança.")

if __name__ == "__main__":
    orchestrator = TradingOrchestrator()
    orchestrator.run()
