from asammdf import MDF
import os
import logging
from tqdm import tqdm

# ✅ Script Settings
use_logging = True                                # Toggle terminal logging
input_dir = "."                                    # Folder with .mf4 files (default: current folder)
output_dir = "mf4_to_csv"                         # Output folder for .csv files (auto-created)

# ✨ Signal filter — update with your desired signal names (e.g. voltage, current)
# For GitHub and public repos, use placeholders to avoid exposing proprietary names.
signals_to_export = ["Signal1", "Signal2", "Signal3"]  # Replace locally for real use

# ✅ Logging setup
if use_logging:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ✅ Create output folder
os.makedirs(output_dir, exist_ok=True)

# ✅ Find all .mf4 files
mf4_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".mf4")]

# ✅ Convert each file
for file in tqdm(mf4_files, desc="Converting", unit="file"):
    input_path = os.path.join(input_dir, file)
    output_name = os.path.splitext(file)[0] + ".csv"
    output_path = os.path.join(output_dir, output_name)

    if use_logging:
        logging.info(f"Converting {file} → {output_path}")
    else:
        print(f"Converting {file} → {output_path}")

    try:
        mdf = MDF(input_path)
        available = mdf.channels_db.keys()
        selected = [s for s in signals_to_export if s in available]

        if not selected:
            logging.warning(f"⚠️ No selected signals found in {file}, skipping.")
            continue

        filtered_mdf = mdf.select(selected)
        df = filtered_mdf.to_dataframe()
        df.to_csv(output_path, index=False)

    except Exception as e:
        logging.error(f"❌ Failed to convert {file}: {e}")

# ✅ Done
msg = f"✅ All files processed. Output saved in: {output_dir}"
logging.info(msg) if use_logging else print(msg)
