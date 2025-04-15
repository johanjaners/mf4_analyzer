# 🔍 mf4_analyzer

A lightweight, modular Python tool for analyzing `.mf4` log files.  
Optimized for EV battery test data and fast signal filtering, visualization, and metadata reporting.

---

## ✨ Features

📂 Auto-loads the latest `.mf4` file  
🔎 Keyword-based filtering using `DEFAULT_KEYWORDS`  
🧠 Signal mapping for battery, current, cell voltage, module temp, etc.  
📈 Clean plotting with accurate time axis  
ℹ️ Metadata summary: name, unit, sample count, min/max values  
📁 Export of tables/plots to `/output/` folder  
🚫 `.gitignore` support to exclude unwanted files

---

## 📦 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

1. Place one or more `.mf4` files in the project folder  
2. Optionally edit `DEFAULT_KEYWORDS` in `mf4_analyzer.py` to match your signal targets  
3. Run the analyzer:
```bash
python mf4_analyzer.py
```
4. View signal metadata in terminal  
5. Selected signals will be plotted in a separate window

---

## 💡 Planned Features

- Export filtered signals to `.csv`  
- Multi-signal plotting  
- CLI arguments (e.g., `--plot "SignalName"`, `--filter "Keyword"`)  
- Signal metadata export to file

---

## 🗂 Version History

**v1.1.0** – Keyword mapping, filtering system, cleanup, new structure  
**v1.0.0** – Initial release: signal summary, filtering, plotting

---

## 📘 License

MIT License – use freely, credit appreciated 🙌