import os
import glob
import yaml
from relatorio_detalhado import generate_detailed_reports_by_crypto
from relatorio_por_timeframe import generate_timeframe_report_by_crypto

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_reports():
    config = load_config()
    output_report = config["output_report"]

    os.makedirs(output_report, exist_ok=True)
    for f in glob.glob(os.path.join(output_report, "*")):
        os.remove(f)
    print(f"\n🧹 Folder '{output_report}' cleaned.")

    print("\n📊 Generating detailed report per crypto...")
    generate_detailed_reports_by_crypto(config)

    print("\n📈 Generating timeframe report per crypto...")
    generate_timeframe_report_by_crypto(config)

    print("\n✅ All reports successfully generated!")

if __name__ == "__main__":
    run_reports()
