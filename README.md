# 🔍 mf4_analyzer

A Python tool for performance analysis of EV battery data — focused on extracting key KPIs from `.mf4` log files.  
Transforms log data into plots, metrics, and PDF reports using predefined signal mappings and derived calculations.

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

1. Place one or more `.mf4` files in the `./mf4_logfiles` directory  
2. Run the script:

   ```bash
   python mf4_analyzer.py
   ```

3. Outputs will be generated in the `./mf4_exports` directory:
   - PDF report: `*_mf4_analysis_report.pdf`
   - Signal plots: `*.png` files grouped by signal category
   - Signal metadata: `*_signal_summary.json`

---

## 🧩 Signal Mapping & Derived Metrics

Signals are mapped using a structured keyword system defined in `KEYWORD_MAP`:

- Current: `PackCurrent`, `ChargeCurrentLimit`
- Power: `PackVoltage * PackCurrent`, `DischargePowerLimit`, `ChargePowerLimit`
- Cell Voltage: `CellVoltageMax`, `CellVoltageMin`, `CellVoltageMax - CellVoltageMin`
- Temperature: `CellTempMax`, `CellTempMin`, `CoolantInletTemp`
- Temperature Delta: `CellTempMax - CellTempMin`, `CellTempMax - CoolantInletTemp`
- SoC: `StateOfCharge`, `CellSocMin`, `CellSocMax`
- Delta SoC: `CellSocMax - CellSocMin`
- Fault Flags: `SystemFaultIndicator`

Derived metrics are calculated using aligned timestamps to ensure accurate comparisons and trend insights.

---

## 📁 Output Structure

All outputs are saved in the `./mf4_exports` directory:

- PDF report: Complete analysis with bullet metrics, tabulated values, and embedded plots  
- PNG plots: Individual signal group plots using dual axes where needed  
- JSON summary: Metadata for each signal (min, max, unit, delta)

---

## 🛠️ Roadmap

Future updates may include:

- Modular structure with CLI support  
- Export to CSV or other raw formats  
- Integration with dashboards or web interfaces  
- More flexible signal configuration or presets

---

## 📘 Version History

v2.0.0 – Adds derived metric support, PDF generation, JSON metadata export  
v1.1.0 – Introduced keyword mapping and filtering system  
v1.0.0 – Basic signal summary and plotting

---

## 🪪 License

MIT License – use freely, credit appreciated 🙌
