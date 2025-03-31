# 📁 MF4 to CSV Converter (Signal-Filtered)

This Python script extracts selected signals from `.mf4` log files and converts them to `.csv`, using the `asammdf` library. 
It is optimized for smaller exports by **filtering only the desired signals**, improving performance and avoiding memory issues.

---

## ✅ Features
- Convert `.mf4` → `.csv` for **selected signals only**
- Lightweight & memory-safe compared to full export
- Logging & progress bar included
- Placeholder signal names (can be customized)

---

## 🔧 Example Use Case
You're analyzing electric vehicle data and want to extract specific measurements like `Voltage`, `Current`, and `Temperature` to:
- Calculate **internal resistance**
- Compare signal patterns across test logs
- Use output `.csv` in ML pipelines or external tools

---

## 🚀 How to Use

1. **Install required packages**:
   ```bash
   pip install asammdf pandas tqdm
   ```

2. **Place `.mf4` files** in the same folder as the script *(or set a different input folder)*.

3. **Edit `signals_to_export`** in the script:
   ```python
   signals_to_export = ["Voltage1", "CurrentSensor", "PackTemp"]
   ```
   > Keep placeholder names (`Signal1`, etc.) if pushing to public repos.

4. **Run the script**:
   ```bash
   python convert_mf4_to_csv.py
   ```

5. **Check `mf4_to_csv/` folder** for the exported `.csv` files.

---

## 🧠 Notes
- You can modify the signal list to match your own measurement channels.
- Files with no matching signals will be **skipped safely**.
- The `.csv` output is kept minimal by exporting only specifed signals.

---

## 🧭 About This Project
This project lays a foundation for future tools such as:

- A **CSV Analyzer** for signal trends
- Integrated **battery resistance calculators**
- or even **ML-ready feature extractors**

---
