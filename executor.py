import os
import glob
from resources import OUTPUT_REPORT
from relatorio_detalhado import gerar_relatorios_detalhados_por_cripto
from relatorio_por_timeframe import gerar_relatorio_por_timeframe

def executar_relatorios():
    os.makedirs(OUTPUT_REPORT, exist_ok=True)
    for f in glob.glob(os.path.join(OUTPUT_REPORT, "*")):
        os.remove(f)
    print(f"\n🧹 Folder '{OUTPUT_REPORT}' cleaned.")

    print("\n📊 Generating detailed report per crypto...")
    gerar_relatorios_detalhados_por_cripto()

    print("\n📈 Generating timeframe report per crypto...")
    gerar_relatorio_por_timeframe()

    print("\n✅ All reports successfully generated!")

if __name__ == "__main__":
    executar_relatorios()
