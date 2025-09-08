## mf4_analyzer.py
import os
import numpy as np
from mf4_analyzer_modular.mdf_loader import load_latest_mdf
from mf4_analyzer_modular.signal_extractor import extract_signals, detect_mode
from mf4_analyzer_modular.compute_metrics import compute_discharge_metrics, compute_charging_metrics, compute_rms_power
from mf4_analyzer_modular.summary_generator import generate_summary
from mf4_analyzer_modular.plotter_exporter import export_group_plots
from mf4_analyzer_modular.pdf_exporter import export_pdf, export_csv

# === Paths ===
INPUT_DIR = "./mf4_logfiles"
EXPORT_DIR = "./mf4_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def main():
    # Load latest MDF file
    mdf, fname = load_latest_mdf("./mf4_logfiles")
    base_name = os.path.splitext(fname)[0]

    # Extract signal data
    data, metric_map, derived = extract_signals(mdf)

    # Detect mode and normalize labels
    mode_raw = detect_mode(derived.get("StateOfCharge", {}).get("samples", np.array([])))
    mode = {"Charge": "Charging", "Discharge": "Discharging"}.get(mode_raw, mode_raw)
    derived["Mode"] = mode
    print(f"[i] Mode: {mode}")


    # Compute metrics and append
    # Always-safe metrics
    data.extend(compute_rms_power(derived))

    # Mode-specific metrics (optional; you can also let functions self-gate)
    if mode == "Charging":
        data.extend(compute_charging_metrics(derived))
    elif mode == "Discharging":
        data.extend(compute_discharge_metrics(derived))

    # Summary
    summary = generate_summary(data, derived)

    # Export
    export_csv(data, base_name)
    export_group_plots(metric_map, base_name)
    export_pdf(data, summary, fname, metric_map)

    print(f"[✓] Processed: {fname} → Output in: ./mf4_exports")

if __name__ == "__main__":
    main() 

 