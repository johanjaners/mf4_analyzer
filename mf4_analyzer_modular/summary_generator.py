# # mf4_analyzer_modular/summary_generator.py
import numpy as np
from mf4_analyzer_modular.compute_metrics import compute_charging_metrics, compute_discharge_metrics, compute_rms_power

# === Summary Generator ===
def generate_summary(data, derived):
    soc = derived.get("StateOfCharge", {}).get("samples", [])
    time = derived.get("StateOfCharge", {}).get("timestamps", [])
    power = derived.get("Actual Power", {}).get("samples", [])
    current = derived.get("PackCurrent", {}).get("samples", [])

    soc_range = f"{soc[0]:.2f} -> {soc[-1]:.2f}" if len(soc) else "N/A"
    peak_power_val = power[np.argmax(np.abs(power))] if len(power) else None
    peak_power = f"{peak_power_val:.2f} kW" if peak_power_val is not None else "N/A"
    rms_current = f"{float(np.sqrt(np.mean(np.square(current)))):.2f} A" if len(current) else "N/A"

    def find(name):
        return next((d for d in data if d["name"] == name), None)

    max_temp = find("CellTempMax")
    delta_v = find("Delta Cell Voltage")
    delta_soc = find("Delta SoC")

    # Define summary before updating
    summary = {
        "Log Duration": f"{derived['StateOfCharge']['timestamps'][-1] - derived['StateOfCharge']['timestamps'][0]:.2f} s" if len(soc) else "N/A",
        "SoC Range": soc_range,
        "Peak Power": peak_power,
        "Current RMS": rms_current,
        "Max Cell Temperature": f"{max_temp['max']:.2f} °C" if max_temp else "N/A",
        "Max delta Cell Voltage": f"{delta_v['max']:.0f} mV" if delta_v else "N/A",
        "Max delta SoC": f"{delta_soc['max']:.2f} %" if delta_soc else "N/A"
    }

    # always-safe metrics, then mode-specific
    for entry in compute_rms_power(derived):
        summary[entry["name"]] = f"{entry['value']} {entry['unit']}"

    # === Append derived metrics based on mode ===
    mode = derived.get("Mode", "Idle")
    if mode == "Charging":
        for entry in compute_charging_metrics(derived):
            summary[entry["name"]] = f"{entry['value']} {entry['unit']}"
    elif mode == "Discharging":
        for entry in compute_discharge_metrics(derived):
            summary[entry["name"]] = f"{entry['value']} {entry['unit']}"

    return summary
