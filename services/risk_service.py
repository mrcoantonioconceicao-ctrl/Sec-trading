"""Módulo de Gestão de Risco (SOA).

Responsável pelo isolamento estrito das regras de alocação de capital e limites de exposição.
"""

class RiskManagementService:
    """Serviço isolado para cálculo de tamanho de posição e mitigação de risco."""
    
    def __init__(self, capital_total: float, risco_maximo_porcentagem: float = 0.02) -> None:
        """Inicializa o serviço de risco com capital base e teto de risco por trade."""
        self.capital_total = capital_total
        self.risco_maximo_porcentagem = risco_maximo_porcentagem

    def calcular_tamanho_posicao(self, preco_entrada: float, stop_loss: float) -> float:
        """Calcula o volume da posição respeitando estritamente o limite de perda aceitável."""
        risco_unitario = abs(preco_entrada - stop_loss)
        if risco_unitario == 0:
            return 0.0
        capital_em_risco = self.capital_total * self.risco_maximo_porcentagem
        return capital_em_risco / risco_unitario
