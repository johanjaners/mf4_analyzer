# # mf4_analyzer_modular/metrics_list.py
# === Metric Configuration Module ===

# --- List of all signal evaluations (raw and derived) ---

# === SIGNAL_LIST Format ===
# Each entry defines a metric to extract and optionally derive:
#   - "metric": logical group (e.g. "Power", "SoC") for plot/PDF
#   - "signal": raw signal or formula (e.g. "A - B" or "X * Y")
#   - "name" (optional): custom label for plot/PDF; defaults to "signal"
#   - "unit_override" (optional): string to override signal unit for display
#   - "scaling_factor" (optional): numerical factor applied to signal values
# Signals can be derived from raw signals or earlier derived names.


SIGNAL_LIST = [
    {"metric": "Current", "signal": "PackCurrent"},
    {"metric": "Current", "signal": "ChargeCurrentLimit", "scaling_factor": -1},

    {"metric": "Power", "name": "Actual Power", "signal": "PackVoltage * PackCurrent", "unit_override": "kW", "scaling_factor": 1e-3},
    {"metric": "Power", "signal": "DischargePowerLimit"},
    {"metric": "Power", "signal": "ChargePowerLimit", "scaling_factor": -1},

    {"metric": "Temperature", "signal": "CellTempMax"},
    {"metric": "Temperature", "signal": "CellTempMin"},
    {"metric": "Temperature", "signal": "CoolantInletTemp"},

    {"metric": "Temperature Delta", "name": "Delta Cell Temperature", "signal": "CellTempMax - CellTempMin"},
    {"metric": "Temperature Delta", "name": "Cell-Coolant DeltaT", "signal": "CellTempMax - CoolantInletTemp"},

    {"metric": "Cell Voltage", "signal": "CellVoltageMax"},
    {"metric": "Cell Voltage", "signal": "CellVoltageMin"},

    {"metric": "Delta Cell Voltage", "name": "Delta Cell Voltage", "signal": "CellVoltageMax - CellVoltageMin", "unit_override": "mV", "scaling_factor": 1e3},

    {"metric": "SoC", "signal": "StateOfCharge"},
    {"metric": "SoC", "signal": "CellSocMin"},
    {"metric": "SoC", "signal": "CellSocMax"},

    {"metric": "Delta SoC", "name": "Delta SoC", "signal": "CellSocMax - CellSocMin"},

    {"metric": "Fault Flags", "signal": "SystemFaultIndicator"}
]