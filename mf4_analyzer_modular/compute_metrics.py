## compute_metrics.py
import numpy as np

# === Computed Metric Functions ===
# Each function returns a list of computed metrics, where each entry is a dictionary:
# { "name": <metric name>, "value": <numeric value>, "unit": <string> }
#
# Units must be included directly in each metric return.
# Metric naming must be consistent with summary/report expectations.
# No external metric/unit lookup is used — all values are self-contained.

# --- Power threshold for active logic ---
CHARGE_ACTIVE_THRESHOLD_KW    = -5.0  # negative power = charging
DISCHARGE_ACTIVE_THRESHOLD_KW = 5.0   # ignore idle/noise

# Charging metric threshold
DERIVATIVE_THRESHOLD   = 1e-3     # %-pts/s (very small, just needs to be >0)

# === Computed Metrics ===
#     {"name": "Charging Time", "unit": "s"},
#     {"name": "Charging Power Avg", "unit": "kW"},
#     {"name": "DischargeActive Power Avg", "unit": "kW"},
#     {"name": "DischargeActive Duration", "unit": "s"},
#     {"name": "Power RMS", "unit": "kW"}
# ]

# --- Simple & robust charging-time (SoC-derivative based) ---
def compute_charging_time(timestamps: np.ndarray, soc: np.ndarray) -> float:
    """
    Return total charging duration in seconds based on when SoC is increasing.
    """
    if len(soc) < 3:
        return 0.0

    # Smooth derivative to ignore noise
    dsoc = np.gradient(soc)
    active_indices = np.where(dsoc > DERIVATIVE_THRESHOLD)[0]  # threshold for SoC increase

    if len(active_indices) < 2:
        return 0.0

    start_idx = active_indices[0]
    end_idx = active_indices[-1]
    return float(timestamps[end_idx] - timestamps[start_idx])


# === Compute charge metrics ===
def compute_charging_metrics(derived: dict) -> list[dict]:
    if derived.get("Mode") != "Charging":
        return [] # Hard gate by mode to avoid false positives on discharge/idle logs

    # --- inputs ---
    soc = np.asarray(derived.get("StateOfCharge", {}).get("samples", []), float)
    ts  = np.asarray(derived.get("StateOfCharge", {}).get("timestamps", []), float)
    p   = np.asarray(derived.get("Actual Power", {}).get("samples", []), float)
    tp  = np.asarray(derived.get("Actual Power", {}).get("timestamps", []), float)

    if soc.size < 3 or ts.size < 3:
        return []

    # --- sanitize & order ---
    idx = np.argsort(ts)
    ts, soc = ts[idx], soc[idx]
    m = np.isfinite(ts) & np.isfinite(soc)
    ts, soc = ts[m], soc[m]
    if ts.size < 3:
        return []

    # --- Charging Time via simple SoC-derivative method (validated) ---
    charge_time = compute_charging_time(ts, soc)
    out = [{"name": "Charging Time", "value": round(float(charge_time), 2), "unit": "s"}]

    # --- optional: average charging power (time-weighted, negative = charging) ---
    if p.size >= 2 and tp.size >= 2:
        ordp = np.argsort(tp); tp, p = tp[ordp], p[ordp]
        mp = np.isfinite(tp) & np.isfinite(p); tp, p = tp[mp], p[mp]
        if tp.size >= 2:
            dtp = np.diff(tp)
            mask = p[:-1] < CHARGE_ACTIVE_THRESHOLD_KW  # negative power = charging
            if np.any(mask):
                avg_pow = float(np.sum(p[:-1][mask] * dtp[mask]) / np.sum(dtp[mask]))
                out.append({"name": "Charging Power Avg", "value": round(avg_pow, 2), "unit": "kW"})

    return out


# === Compute discharge metrics ===
def compute_discharge_metrics(derived: dict) -> list[dict]:
    if derived.get("Mode") != "Discharging":
        return []  # hard gate by mode

    p  = np.asarray(derived.get("Actual Power", {}).get("samples", []), float)
    t  = np.asarray(derived.get("Actual Power", {}).get("timestamps", []), float)
    if p.size < 2 or t.size < 2:
        return []

    dt = np.diff(t)
    dis_i = p[:-1] > DISCHARGE_ACTIVE_THRESHOLD_KW  # threshold, no abs, discharging only
    if not dis_i.any():
        return []

    active_time = float(np.sum(dt[dis_i]))
    avg_power   = float(np.sum(p[:-1][dis_i] * dt[dis_i]) / active_time)

    return [
        {"name": "DischargeActive Duration", "value": round(active_time, 2), "unit": "s"},
        {"name": "DischargeActive Power Avg", "value": round(avg_power, 2), "unit": "kW"},
    ]

# === Compute RMS Power ===
def compute_rms_power(derived: dict) -> list[dict]:
    if "Actual Power" not in derived:
        return []

    power = derived["Actual Power"]["samples"]
    rms = round(float(np.sqrt(np.mean(np.square(power)))), 2)
    return [{"name": "Power RMS", "value": rms, "unit": "kW"}]
