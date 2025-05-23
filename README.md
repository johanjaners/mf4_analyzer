# 🔍 mf4_analyzer

A Python tool for performance analysis of EV battery test data — focused on extracting key KPIs from `.mf4` log files.  
Transforms raw log data into plots, metrics, and PDF reports using predefined signal mappings and derived calculations.

---

## ✨ Features

- 📂 **Auto-loads** the latest `.mf4` file from the specified directory  
- 🔑 **Keyword-based signal mapping** using `KEYWORD_MAP` for structured analysis  
- 🧠 **Derived metric calculations** (e.g., delta voltages, temperature differentials, SoC ranges)  
- 📈 **Time-aligned plotting** of signals with optional dual-axis views  
- 📄 **PDF report generation** with summary metrics and embedded plots  
- 🗃️ **JSON export** of signal metadata for inspection or reuse  
- 🧪 **Discharge mode detection** (based on SoC trend) for context-sensitive output  

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
🚀 How to Use
Place one or more .mf4 files in the ./mf4_logfiles directory

Run the script:

bash
Kopiera
Redigera
python mf4_analyzer.py
Outputs will be generated in the ./mf4_exports directory:

📄 PDF report: *_mf4_analysis_report.pdf

🖼️ Signal plots: *.png files grouped by signal category

🗃️ Signal metadata: *_signal_summary.json

📊 Signal Mapping & Derived Metrics
Signals are mapped using a structured keyword system defined in KEYWORD_MAP:

Current: PackCurrent, ChargeCurrentLimit

Power: PackVoltage * PackCurrent, DischargePowerLimit, ChargePowerLimit

Cell Voltage: CellVoltageMax, CellVoltageMin, CellVoltageMax - CellVoltageMin

Temperature: CellTempMax, CellTempMin, CoolantInletTemp

Temperature Delta: CellTempMax - CellTempMin, CellTempMax - CoolantInletTemp

SoC: StateOfCharge, CellSocMin, CellSocMax

Delta SoC: CellSocMax - CellSocMin

Fault Flags: SystemFaultIndicator

Derived metrics are calculated using aligned timestamps to ensure accurate comparisons and trend insights.

📁 Output Structure
All outputs are saved in the ./mf4_exports directory:

PDF Reports: Complete analysis summary with bullet metrics, tabulated values, and embedded signal plots

PNG Plots: Individual signal group plots using dual axes where appropriate

JSON Summary: Cleaned metadata for each signal including min, max, unit, and delta values

🛠 Roadmap
Future updates may include:

Modular structure with CLI support

Export to CSV or other raw formats

Integration with dashboards or web interfaces

More flexible signal configuration or presets

🗂 Version History
v2.0.0 – Adds derived metric support, PDF generation, JSON metadata export
v1.1.0 – Introduced keyword mapping and filtering system
v1.0.0 – Basic signal summary and plotting

📘 License
MIT License – use freely, credit appreciated 🙌