import os
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from tqdm import tqdm


def generate_trades_report(config: dict):
    input_folder = config["output_folder"]
    output_folder = config["output_report"]

    os.makedirs(output_folder, exist_ok=True)

    trade_files = [
        f for f in os.listdir(input_folder)
        if f.endswith("_trades.xlsx")
    ]

    if not trade_files:
        print("⚠️  No *_trades.xlsx files found. Skipping trades report.")
        return

    with tqdm(trade_files, desc="🧾 Trades Report", unit="crypto") as pbar:
        for file in pbar:
            symbol = file.replace("_trades.xlsx", "")
            path = os.path.join(input_folder, file)

            df = pd.read_excel(path)
            df.columns = [c.lower() for c in df.columns]

            required = {
                "entry_time", "exit_time", "timeframe",
                "year", "month", "side", "return"
            }
            missing = required - set(df.columns)
            if missing:
                pbar.write(f"⚠️  Skipping {file}. Missing columns: {missing}")
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

            df["pnl_percent"] = df["return"] * 100

            # 🔹 Ordenação
            df.sort_values(
                by=["year", "month", "timeframe", "entry_time"],
                inplace=True
            )

            pdf_path = os.path.join(
                output_folder,
                f"{symbol}_trades_flat_table.pdf"
            )

            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=landscape(A4),
                rightMargin=20,
                leftMargin=20,
                topMargin=20,
                bottomMargin=20
            )

            styles = getSampleStyleSheet()
            elements = []

            # 🔹 Título
            elements.append(
                Paragraph(
                    f"<b>{symbol} — Trades Report (Flat Table)</b>",
                    styles["Title"]
                )
            )
            elements.append(Spacer(1, 16))

            # 🔹 Cabeçalho
            table_data = [[
                "Year",
                "Month",
                "Timeframe",
                "Entry Time",
                "Exit Time",
                "Direction",
                "PnL (%)",
                "Duration"
            ]]

            # 🔹 Linhas + controle de mês
            row_months = []

            for _, row in df.iterrows():
                table_data.append([
                    int(row["year"]),
                    f"{int(row['month']):02d}",
                    row["timeframe"],
                    row["entry_time"].strftime("%Y-%m-%d %H:%M"),
                    row["exit_time"].strftime("%Y-%m-%d %H:%M"),
                    row["direction"],
                    f"{row['pnl_percent']:.2f}",
                    str(row["duration"])
                ])
                row_months.append(int(row["month"]))

            table = Table(
                table_data,
                repeatRows=1,
                colWidths=[
                    50,   # Year
                    45,   # Month
                    70,   # Timeframe
                    110,  # Entry
                    110,  # Exit
                    70,   # Direction
                    65,   # PnL
                    90    # Duration
                ]
            )

            # 🔹 Estilos base
            style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ("ALIGN", (6, 1), (6, -1), "RIGHT"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
            ])

            # 🔹 Zebra por mudança de mês (sequencial)
            light_gray = colors.Color(0.85, 0.85, 0.85)

            last_month = None
            paint = False  # começa sem pintar

            for i, month in enumerate(row_months, start=1):  # start=1 por causa do header
                if month != last_month:
                    paint = not paint
                    last_month = month

                if paint:
                    style.add(
                        "BACKGROUND",
                        (0, i),
                        (-1, i),
                        light_gray
                    )

            table.setStyle(style)
            elements.append(table)

            doc.build(elements)
