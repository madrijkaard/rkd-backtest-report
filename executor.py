import os
import glob
import yaml

from relatorio_detalhado import generate_detailed_reports_by_crypto
from relatorio_por_timeframe import generate_timeframe_report_by_crypto
from relatorio_trades import generate_trades_report


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def run_reports():
    config = load_config()
    output_report = config["output_report"]

    # 🔹 Garante pasta de saída
    os.makedirs(output_report, exist_ok=True)

    # 🔹 Limpa relatórios antigos
    for f in glob.glob(os.path.join(output_report, "*")):
        os.remove(f)
    print(f"\n🧹 Folder '{output_report}' cleaned.")

    # 🔹 Relatório detalhado (_strategy.xlsx)
    print("\n📊 Generating detailed report per crypto...")
    generate_detailed_reports_by_crypto(config)

    # 🔹 Relatório por timeframe (_strategy.xlsx)
    print("\n📈 Generating timeframe report per crypto...")
    generate_timeframe_report_by_crypto(config)

    # 🔹 Relatório de trades (_trades.xlsx)  ← NOVO
    print("\n🧾 Generating trades report per crypto...")
    generate_trades_report(config)

    print("\n✅ All reports successfully generated!")


if __name__ == "__main__":
    run_reports()
