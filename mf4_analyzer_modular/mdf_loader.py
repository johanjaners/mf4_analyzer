import os
from asammdf import MDF

def load_latest_mdf(directory):
    files = sorted(
        [f for f in os.listdir(directory) if f.endswith((".mf4", ".dat"))],
        key=lambda x: os.path.getmtime(os.path.join(directory, x)),
        reverse=True
    )
    for file in files:
        try:
            return MDF(os.path.join(directory, file)), file
        except Exception as e:
            print(f"[WARN] Failed to load {file}: {e}")
            continue
    raise FileNotFoundError("No valid MDF (.mf4/.dat) file found.")
