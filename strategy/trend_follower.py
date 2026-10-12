"""Módulo de Estratégia de Seguimento de Tendência.

Implementa os cálculos matemáticos puros de EMA e ATR para filtragem de mercado.
"""

from typing import List, Tuple

class TrendFollowerStrategy:
    """Implementa a lógica pura de tendência (Clean Code / Single Responsibility)."""
    
    def __init__(self, short_period: int = 9, long_period: int = 21, atr_period: int = 14) -> None:
        """Configura os períodos para as médias móveis e o indicador de volatilidade ATR."""
        self.short_period = short_period
        self.long_period = long_period
        self.atr_period = atr_period

    def calcular_ema(self, precos: List[float], periodo: int) -> float:
        """Calcula a Média Móvel Exponencial (EMA) para uma lista de preços."""
        if len(precos) < periodo:
            return precos[-1]
        multiplicador = 2 / (periodo + 1)
        ema = precos[0]
        for preco in precos[1:]:
            ema = (preco * multiplicador) + (ema * (1 - multiplicador))
        return ema

    def calcular_atr(self, highs: List[float], lows: List[float], closes: List[float]) -> float:
        """Calcula o Average True Range (ATR) para mensurar a volatilidade do mercado."""
        if len(closes) < self.atr_period + 1:
            return 1.0
        trs = []
        for i in range(1, len(closes)):
            h = highs[i]
            l = lows[i]
            c_prev = closes[i-1]
            tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
            trs.append(tr)
        return sum(trs[-self.atr_period:]) / self.atr_period

    def analyze(self, highs: List[float], lows: List[float], closes: List[float]) -> Tuple[str, float, float, float]:
        """Analisa os dados de mercado e retorna o sinal operacional e os níveis de preço."""
        ema_curta = self.calcular_ema(closes, self.short_period)
        ema_longa = self.calcular_ema(closes, self.long_period)
        atr = self.calcular_atr(highs, lows, closes)
        preco_atual = closes[-1]

        if ema_curta > ema_longa:
            stop_loss = preco_atual - (2.0 * atr)
            take_profit = preco_atual + (4.0 * atr)
            return "COMPRA", preco_atual, stop_loss, take_profit
        
        return "NEUTRO", preco_atual, 0.0, 0.0
