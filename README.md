# 🔍 mf4_analyzer

A lightweight Python script for analyzing `.mf4` measurement files. Designed for fast signal inspection, filtering, and visualization — ideal for electric vehicle battery logs or similar data-heavy formats.

---

## ✨ Features

- 📂 Auto-loads the latest `.mf4` file in the folder  
- 🔎 Filters signals by keyword (e.g., `"HvBatt"`)  
- ℹ️ Displays:
  - Signal name  
  - Unit  
  - Sample count  
  - **Min/Max values**  
- 📈 Plots selected signal with proper timestamp alignment

---

## 📦 Requirements

Install dependencies with pip:

```bash
pip install asammdf matplotlib numpy
```

---

## 🚀 How to Use

1. Place `.mf4` file(s) in the same folder as the script.
2. Edit the top of `mf4_analyzer.py` to match your target signal:
   ```python
   filter_keyword = "HvBatt"
   plot_signal = "HvBattIDc"
   ```
3. Run the script:
   ```bash
   python mf4_analyzer.py
   ```
4. Check terminal for signal summary.
5. The selected signal will open in a separate plot window.

---

## 💡 Planned Features

- Export filtered signals to `.csv`  
- Multi-plot support  
- CLI argument parsing (`--filter`, `--plot`)  
- Signal metadata export

---

## 🗂 Version History

- `v1.0.0` – First working release: signal summary, filter, and plot

---

## 📘 License

MIT License – use freely, credit appreciated 🙌
