"""
Módulo principal do robô de trading contendo a lógica de mercado e indicadores.
"""

import urllib.request
import json
import math

class TradingBot:
    """
    Classe responsável por gerenciar a conexão com a Binance e calcular indicadores técnicos.
    """

    def __init__(self, symbol="BTCUSDT"):
        """
        Inicializa o robô de trading com o par de ativos desejado.
        """
        self.symbol = symbol
        self.url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval=1m&limit=50"

    def buscar_dados_mercado(self):
        """
        Busca dados de klines (velas) da API pública da Binance via HTTP puro.
        """
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                prices = [float(candle[4]) for candle in data] # Preço de fechamento
                return prices
        except Exception as e:
            print(f"[ERRO] Falha ao buscar dados da Binance: {e}")
            return []

    def calcular_ema(self, prices, periodo):
        """
        Calcula a Média Móvel Exponencial (EMA) para uma lista de preços.
        """
        if len(prices) < periodo:
            return None
        k = 2 / (periodo + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price * k) + (ema * (1 - k))
        return ema

    def calcular_atr(self, prices, periodo=14):
        """
        Calcula o Average True Range (ATR) básico para mensurar volatilidade.
        """
        if len(prices) < periodo + 1:
            return 0.0
        soma_ranges = 0.0
        for i in range(1, len(prices)):
            tr = abs(prices[i] - prices[i-1])
            soma_ranges += tr
        return soma_ranges / periodo

    def iniciar(self):
        """
        Executa um ciclo de análise de mercado utilizando os indicadores técnicos.
        """
        prices = self.buscar_dados_mercado()
        if not prices:
            print("[AVISO] Nenhum dado de preço retornado.")
            return

        ema9 = self.calcular_ema(prices, 9)
        ema21 = self.calcular_ema(prices, 21)
        atr = self.calcular_atr(prices)

        print(f"[ANÁLISE] Preço Atual: {prices[-1]} | EMA 9: {ema9:.2f} | EMA 21: {ema21:.2f} | ATR: {atr:.2f}")
