import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from openpyxl import load_workbook
from tqdm import tqdm
from resources import OUTPUT_FOLDER, OUTPUT_REPORT, TIMEFRAMES, START_YEAR, END_YEAR

MONTHS_EN = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

def generate_detailed_reports_by_crypto():
    os.makedirs(OUTPUT_REPORT, exist_ok=True)
    files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.xlsx"))

    for file in tqdm(files, desc="📊 Detailed Report", unit="crypto"):
        crypto = os.path.basename(file).replace(".xlsx", "")
        pdf_path = os.path.join(OUTPUT_REPORT, f"{crypto}_detailed.pdf")

        with PdfPages(pdf_path) as pdf:
            for year in range(START_YEAR, END_YEAR + 1):
                for tf in TIMEFRAMES:
                    wb = load_workbook(file)
                    if tf not in wb.sheetnames:
                        continue

                    df = pd.read_excel(file, sheet_name=tf)
                    df["Date"] = pd.to_datetime(df["Date"])
                    df["Year"] = df["Date"].dt.year
                    df["Month"] = df["Date"].dt.month.map(MONTHS_EN)
                    df_year = df[df["Year"] == year]

                    if df_year.empty:
                        continue

                    selected_columns = [
                        "Month", "Total Return [%]", "Benchmark Return [%]",
                        "Total Trades", "Total Closed Trades",
                        "Total Open Trades", "Open Trade PnL"
                    ]
                    table = df_year[selected_columns].copy()
                    table["Month"] = pd.Categorical(table["Month"],
                        categories=list(MONTHS_EN.values()), ordered=True)
                    table.sort_values(by="Month", inplace=True)
                    table["Total Return [%]"] = table["Total Return [%]"].map(lambda x: f"{x:.2f}%")
                    table["Benchmark Return [%]"] = table["Benchmark Return [%]"].map(lambda x: f"{x:.2f}%")
                    table["Open Trade PnL"] = table["Open Trade PnL"].map(lambda x: f"{x:.2f}")
                    table["Total Trades"] = table["Total Trades"].astype(int)
                    table["Total Closed Trades"] = table["Total Closed Trades"].astype(int)
                    table["Total Open Trades"] = table["Total Open Trades"].astype(int)

                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.axis("off")
                    ax.axis("tight")
                    table_data = [table.columns.tolist()] + table.values.tolist()
                    table_plot = ax.table(cellText=table_data, colLabels=None, loc='center', cellLoc='center')
                    table_plot.scale(1.1, 1.3)
                    plt.title(f"{crypto} - {tf} - {year}", fontsize=14)
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()
