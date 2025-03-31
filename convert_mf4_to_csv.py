from asammdf import MDF
import os
import logging
from tqdm import tqdm

# Toggle logging and progress bar
use_logging = True

# Setup logging if enabled
if use_logging:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Define folders
input_dir = "mf4_files"
output_dir = "mf4_to_csv"  # 📂 Output folder

# Create output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all .mf4 files
mf4_files = [f for f in os.listdir(input_dir) if f.endswith(".mf4")]

# Loop through all .mf4 files
for file in tqdm(mf4_files, desc="Converting", unit="file"):
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".csv")

    if use_logging:
        logging.info(f"Converting {file} → {output_path}")
    else:
        print(f"Converting {file} → {output_path}")

    mdf = MDF(input_path)
    mdf.export(output_path, fmt="csv")

# Final message
msg = f"All files converted to {output_dir}"
logging.info(msg) if use_logging else print("✅", msg)
