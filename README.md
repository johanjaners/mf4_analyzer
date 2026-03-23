# 🔍 mf4\_analyzer

A Python-based pipeline for performance analysis of EV system logs and data-driven engineering workflows.
Processes `.mf4` files to compute key performance indicators (KPIs), generate structured reports (PDF) and CSV exports.
Now supports a modular CLI and extended KPIs.

> Note: Example report is generated from anonymized and modified data for demonstration purposes.

---

## ✨ Features (v2.2.0)

* Loads latest `.mf4` log file from `./mf4_logfiles/`
* Modular CLI structure
* Configurable signal mapping and derived metrics
* Derived metric calculations:

  * Power KPIs (RMS, Avg)
  * Charge KPIs (time, Avg, SoC-based metrics)
  * Discharge KPIs (time, SoC-based metrics)
  * Voltage & Temperature deltas
* Outputs:

  * **PDF report** with plots + summary
  * **CSV file** with KPIs

---

## 🚀 Quickstart

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Place one or more `.mf4` files in the `./mf4_logfiles/` folder.

3. Run the analyzer:

   ```bash
   python mf4_analyzer.py
   ```

4. Outputs will be created in `./mf4_exports/`:

   * PDF report (`*_mf4_analysis_report.pdf`)
   * CSV KPIs (`*_metrics.csv`)
   * Signal plots (`*.png` grouped by category)

---

## 📁 Repository Structure

```plaintext
mf4_analyzer.py
requirements.txt
.gitignore
README.md
mf4_analyzer_modular/
 ├── compute_metrics.py
 ├── mdf_loader.py
 ├── metrics_list.py
 ├── pdf_exporter.py
 ├── plotter_exporter.py
 ├── signal_config.py         # excluded in public release
 ├── signal_extractor.py
 └── summary_generator.py
mf4_logfiles/                 # place your .mf4/.dat log file here
mf4_exports/                  # auto-created for reports/plots
```

---

## 🛠️ Roadmap

* v3.0 → SQL pipeline
* v3.1 → Batch processing with config flags
* v3.2 → Dashboard interface (Power BI/Tableau)
* v3.3 → API

---

## 📘 Version History

* **v2.2.0** – Modular CLI, CSV export, Power/Charge/Discharge KPIs
* **v2.0.2** – Demo mode, handling improvements, README update
* **v2.0.1** – Demo mode, roadmap, structural upgrades
* **v2.0.0** – PDF/JSON outputs, derived metrics
* **v1.1.0** – Signal keyword system
* **v1.0.0** – Initial version (basic plot + report)

---

## 📜 License

MIT License – free to use, modify, and distribute. Credit appreciated 🙌
