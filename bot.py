import time
import json
import urllib.request
import logging
import csv
import os
from datetime import datetime

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class BinanceAuditedBot:
    def __init__(self, symbol='BTCUSDT', capital=1000.0):
        self.symbol = symbol
        self.capital = capital
        self.risk_max = 0.02 # 2% de risco por operação
        self.url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval=1m&limit=50"
        self.arquivo_csv = "historico_sinais.csv"
        
        # Inicializa o arquivo CSV com os cabeçalhos se ele não existir
        if not os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['DataHora', 'Simbolo', 'Preco', 'EMA9', 'EMA21', 'ATR', 'Sinal', 'StopLoss', 'Alvo'])

    def salvar_auditoria(self, preco, ema9, ema21, atr, sinal, stop, alvo):
        """Salva o estado atual e o sinal gerado em um arquivo CSV local"""
        try:
            with open(self.arquivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    self.symbol,
                    f"{preco:.2f}",
                    f"{ema9:.2f}",
                    f"{ema21:.2f}",
                    f"{atr:.2f}",
                    sinal,
                    f"{stop:.2f}" if stop else "N/A",
                    f"{alvo:.2f}" if alvo else "N/A"
                ])
        except Exception as e:
            logging.error(f"Erro ao salvar no CSV: {e}")

    def buscar_dados_mercado(self):
        try:
            req = urllib.request.Request(
                self.url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                highs = [float(x[2]) for x in data]
                lows = [float(x[3]) for x in data]
                closes = [float(x[4]) for x in data]
                return highs, lows, closes
        except Exception as e:
            logging.error(f"Erro ao buscar dados da API da Binance: {e}")
            return None, None, None

    @staticmethod
    def calcular_ema(precos: list, periodo: int) -> float:
        if len(precos) < periodo:
            return precos[-1]
        multiplicador = 2 / (periodo + 1)
        ema = precos[0]
        for preco in precos[1:]:
            ema = (preco * multiplicador) + (ema * (1 - multiplicador))
        return ema

    @staticmethod
    def calcular_atr(highs: list, lows: list, closes: list, periodo: int = 14) -> float:
        if len(closes) < periodo + 1:
            return 1.0
        trs = []
        for i in range(1, len(closes)):
            h = highs[i]
            l = lows[i]
            c_prev = closes[i-1]
            tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
            trs.append(tr)
        return sum(trs[-periodo:]) / periodo

    def iniciar(self):
        logging.info(f"Iniciando robô auditado para {self.symbol} na Binance. Salvando em {self.arquivo_csv}...")
        
        try:
            while True:
                highs, lows, closes = self.buscar_dados_mercado()
                
                if closes and len(closes) > 25:
                    preco_atual = closes[-1]
                    
                    ema_curta = self.calcular_ema(closes, periodo=9)
                    ema_longa = self.calcular_ema(closes, periodo=21)
                    atr = self.calcular_atr(highs, lows, closes, periodo=14)

                    sinal = "AGUARDANDO"
                    stop_loss = 0.0
                    alvo = 0.0

                    if ema_curta > ema_longa:
                        sinal = "COMPRA"
                        stop_loss = preco_atual - (2.0 * atr)
                        alvo = preco_atual + (4.0 * atr)
                        logging.info(f">> SINAL DE COMPRA | Preço: {preco_atual:.2f} | Stop: {stop_loss:.2f} | Alvo: {alvo:.2f}")
                    else:
                        logging.info(f">> TENDÊNCIA DE BAIXA / AGUARDANDO | Preço: {preco_atual:.2f}")

                    # Salva os dados na auditoria CSV
                    self.salvar_auditoria(preco_atual, ema_curta, ema_longa, atr, sinal, stop_loss, alvo)

                time.sleep(10)
                
        except KeyboardInterrupt:
            logging.info("Robô interrompido manualmente pelo usuário. Dados salvos com sucesso.")

if __name__ == "__main__":
    bot = BinanceAuditedBot(symbol='BTCUSDT', capital=1000.0)
    bot.iniciar()
