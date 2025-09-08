import os
import matplotlib.pyplot as plt

# === Generate plot filename for a given metric ===
# Returns: full path to PNG image based on export dir, base filename, and metric name
def get_plot_filename(metric: str, base_name: str) -> str:
    return os.path.join("mf4_exports", f"{base_name}_{metric.lower().replace(' ', '_')}.png")

# === Export grouped signal plots by metric ===
# Each metric group is plotted into a shared figure with labeled curves
# Saves plots as PNGs named using get_plot_filename()
def export_group_plots(metric_map: dict, base_name: str):
    for metric, signals in metric_map.items():
        if not signals:
            continue

        fig, ax1 = plt.subplots(figsize=(10, 3))
        y_label = signals[0]["unit"]

        for signal in signals:
            samples = signal["samples"]
            timestamps = signal["timestamps"]
            unit = signal["unit"]
            label = f"{signal['name']} ({unit})"
            ax1.plot(timestamps, samples, label=label)

        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(y_label)
        ax1.grid(True)

        # Add legend above plot
        fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.945), ncol=min(3, len(signals)), frameon=False)
        fig.subplots_adjust(top=0.82)

        # Save plot to export folder
        filename = get_plot_filename(metric, base_name)
        plt.savefig(filename, bbox_inches="tight")
        plt.close()