import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib import colors
from tqdm import tqdm


def generate_trades_report(config: dict):
    input_folder = config["output_folder"]
    output_folder = config["output_report"]
    start_year = config["start_year"]
    end_year = config["end_year"]

    os.makedirs(output_folder, exist_ok=True)

    trade_files = [
        f for f in os.listdir(input_folder)
        if f.endswith("_trades.xlsx")
    ]

    if not trade_files:
        print("⚠️  No *_trades.xlsx files found. Skipping trades report.")
        return

    # 🔹 Barra de progresso padronizada para arquivos/crypto
    with tqdm(trade_files, desc="🧾 Trades Report", unit="crypto") as pbar:
        for file in pbar:
            symbol = file.replace("_trades.xlsx", "")
            path = os.path.join(input_folder, file)

            df = pd.read_excel(path)
            df.columns = [c.lower() for c in df.columns]

            required = {
                "entry_time", "exit_time", "timeframe",
                "year", "month", "pnl", "side", "return"
            }
            missing = required - set(df.columns)
            if missing:
                pbar.write(f"⚠️  Skipping {file}. Missing columns: {missing}")
                pbar.update(1)
                continue

            # 🔹 Normalizações
            df["entry_time"] = pd.to_datetime(df["entry_time"])
            df["exit_time"] = pd.to_datetime(df["exit_time"])
            df["duration"] = df["exit_time"] - df["entry_time"]
            df["direction"] = df["side"].map({
                1: "Long",
                -1: "Short",
                "long": "Long",
                "short": "Short"
            }).fillna(df["side"].astype(str))
            df['pnl_percent'] = df['return'] * 100

            pdf_path = os.path.join(output_folder, f"{symbol}_trades_detailed.pdf")
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph(f"<b>{symbol} — Trade Level Report</b>", styles["Title"]))
            elements.append(Spacer(1, 20))

            # 🔹 Organiza ano → mês → timeframe
            for year in range(start_year, end_year + 1):
                df_y = df[df["year"] == year]
                if df_y.empty:
                    continue

                elements.append(Paragraph(f"<b>Year: {year}</b>", styles["Heading1"]))
                elements.append(Spacer(1, 10))

                for month in sorted(df_y["month"].unique()):
                    df_m = df_y[df_y["month"] == month]

                    elements.append(Paragraph(f"<b>Month: {month:02d}</b>", styles["Heading2"]))
                    elements.append(Spacer(1, 8))

                    for timeframe in sorted(df_m["timeframe"].unique()):
                        df_tf = df_m[df_m["timeframe"] == timeframe]
                        if df_tf.empty:
                            continue

                        elements.append(Paragraph(f"<b>Timeframe: {timeframe}</b>", styles["Heading3"]))
                        elements.append(Spacer(1, 6))

                        table_data = [["Entry Time", "Exit Time", "Direction", "PnL (%)", "Duration"]]

                        for _, row in df_tf.iterrows():
                            table_data.append([
                                row["entry_time"].strftime("%Y-%m-%d %H:%M"),
                                row["exit_time"].strftime("%Y-%m-%d %H:%M"),
                                row["direction"],
                                f"{row['pnl_percent']:.2f} %",
                                str(row["duration"])
                            ])

                        table = Table(table_data, repeatRows=1)
                        table.setStyle(TableStyle([
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
                            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("ALIGN", (3, 1), (3, -1), "RIGHT"),
                        ]))

                        elements.append(table)
                        elements.append(Spacer(1, 12))

                    elements.append(PageBreak())

            # 🔹 Geração do PDF
            doc.build(elements)
