## mf4_analyzer_modular/signal_extractor.py
import numpy as np
from scipy.interpolate import interp1d
from mf4_analyzer_modular.signal_config import SIGNAL_CONFIG
from mf4_analyzer_modular.metrics_list import SIGNAL_LIST


# === Safe Operation Helper ===
def safe_op(a, b, ts_a, ts_b, op='/'):
    try:
        if len(a) > len(b):
            interp = interp1d(ts_b, b, bounds_error=False, fill_value="extrapolate")
            b_resampled = interp(ts_a)
            a_resampled = a
            t_common = ts_a
        else:
            interp = interp1d(ts_a, a, bounds_error=False, fill_value="extrapolate")
            a_resampled = interp(ts_b)
            b_resampled = b
            t_common = ts_b

        if op == '+':
            result = a_resampled + b_resampled
        elif op == '-':
            result = a_resampled - b_resampled
        elif op == '*':
            result = a_resampled * b_resampled
        elif op == '/':
            result = a_resampled / np.clip(b_resampled, 1e-6, None)
        else:
            raise ValueError(f"Unsupported operation: {op}")

        return result, t_common
    except Exception as e:
        print(f"[SAFE_OP ERROR] op={op}: {e}")
        return np.array([]), np.array([])



# === Detect user mode ===
# Mode is determined by the first and last SoC values:
# - If SoC decreases, it's "Discharge" 
# - If SoC increases, it's "Charge"
# - If SoC is constant or has only one value, we assume "Idle" (default)
def detect_mode(soc: np.ndarray) -> str:
    if len(soc) < 2:
        return "Idle"
    if soc[0] > soc[-1]:
        return "Discharging"
    if soc[-1] > soc[0]:
        return "Charging"
    return "Idle"


# === Signal Extraction and Evaluation ===
def extract_signals(mdf):
    signal_data = {}
    derived = {}
    results = []
    metric_map = {}

    # Load raw signals
    for entry in SIGNAL_LIST:
        sig_expr = entry["signal"]
        for token in sig_expr.replace("*", " ").replace("-", " ").replace("/", " ").split():
            if token in SIGNAL_CONFIG and token not in signal_data:
                try:
                    sig = mdf.get(SIGNAL_CONFIG[token])
                    signal_data[token] = {
                        "samples": sig.samples,
                        "timestamps": sig.timestamps,
                        "unit": getattr(sig, 'unit', '')
                    }
                except Exception as e:
                    print(f"[WARN] Failed to load: {token} -> {e}")

    # === Detect operating mode ===
    soc_signal = signal_data.get("StateOfCharge")
    if soc_signal:
        mode = detect_mode(soc_signal["samples"])
    else:
        mode = "Unknown"

    # Evaluate entries
    for entry in SIGNAL_LIST:
        name = entry.get("name", entry["signal"])
        expr = entry["signal"]
        metric = entry["metric"]


        # === Conditional metric exclusion ===
        if name in ["ChargeCurrentLimit", "ChargePowerLimit"] and mode != "Charging":
            continue # Skip charge limits if not charging
        

        try:
            if '-' in expr:
                a, b = [x.strip() for x in expr.split('-')]
                a_data = derived.get(a) or signal_data.get(a)
                b_data = derived.get(b) or signal_data.get(b)
                if not a_data or not b_data:
                    raise ValueError(f"Missing signal in expression '{expr}': {a if not a_data else b}")
                samples, timestamps = safe_op(a_data["samples"], b_data["samples"],
                                              a_data["timestamps"], b_data["timestamps"], op='-')
                unit = a_data.get("unit", "")

            elif '*' in expr:
                l, r = [x.strip() for x in expr.split('*')]
                l_data = derived.get(l) or signal_data.get(l)
                r_data = derived.get(r) or signal_data.get(r)
                if not l_data or not r_data:
                    raise ValueError(f"Missing signal in expression '{expr}': {l if not l_data else r}")
                samples, timestamps = safe_op(l_data["samples"], r_data["samples"],
                                              l_data["timestamps"], r_data["timestamps"], op='*')
                unit = entry.get("unit_override", l_data.get("unit", ""))

            elif '/' in expr:
                n, d = [x.strip() for x in expr.split('/')]
                n_data = derived.get(n) or signal_data.get(n)
                d_data = derived.get(d) or signal_data.get(d)
                if not n_data or not d_data:
                    raise ValueError(f"Missing signal in expression '{expr}': {n if not n_data else d}")
                samples, timestamps = safe_op(n_data["samples"], d_data["samples"],
                                              n_data["timestamps"], d_data["timestamps"], op='/')
                unit = entry.get("unit_override", "") or n_data.get("unit", "")

            else:
                src = derived.get(expr) or signal_data.get(expr)
                if not src:
                    raise ValueError(f"Missing signal: {expr}")
                samples = src["samples"]
                timestamps = src["timestamps"]
                unit = src.get("unit", "")

            samples = samples * entry.get("scaling_factor", 1)
            unit = entry.get("unit_override", unit)

            stat = {
                "metric": metric,
                "name": name,
                "unit": unit,
                "samples": samples,
                "timestamps": timestamps,
                "min": round(float(np.min(samples)), 2),
                "max": round(float(np.max(samples)), 2),
                "delta": round(float(np.max(samples) - np.min(samples)), 2)
            }

            results.append(stat)
            derived[name] = {
                "samples": samples,
                "timestamps": timestamps,
                "unit": unit
            }
            metric_map.setdefault(metric, []).append(stat)

        except Exception as e:
            print(f"[ERROR] Failed to evaluate {name}: {e}")

    return results, metric_map, derived
