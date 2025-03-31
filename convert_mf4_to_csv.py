from asammdf import MDF
import os

# Define folders
input_dir = "mf4_files"
output_dir = "mf4_to_csv"  # 📂 Output folder

# Create output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through all .mf4 files in input_dir
for file in os.listdir(input_dir):
    if file.endswith(".mf4"):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".csv")

        print(f"📂 Converting {file} → {output_path}")
        mdf = MDF(input_path)
        mdf.export(output_path, fmt="csv")

print("✅ All files converted to", output_dir)
