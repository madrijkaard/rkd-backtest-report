# 📊 rkd-backtest-report

Automated generation of **PDF graphical reports** from backtest results produced by the [`rkd-backtest-core`](https://github.com/madrijkaard/rkd-backtest-core) project.  
This project focuses on visually consolidating monthly returns of multiple cryptocurrencies across different timeframes using a YAML configuration.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-yellow?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=plotly)
![PDF](https://img.shields.io/badge/Report-PDF-red?logo=adobeacrobatreader)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🧠 Objective

This tool reads `.xlsx` files generated by `rkd-backtest-core` and:

- ✅ Generates **one PDF per cryptocurrency**
- ✅ Groups results by **timeframe** and **year**
- ✅ Displays clear **monthly return charts**
- ✅ Saves output in a clean `report/` folder
- ✅ Uses a **configurable YAML file**

---

## ⚙️ Technologies Used

| Technology     | Role                              |
|----------------|-----------------------------------|
| 🐍 Python       | Main programming language         |
| 📊 Pandas       | Tabular data manipulation         |
| 📈 Matplotlib   | Chart and PDF rendering           |
| 📗 Openpyxl     | Reading `.xlsx` Excel files       |
| 📄 PyYAML       | Loading YAML configuration        |
| ⚙️ Glob / OS    | File scanning and operations      |

---

## 📁 Project Structure

```
rkd-backtest-report/
├── config.yaml                 # Runtime configuration
├── executor.py                 # Main script for generating all reports
├── relatorio_detalhado.py     # Detailed table-style report per crypto
├── relatorio_por_timeframe.py # Timeframe-based charts per crypto
├── requirements.txt           # Project dependencies
├── venv.sh                    # Shell script to install and execute
├── report/                    # Output folder for PDFs
└── README.md                  # This file
```

---

## ⚙️ Configuration (`config.yaml`)

Customize your report generation through this file:

```yaml
output_folder: ../rkd-backtest-core/backtest
output_report: report
timeframes:
  - 15m
  - 30m
  - 1h
  - 4h
start_year: 2020
end_year: 2024
```

---

## 🚀 How to Run

### 1. Ensure `rkd-backtest-core` has generated `.xlsx` files

Expected location:

```bash
../rkd-backtest-core/backtest/
```

### 2. Run the environment setup script

Use the included shell script:

```bash
source venv.sh
```

> This script creates and activates a virtual environment, installs all dependencies, and runs the project.

---

## 📄 Output Reports

All PDFs will be generated inside the `report/` folder:

- `ETHUSDT_detailed.pdf`
- `ADAUSDT_timeframe.pdf`
- `AVAXUSDT_detailed.pdf`
- ...

Each file includes:

- One page per **year**
- Results grouped by **timeframe**
- Monthly **aggregated return** charts or tables

---

## 📸 Example Output

<p align="center">
  <img src="https://raw.githubusercontent.com/your-username/your-repo/main/assets/example_report.png" width="600" alt="Report Example">
</p>

---

## 🧪 Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:

```txt
pandas
matplotlib
openpyxl
pyyaml
tqdm
```

Install manually via:

```bash
pip install -r requirements.txt
```

---

## 📬 Contact

Questions or suggestions?  
Open an [issue](https://github.com/madrijkaard/rkd-backtest-report/issues) or submit a pull request!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Made with 💙 by [madrijkaard](https://github.com/madrijkaard)