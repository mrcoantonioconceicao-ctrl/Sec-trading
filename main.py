"""
Orquestrador central do sistema de trading (Entrypoint).
"""

from bot import TradingBot

class TradingOrchestrator:
    """
    Gerencia a execução contínua do robô de trading seguindo princípios SOA.
    """

    def __init__(self):
        """
        Inicializa o orquestrador instanciando o bot de trading.
        """
        self.bot = TradingBot()

    def fetch_market_data(self):
        """
        Delega a busca de dados de mercado para o bot especializado.
        """
        return self.bot.buscar_dados_mercado()

    def run(self):
        """
        Executa o ciclo principal do orquestrador.
        """
        print("[ORQUESTRADOR] Iniciando ciclo de monitoramento do Sec-Trading...")
        self.bot.iniciar()

if __name__ == "__main__":
    orchestrator = TradingOrchestrator()
    orchestrator.run()
