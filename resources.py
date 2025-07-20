import os

# Pasta onde estão os arquivos XLSX de resultados gerados pelo core
OUTPUT_FOLDER = os.path.join("..", "rkd-backtest-core", "backtest")

# Pasta onde os PDFs consolidados serão salvos
OUTPUT_REPORT = "report"

# Timeframes disponíveis (deve coincidir com o core)
TIMEFRAMES = ['15m', '30m', '1h', '4h']

# Intervalo de anos para os relatórios
START_YEAR = 2020
END_YEAR = 2024
