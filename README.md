# MF4 to CSV Converter

This script batch converts `.mf4` files to `.csv` using the `asammdf` library.

---

## 📂 Folder Structure

```
project-folder/
├── convert_mf4_to_csv.py
├── mf4_files/          # Put your .mf4 files here
└── mf4_to_csv/         # Output folder (auto-created)
```

---

## 🚀 How to Use

1. Install the required library:
   ```bash
   pip install asammdf
   ```

2. Add `.mf4` files to `mf4_files/`.

3. Run the script:
   ```bash
   python convert_mf4_to_csv.py
   ```

4. Converted `.csv` files will appear in `mf4_to_csv/`.

---

## 🛠️ Future Improvements

- [ ] Add support for specific signal filtering
- [ ] Option to select custom input/output folders
- [ ] Add logging and progress bar
