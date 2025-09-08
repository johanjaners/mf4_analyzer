import os
import csv
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from mf4_analyzer_modular.metrics_list import SIGNAL_LIST
from mf4_analyzer_modular.plotter_exporter import get_plot_filename


# === PDF Export ===
# Generates analysis report with summary, metrics table, and embedded plots
def export_pdf(data, summary, fname, metric_map):
    base_name = os.path.splitext(fname)[0]
    pdf = FPDF()
    pdf.set_font("Helvetica", size=11)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Report header
    pdf.cell(0, 10, "MF4 Analysis Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Logfile: {fname}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Summary metrics
    for label, value in summary.items():
        pdf.cell(0, 8, f"- {label:<25}: {value}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)

    # --- PDF Table Headers ---
    TABLE_HEADERS = ["Metric", "Signal", "Unit", "Min", "Max"]
    TABLE_WIDTHS = [35, 80, 15, 25, 25]

    # Table headers
    pdf.set_font("Helvetica", style="B", size=10)
    for i, h in enumerate(TABLE_HEADERS):
        pdf.cell(TABLE_WIDTHS[i], 8, h, border=1)
    pdf.ln()

    # Table values
    pdf.set_font("Helvetica", size=9)
    for entry in SIGNAL_LIST:
        metric = entry["metric"]
        name = entry.get("name", entry["signal"])
        match = next((d for d in metric_map.get(metric, []) if d["name"] == name), None)
        if match:
            row = [
                metric,
                name,
                match["unit"],
                f"{match['min']:.2f}",
                f"{match['max']:.2f}"
            ]
            for i, val in enumerate(row):
                pdf.cell(TABLE_WIDTHS[i], 6, val, border=1)
            pdf.ln()

    # Plot images
    pdf.ln(4)
    for metric in metric_map:
        img_file = get_plot_filename(metric, base_name)
        if os.path.exists(img_file):
            pdf.image(img_file, x=15, w=180)


    pdf.output(os.path.join("mf4_exports", f"{base_name}_mf4_analysis_report.pdf"))

# === CSV Export ===
def export_csv(data, base_name):
    """
    One CSV per log:
        mf4_exports/<base_name>.csv

    Includes:
    file_key, group, name, unit, min, max, delta, value
    - For signals → min/max/delta filled, value blank
    - For computed metrics → value filled, min/max/delta blank
    """
    os.makedirs("mf4_exports", exist_ok=True)
    out_path = os.path.join("mf4_exports", f"{base_name}.csv")

    fieldnames = ["file_key", "name", "unit", "min", "max", "delta", "value"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        for d in data:
            row = {
                "file_key": base_name,
                "name":  d.get("name", ""),
                "unit":  d.get("unit", ""),
                "min":   d.get("min", ""),
                "max":   d.get("max", ""),
                "delta": d.get("delta", ""),
                "value": d.get("value", ""),
            }
            w.writerow(row)
