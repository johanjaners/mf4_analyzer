from asammdf import MDF

# Load your MF4 file
mdf = MDF("your_file.mf4")

# Export all channels to CSV
mdf.export("output.csv", fmt="csv")

print("Done! Exported to output.csv ✅")
