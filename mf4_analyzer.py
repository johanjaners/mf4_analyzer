"""
mf4_analyzer.py
 
Tool for extracting performance KPIs from EV battery test data in .mf4 log files.

Features:
- Signal extraction and derived metric computation
- PDF report generation with plots and summary
- JSON export of signal metadata

Input:  latest .mf4 file in ./mf4_logfiles
Output: PDF, PNG, and JSON files in ./mf4_exports

Version: 2.0.0
Author: Johan Janérs
"""

# === Imports ===
# Standard libraries for file handling, math, plotting, and PDF export
import os
import numpy as np
import matplotlib.pyplot as plt
import json
from asammdf import MDF
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# === Paths ===
# Directory paths for input and output
INPUT_DIR = "./mf4_logfiles"
EXPORT_DIR = "./mf4_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === Signal groups mapped to signal names (including derived signals) ===
# Structure used to extract and categorize signals and derived metrics
KEYWORD_MAP = {
    "Current": ["PackCurrent", "ChargeCurrentLimit"],
    "Power": [
        "PackVoltage * PackCurrent",
        "DischargePowerLimit",
        "ChargePowerLimit"
    ],
    "Cell Voltage": [
        "CellVoltageMax",
        "CellVoltageMin",
        "CellVoltageMax - CellVoltageMin"
    ],
    "Temperature": [
        "CellTempMax",
        "CellTempMin",
        "CoolantInletTemp"
    ],
    "Temperature Delta": [
        "CellTempMax - CellTempMin",
        "CellTempMax - CoolantInletTemp"
    ],
    "SoC": [
        "StateOfCharge", 
        "CellSocMin", 
        "CellSocMax"
    ],
    "Delta SoC": [
        "CellSocMax - CellSocMin"
    ],
    "Fault Flags": ["SystemFaultIndicator"]
}

# === Load the latest .mf4 file from directory ===
def load_latest_mf4(directory=INPUT_DIR):
    files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".mf4")],
        key=lambda x: os.path.getmtime(os.path.join(directory, x)),
        reverse=True
    )
    for file in files:
        try:
            return MDF(os.path.join(directory, file)), file
        except:
            continue
    raise FileNotFoundError("No valid MF4 file found.")

# === Extract signals and compute derived metrics ===
def extract_signals(mdf):
    data = []  # List of all processed signals
    group_map = {}  # Dictionary mapping each group to its signal entries
    soc_samples = []
    actual_power_samples = []
    current_samples = []

    for group, names in KEYWORD_MAP.items():
        group_map[group] = []
        for name in names:
            try:
                # Derived: Delta Cell Voltage
                if name == "CellVoltageMax - CellVoltageMin":
                    a = mdf.get("CellVoltageMax").samples
                    b = mdf.get("CellVoltageMin").samples
                    ts = mdf.get("CellVoltageMax").timestamps
                    samples = a - b

                # Derived: Delta Tmax - Tmin
                elif name == "CellTempMax - CellTempMin":
                    a = mdf.get("CellTempMax").samples
                    b = mdf.get("CellTempMin").samples
                    ts = mdf.get("CellTempMax").timestamps
                    samples = a - b

                # Derived: Delta Tmax - Coolant with time alignment
                elif name == "CellTempMax - CoolantInletTemp":
                    a_sig = mdf.get("CellTempMax")
                    b_sig = mdf.get("CoolantInletTemp")
                    common_time = a_sig.timestamps if len(a_sig.timestamps) <= len(b_sig.timestamps) else b_sig.timestamps
                    a_resampled = a_sig.interp(common_time).samples
                    b_resampled = b_sig.interp(common_time).samples
                    samples = a_resampled - b_resampled
                    ts = common_time

                # Derived: Delta SoC with time alignment
                elif name == "CellSocMax - CellSocMin":
                    a_sig = mdf.get("CellSocMax")
                    b_sig = mdf.get("CellSocMin")
                    common_time = a_sig.timestamps if len(a_sig.timestamps) <= len(b_sig.timestamps) else b_sig.timestamps
                    a_resampled = a_sig.interp(common_time).samples
                    b_resampled = b_sig.interp(common_time).samples
                    samples = a_resampled - b_resampled
                    ts = common_time

                # Derived: Actual power
                elif name == "PackVoltage * PackCurrent":
                    a = mdf.get("PackVoltage").samples
                    b = mdf.get("PackCurrent").samples
                    ts = mdf.get("PackVoltage").timestamps
                    samples = a * b / 1000
                    actual_power_samples = samples

                # Raw signal
                else:
                    sig = mdf.get(name)
                    samples = sig.samples
                    ts = sig.timestamps
                    if "Chrgn" in name:
                        samples = samples * -1

                entry = {
                    "group": group,
                    "name": name,
                    "unit": "kW" if "*" in name else "degC" if "-" in name and "T" in name else "V" if "CellU" in name else sig.unit,
                    "samples": samples,
                    "timestamps": ts,
                    "min": float(np.min(samples)),
                    "max": float(np.max(samples))
                }
                entry["delta"] = entry["max"] - entry["min"]
                data.append(entry)
                group_map[group].append(entry)

                if name == "StateOfCharge":
                    soc_samples = samples
                if name == "PackCurrent":
                    current_samples = samples
            except:
                continue

    # Usage mode check: remove charge limit if discharge test (SoC decreasing)
    if len(soc_samples) >= 2 and soc_samples[-1] < soc_samples[0]:
        if "Current" in group_map:
            group_map["Current"] = [d for d in group_map["Current"] if d["name"] != "ChargeCurrentLimit"]

    return data, group_map, soc_samples, actual_power_samples, current_samples

# === Analyze total duration from first signal ===
def analyze_duration(sig_data):
    for row in sig_data:
        if row["timestamps"] is not None and len(row["timestamps"]) > 1:
            ts = row["timestamps"]
            return float(ts[-1] - ts[0])
    return 0

# === Summarize key metrics for report header ===
def export_summary(data, soc, power_samples, current_samples, duration):
    # Calculate SoC range from start to end
    soc_range = f"{float(soc[0]):.2f} -> {float(soc[-1]):.2f}" if len(soc) else "N/A"

    # Extract power value with highest absolute value, keeping sign
    peak_power_val = power_samples[np.argmax(np.abs(power_samples))] if len(power_samples) else None
    peak_power = f"{peak_power_val:.2f} kW" if peak_power_val is not None else "N/A"

    # Compute RMS current
    rms_current = f"{float(np.sqrt(np.mean(np.square(current_samples)))):.2f} A" if len(current_samples) else "N/A"

    # Find maximum temperature from TMax signal
    max_temp = next((d for d in data if d["name"] == "CellTempMax"), None)
    max_temp_val = f"{max_temp['max']:.2f} °C" if max_temp else "N/A"

    # Find max delta voltage and convert to mV
    delta_v = next((d for d in data if d["name"] == "CellVoltageMax - CellVoltageMin"), None)
    max_delta_mv = f"{delta_v['max'] * 1000:.0f} mV" if delta_v else "N/A"

    # Find max delta SoC
    delta_soc = next((d for d in data if d["name"] == "CellSocMax - CellSocMin"), None)
    max_delta_soc = f"{delta_soc['max']:.2f} %" if delta_soc else "N/A"

    return {
        "log_duration": f"{duration:.2f} s",
        "soc_range": soc_range,
        "peak_power": peak_power,
        "rms_current": rms_current,
        "max_temp": max_temp_val,
        "max_delta_mv": max_delta_mv,
        "max_delta_soc": max_delta_soc
    }

# === Generate PDF report with metrics table and plots ===
def export_pdf(data, summary, fname, group_map):
    base_name = os.path.splitext(fname)[0]
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    # Report title and file
    pdf.cell(0, 10, "MF4 Analysis Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Logfile: {fname}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Bullet-style summary header section
    bullet = [
        f"- Log Duration     : {summary['log_duration']}",
        f"- SoC Range        : {summary['soc_range']}",
        f"- Peak Power       : {summary['peak_power']}",
        f"- Current RMS      : {summary['rms_current']}",
        f"- Max Cell Temperature    : {summary['max_temp']}",
        f"- Max delta Cell Voltage  : {summary['max_delta_mv']}",
        f"- Max delta SoC  : {summary['max_delta_soc']}"
    ]
    for line in bullet:
        pdf.cell(0, 8, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)

    # Table column headers
    headers = ["Metric", "Signal", "Unit", "Min", "Max"]
    widths = [35, 80, 15, 25, 25]
    pdf.set_font("Helvetica", style="B", size=10)
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 8, h, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", size=9)

    # Populate table rows group by group, using keyword map order
    for group in list(KEYWORD_MAP.keys()):
        for name in KEYWORD_MAP[group]:
            match = next((d for d in group_map.get(group, []) if d["name"] == name), None)
            if match:
                row = [group, match["name"], match["unit"], f"{match['min']:.2f}", f"{match['max']:.2f}"]
                for i, val in enumerate(row):
                    pdf.cell(widths[i], 6, val, border=1)
                pdf.ln()

    pdf.ln(4)

    # Embed PNG plots for each group
    plot_order = list(KEYWORD_MAP.keys())
    for group in plot_order:
        img_file = os.path.join(EXPORT_DIR, f"{base_name}_{group.lower().replace(' ', '_')}.png")
        if os.path.exists(img_file):
            pdf.image(img_file, x=15, w=180)

    # Finalize and save the full PDF report
    pdf.output(os.path.join(EXPORT_DIR, f"{base_name}_mf4_analysis_report.pdf"))

# === Export signal plots for each group into PNG ===
def export_group_plots(group_map, base_name):
    # Define the plot export order based on keyword map
    plot_order = list(KEYWORD_MAP.keys())
    for group in plot_order:
        signals = []
        # Ensure signal order respects the KEYWORD_MAP
        for name in KEYWORD_MAP[group]:
            match = next((d for d in group_map.get(group, []) if d["name"] == name), None)
            if match:
                signals.append(match)
        if not signals:
            continue

        # Create figure and axis
        fig, ax1 = plt.subplots(figsize=(10, 3))
        ax2 = ax1.twinx() if group == "Cell Voltage" else None  # Enable second y-axis if needed

        for sig in signals:
            timestamps = sig["timestamps"]
            samples = sig["samples"]
            label = sig["name"]

            # Label adjustment for Cell Voltage
            if group == "Cell Voltage":
                if label == "CellVoltageMax" or label == "CellVoltageMin":
                    label += " (V)"
                elif label == "CellVoltageMax - CellVoltageMin":
                    label += " (mV)"

            # Plot Cell Voltage derived signal on right axis, scaled to mV
            if group == "Cell Voltage" and "-" in label:
                ax2.plot(timestamps, samples * 1000, label=label, color="green")
            else:
                ax1.plot(timestamps, samples, label=label)

        # General plot formatting
        ax1.grid(True)
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(signals[0]["unit"] if signals else "")
        if ax2:
            ax2.set_ylabel("mV")

        # Adjust space and legend layout
        fig.subplots_adjust(top=0.82)
        fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.945), ncol=min(len(signals), 3), frameon=False)

        # Save PNG plot
        filename = f"{base_name}_{group.lower().replace(' ', '_')}.png"
        path = os.path.join(EXPORT_DIR, filename)
        plt.savefig(path, bbox_inches="tight")
        plt.close()

# === Export signal metadata (no samples) to JSON ===
def export_summary_json(data, base_name):
    filename = f"{base_name}_signal_summary.json"
    path = os.path.join(EXPORT_DIR, filename)
    # Strip out large sample arrays from export
    clean_data = [{k: v for k, v in d.items() if k not in ["samples", "timestamps"]} for d in data]
    with open(path, "w") as f:
        json.dump(clean_data, f, indent=2)

# === Main processing pipeline ===
def main():
    # Load latest .mf4 file
    mdf, fname = load_latest_mf4()
    base_name = os.path.splitext(fname)[0]

    # Extract signals and usage-specific outputs
    data, group_map, soc, power_samples, current_samples = extract_signals(mdf)

    # Analyze total test duration
    duration = analyze_duration(data)

    # Extract test summary for reporting
    summary = export_summary(data, soc, power_samples, current_samples, duration)

    # Export structured signal metadata to JSON
    export_summary_json(data, base_name)

    # Export grouped signal plots
    export_group_plots(group_map, base_name)

    # Generate final PDF report
    export_pdf(data, summary, fname, group_map)

# === Entry point ===
if __name__ == "__main__":
    main()