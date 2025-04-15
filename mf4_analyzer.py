# mf4_analyzer.py

"""
🔍 MF4 Analyzer – Version 1.1.0

A lightweight, modular Python tool for analyzing `.mf4` log files.  
Optimized for EV battery test data and fast signal filtering, visualization, and metadata reporting.

Features:
- Auto-loads latest `.mf4` file
- Filters signals by keyword
- Displays min/max/unit/sample count in tables
- Plots grouped signals over time

Usage:
    - Place .mf4 logs in `mf4_logfiles/`
    - Adjust `KEYWORD_MAP` if needed
    - Run the script to analyze & visualize

Author: J2Workx
GitHub: https://github.com/J2Workx
"""


import os
from asammdf import MDF
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

# === GLOBAL SETTINGS ===
INPUT_DIR = "./mf4_logfiles"  # Directory containing .mf4 files

# === SIGNAL MAPPING ===
# Signal keyword-to-name mapping
KEYWORD_MAP = {
    "battery": "batt",
    "pack current": "current",
    "cell voltage": "voltage",
    "module tab temp": "temperature"
}

DEFAULT_KEYWORDS = list(KEYWORD_MAP.keys())

# === Function: Load latest MF4 file ===
def load_latest_mf4(directory=INPUT_DIR):
    mf4_files = sorted(
        [f for f in os.listdir(directory) if f.lower().endswith(".mf4")],
        key=lambda f: os.path.getmtime(os.path.join(directory, f)),
        reverse=True
    )
    for file in mf4_files:
        try:
            path = os.path.join(directory, file)
            mdf = MDF(path, memory='minimum')  # Leaner loading
            print(f"✅ Loaded file: {file}")
            return mdf
        except Exception as e:
            print(f"⚠️ Failed to load {file}: {e}")
    raise FileNotFoundError("❌ No .mf4 files could be loaded.")

# === Function: General File Analysis ===
def analyze_file(mdf):
    for ch_name in mdf.channels_db:
        try:
            sig = mdf.get(ch_name)
            timestamps = sig.timestamps
            if len(timestamps) > 1:
                duration = timestamps[-1] - timestamps[0]
                avg_step = np.mean(np.diff(timestamps))
                return {
                    "total_signals": len(mdf.channels_db),
                    "duration": duration,
                    "avg_step": avg_step
                }
        except:
            continue
    return {"total_signals": len(mdf.channels_db), "duration": None, "avg_step": None}

# === Function: Filter Signals by Keywords ===
def filter_signals_by_keywords(mdf, keywords=DEFAULT_KEYWORDS):
    results = []
    for keyword in keywords:
        mapped_keyword = KEYWORD_MAP.get(keyword, keyword)
        filtered = [name for name in mdf.channels_db if mapped_keyword.lower() in name.lower()]
        for name in filtered:
            try:
                sig = mdf.get(name)
                samples = sig.samples
                results.append({
                    "keyword": keyword,
                    "name": name,
                    "unit": sig.unit,
                    "samples": len(samples),
                    "signal": sig,
                    "min": float(np.min(samples)),
                    "max": float(np.max(samples))
                })
            except:
                continue
    return results

# === Function: Display Signal Tables by Keyword ===
def display_signal_tables_by_keyword(data):
    from collections import defaultdict

    grouped = defaultdict(list)
    for item in data:
        grouped[item["keyword"].lower()].append(item)

    windows = []
    for keyword, signals in grouped.items():
        root = tk.Tk()
        root.title(f"Signals: {keyword}")

        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("Name", "Unit", "Samples", "Min", "Max"), show="headings")
        for col in ("Name", "Unit", "Samples", "Min", "Max"):
            tree.heading(col, text=col)
            tree.column(col, anchor="w")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        for item in signals:
            tree.insert("", "end", values=(item["name"], item["unit"], item["samples"], item.get("min"), item.get("max")))

        windows.append(root)

    for win in windows:
        win.mainloop()

# === Function: Multi-Plot ===
def plot_core_signals(mdf):
    plt.switch_backend('tkagg')
    signals_to_plot = {}

    for key, keyword in KEYWORD_MAP.items():
        filtered_names = [name for name in mdf.channels_db if keyword.lower() in name.lower()]
        if filtered_names:
            signals_to_plot[key] = filtered_names

    num_plots = len(signals_to_plot)
    fig, axs = plt.subplots(num_plots, 1, figsize=(12, 3 * num_plots), sharex=True)
    if num_plots == 1:
        axs = [axs]

    for idx, (key, signal_list) in enumerate(signals_to_plot.items()):
        for name in signal_list:
            try:
                sig = mdf.get(name)
                
                axs[idx].plot(sig.timestamps, sig.samples, label=name)
                axs[idx].set_ylabel(f"{sig.unit}" if sig.unit else "Value")
            except:
                continue
        axs[idx].set_title(key.replace("_", " ").title())
        axs[idx].grid(True)

    axs[-1].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

# === MAIN ===
def main():
    mdf = load_latest_mf4()
    file_info = analyze_file(mdf)
    print("\n📊 General File Info:")
    print(f"Total signals: {file_info['total_signals']}")
    if file_info['duration']:
        print(f"🕒 Duration: {file_info['duration']:.2f}s, ⏱ Avg step: {file_info['avg_step']:.6f}s")

    keyword_data = filter_signals_by_keywords(mdf)
    display_signal_tables_by_keyword(keyword_data)

    # Core Multi-Plot
    plot_core_signals(mdf)

if __name__ == "__main__":
    main()
