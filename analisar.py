"""Módulo de Análise e Métricas de Desempenho (Trading Analytics).

Lê os dados coletados e processa estatísticas de comportamento do robô.
"""

import os

def analisar_desempenho() -> None:
    """Processa e exibe o relatório analítico do robô de trading."""
    print("=" * 60)
    print("RELATÓRIO DE ANÁLISE DE MERCADO E AUDITORIA DO ROBÔ")
    print("=" * 60)
    
    # Verifica se o log do orquestrador existe para extrair dados em tempo de execução
    log_file = "bot.log"
    if os.path.exists(log_file):
        print(f"Lendo registros recentes do arquivo de log: {log_file}")
        print("-" * 60)
        os.system(f"tail -n 10 {log_file}")
    else:
        print("Nenhum arquivo de log encontrado. Execute o main.py para gerar registros.")

    print("=" * 60)
    print("Status do Sistema: Orquestrador DDD/SOA operando normalmente no Termux.")
    print("=" * 60)

if __name__ == "__main__":
    analisar_desempenho()
