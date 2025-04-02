import os
from asammdf import MDF
import numpy as np
import matplotlib.pyplot as plt 

# === SETTINGS ===
input_dir = "."
filter_keyword = "YourKeywordHere"  # Filter signals by this keyword
plot_signal = "ExampleSignal123"  # Signal to plot

mf4_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".mf4")]
if not mf4_files:
    print("❌ No .mf4 files found in current folder.")
    exit()

# 📂 Sort files by modification time (latest first)
mf4_files.sort(key=lambda f: os.path.getmtime(os.path.join(input_dir, f)), reverse=True)

# === Load newest file ===
for file in mf4_files:
    path = os.path.join(input_dir, file)
    try:
        mdf = MDF(path)
        print(f"\n✅ Loaded file: {file}")
        break
    except Exception as e:
        print(f"⚠️ Failed to load {file}: {e}")
else:
    print("❌ Could not load any .mf4 files.")
    exit()

# === Summary ===
total_signals = len(mdf.channels_db)
print(f"\n📊 Total signals: {total_signals}")

timestamps = None
for ch_name in mdf.channels_db:
    try:
        sig = mdf.get(ch_name, group=0)
        timestamps = sig.timestamps
        break
    except:
        continue

if timestamps is not None and len(timestamps) > 1:
    duration = timestamps[-1] - timestamps[0]
    avg_step = np.mean(np.diff(timestamps))
    print(f"🕒 File duration: {duration:.2f} seconds")
    print(f"⏱ Avg time step: {avg_step:.6f} seconds")
else:
    print("⚠️ Could not extract time info.")

# === Filtered Signal Preview ===
print(f"\n🔍 Signals matching filter: '{filter_keyword}'\n")
filtered_signals = [name for name in mdf.channels_db if filter_keyword.lower() in name.lower()]
if not filtered_signals:
    print("⚠️ No signals matched the filter.")
else:
    for name in filtered_signals:
        try:
            sig = mdf.get(name)
            print(f"• {name} | Unit: {sig.unit} | Samples: {len(sig.samples)}")
        except:
            print(f"• {name} ⚠️ (could not read)")

# === Plot Selected Signal ===
print(f"\n📈 Attempting to plot: {plot_signal}")
try:
    sig = mdf.get(plot_signal)
    plt.switch_backend('tkagg')  # Ensure plot window works properly
    plt.figure(figsize=(12, 4))
    plt.plot(sig.timestamps, sig.samples, label=plot_signal)
    plt.title(f"Signal: {plot_signal}")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{sig.unit}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.pause(0.001)  # Show plot non-blocking
    input("\n✅ Plot displayed. Press Enter to exit...")
except Exception as e:
    print(f"⚠️ Could not plot {plot_signal}: {e}")
