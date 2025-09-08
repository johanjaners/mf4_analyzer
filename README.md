# 🔍 mf4_analyzer

A Python-based pipeline for performance analysis of EV system logs and data-driven engineering workflows.
Processes `.mf4` files to compute key performance indicators (KPIs), generate structured reports and metadata exports.
Planned extensions include CSV export and SQL pipeline for structured storage and database integration.

---

## ✨ Features

- Loads latest `.mf4` log file from specified directory  
- Keyword-based signal mapping using `KEYWORD_MAP`  
- Derived metric calculations (e.g. delta voltages, temp differentials, SoC delta)  
- Time-aligned plotting with optional dual-axis views  
- PDF report with summary metrics and embedded plots  
- JSON metadata export (min, max, unit, delta)  
- Discharge mode detection (based on SoC trend)

---

## 📆 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

1. Place one or more `.mf4` files in the `./mf4_logfiles/` directory
2. Run the script:

   ```bash
   python mf4_analyzer.py
   ```
   To run the included demo:

   ```bash
   python mf4_analyzer.py --demo
   ```

4. Outputs will be generated in the `./mf4_exports` directory:
   - PDF report: `*_mf4_analysis_report.pdf`
   - Signal plots: `*.png` files grouped by signal category
   - Signal metadata: `*_signal_summary.json`

---

## 🩹 Signal Mapping & Derived Metrics

Signals are mapped using a structured keyword system defined in `KEYWORD_MAP`:

- Current: `PackCurrent`, `ChargeCurrentLimit`
- Power: `PackVoltage * PackCurrent`, `DischargePowerLimit`, `ChargePowerLimit`
- Cell Voltage: `CellVoltageMax`, `CellVoltageMin`, `CellVoltageMax - CellVoltageMin`
- Temperature: `CellTempMax`, `CellTempMin`
- Temperature Delta: `CellTempMax - CellTempMin`
- SoC: `StateOfCharge`, `CellSocMin`, `CellSocMax`
- Delta SoC: `CellSocMax - CellSocMin`
- Fault Flags: `SystemFaultIndicator`

Derived metrics are calculated using aligned timestamps to ensure accurate comparisons and trend insights.

---

## 📁 File Structure

```plaintext
.
├── mf4_analyzer.py
├── requirements.txt
├── /mf4_logfiles/                # Input directory for .mf4 files
├── /mf4_exports/                 # Output directory for reports and plots
├── /demo/
│   ├── mf4_demo.mf4              # Example sanitized log file
│   └── mf4_demo_mf4_analysis_report.pdf   # Example output report
```

---

## 🌟 Demo File

A demo log file is included for quick validation of functionality. The file has been sanitized to remove any sensitive or proprietary data.

```bash
python mf4_analyzer.py --demo
```

- Input: `./demo/mf4_demo.mf4`  
- Output: `./demo/mf4_demo_mf4_analysis_report.pdf`

---

## 🛠️ Roadmap

- v2.1 → Modular CLI structure
- v2.2 → CSV export
- v2.3 → SQL pipeline integration
- v3.0 → Batch processing with config flags
- v3.1 → Dashboard interface or integration (Power BI, Tableau)
- v3.2 → KPI profiles for specific test cases

---

## 📘 Version History

- v2.0.1 – Added demo file, directory structure, roadmap alignment  
- v2.0.0 – Added PDF/JSON output, derived metrics  
- v1.1.0 – Signal keyword system  
- v1.0.0 – Initial version with basic plot and report

---

## 📜 License

MIT License – use freely, credit appreciated 🙌