# MF4 to CSV Converter (with Logging + Progress Bar)

This Python script converts all `.mf4` files in the **current folder** into `.csv` format using the `asammdf` library.  
It includes optional logging and a progress bar via `tqdm`.

---

## 📁 Folder Setup

You can either:

### ✅ Option 1 — Current folder
```
your-folder/
├── mf4_to_csv_with_logging.py
├── file1.mf4
├── file2.mf4
└── mf4_to_csv/        # Output folder (auto-created)
```

### 📂 Option 2 — Subfolder setup (Optional)
```
your-folder/
├── mf4_to_csv_with_logging.py
├── mf4_files/
│   ├── file1.mf4
│   └── file2.mf4
└── mf4_to_csv/        # Output folder (auto-created)
```

> 🔁 To use Option 2, just uncomment `input_dir = "mf4_files"` in the script.

---

## 🚀 How to Use

1. Install required libraries:
   ```bash
   pip install asammdf tqdm
   ```

2. Place your `.mf4` files in the **same folder as the script** *(or in `mf4_files/` if using Option 2)*.

3. Run the script:
   ```bash
   python mf4_to_csv_with_logging.py
   ```

4. Your `.csv` files will appear in the `mf4_to_csv/` folder.

---

## 🔧 Features

- ✅ Converts all `.mf4` files in the folder
- ✅ Creates `.csv` files with the same names
- ✅ Auto-creates output folder if it doesn’t exist
- ✅ Logs progress and shows a terminal progress bar

---

## 🧠 Notes

- Toggle logging with the `use_logging` variable at the top of the script.
- Adjust `input_dir` if you want to use a separate folder.
- All `.csv` files go to `mf4_to_csv/`.

---

## 🔮 Future Ideas

- [ ] Add command-line arguments for flexibility
- [ ] Allow filtering of specific signals
- [ ] Export logs to file
