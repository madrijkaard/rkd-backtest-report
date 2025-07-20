import os
import glob

from resources import OUTPUT_REPORT
from relatorio_detalhado import gerar_relatorios_detalhados_por_cripto
from relatorio_por_timeframe import gerar_relatorio_por_timeframe

def executar_relatorios():
    # Limpar a pasta de relatórios
    os.makedirs(OUTPUT_REPORT, exist_ok=True)
    for f in glob.glob(os.path.join(OUTPUT_REPORT, "*")):
        os.remove(f)
    
    print(f"\n🧹 Pasta '{OUTPUT_REPORT}' limpa com sucesso.")

    # Gerar os relatórios
    print("\n📊 Gerando relatório detalhado por cripto...")
    gerar_relatorios_detalhados_por_cripto()

    print("\n📊 Gerando relatório por timeframe...")
    gerar_relatorio_por_timeframe()

    print("\n✅ Todos os relatórios foram gerados com sucesso!")

if __name__ == "__main__":
    executar_relatorios()
