# MF4 to CSV Converter (with Logging + Progress Bar)

This Python script converts all `.mf4` files in the `mf4_files/` folder into `.csv` format, using the `asammdf` library. It includes optional logging and a terminal-based progress bar with `tqdm`.

---

## 📁 Folder Structure

```
project-folder/
├── convert_mf4_to_csv.py         # or mf4_to_csv_with_logging.py
├── mf4_files/                    # Place your .mf4 files here
└── mf4_to_csv/                   # Auto-created folder for CSV output
```

---

## ⚙️ How to Use

1. Install required libraries:
   ```bash
   pip install asammdf tqdm
   ```

2. Place `.mf4` files inside the `mf4_files/` folder.

3. Run the script:
   ```bash
   python mf4_to_csv_with_logging.py
   ```

4. Converted `.csv` files will appear in the `mf4_to_csv/` folder.

---

## 🔧 Features

- ✅ Batch conversion of `.mf4` files
- ✅ Output `.csv` files named after original input files
- ✅ Optional logging with timestamps and info
- ✅ Clean progress bar via `tqdm`

---

## 🔮 Potential Future Features

- [ ] Command-line argument support for input/output folders
- [ ] Signal-level filtering during conversion
- [ ] Save logs to external file
