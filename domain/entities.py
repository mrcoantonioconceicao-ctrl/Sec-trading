"""Módulo de Entidades de Domínio (DDD).

Define as estruturas imutáveis e objetos de valor utilizados pelo ecossistema de trading.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Signal:
    """Define os tipos de sinais gerados pelo motor de estratégia."""
    COMPRA = "COMPRA"
    VENDA = "VENDA"
    NEUTRO = "NEUTRO"

@dataclass
class TradeOrder:
    """Representa a estrutura de uma ordem executada ou simulada."""
    symbol: str
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    signal_type: str
