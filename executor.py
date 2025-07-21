import os
import glob
from resources import OUTPUT_REPORT
from relatorio_detalhado import generate_detailed_reports_by_crypto
from relatorio_por_timeframe import generate_timeframe_report_by_crypto

def run_reports():
    os.makedirs(OUTPUT_REPORT, exist_ok=True)
    for f in glob.glob(os.path.join(OUTPUT_REPORT, "*")):
        os.remove(f)
    print(f"\n🧹 Folder '{OUTPUT_REPORT}' cleaned.")

    print("\n📊 Generating detailed report per crypto...")
    generate_detailed_reports_by_crypto()

    print("\n📈 Generating timeframe report per crypto...")
    generate_timeframe_report_by_crypto()

    print("\n✅ All reports successfully generated!")

if __name__ == "__main__":
    run_reports()
