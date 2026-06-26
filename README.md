# Inventory & POS System
#### Video Demo: `<URL>`
#### Description:

A command-line inventory and point-of-sale (POS) tool for small wholesale or retail businesses.
Products are stored in a local `data.csv` file. The program supports three modes:

| Mode | Command | What it does |
|------|---------|--------------|
| Buy  | `python project.py buy`    | Add new stock to the inventory |
| Sell | `python project.py sell`   | Record sales and print a receipt total |
| Report | `python project.py report` | Print a formatted inventory table |

---

## Background

I run a wholesale women's fashion business and needed a lightweight tool to track purchases,
set selling prices, and keep a running tally of what is in stock — without a heavy spreadsheet
or cloud service. This project solves that problem with nothing but Python's standard library.

---

## Project Structure

```
project.py        ← main program + all logic functions
test_project.py   ← pytest test suite (4+ tests across 3+ functions)
requirements.txt  ← pytest
data.csv          ← auto-created on first run
README.md
```

---

## Design Decisions

### Single CSV file
All inventory lives in `data.csv` with the fieldnames `id, kind, cost, shp, price, q`.
Keeping it as plain CSV makes the data human-readable and easy to inspect or edit in Excel.

### `ensure_csv()` on every read
Rather than requiring the user to create the file manually, `ensure_csv()` creates it with
the correct header on first use. This avoids the silent corruption that happens when you
open a file in append mode before any header exists.

### `process_sale()` is the heart of sell mode
The original code had the sale logic spread across `sell()` and `sell_mode()` with a global
list and a fieldname typo (`"sh.p"` instead of `"shp"`) that silently corrupted the CSV on
every sale. Extracting the logic into `process_sale()` made the bug obvious, fixed it, and
made the function independently testable.

### `calculate_total()` accepts strings
Prices read back from a CSV are strings. The original `checkout()` worked around this with
`float(i)` inside the loop, but the function signature didn't make that clear.
`calculate_total()` explicitly converts each element, which means tests can pass either
`[10.0, 5.5]` or `["10.0", "5.5"]` and get the same result.

### `find_product()` separated from mutation
Looking up a product row and modifying it are two separate concerns. Separating them lets
the test suite verify lookup independently of file I/O.

---

## How to Run

```bash
# Add stock
python project.py buy

# Sell items (Ctrl-D to checkout and see total)
python project.py sell

# View current inventory
python project.py report
```

## How to Test

```bash
pip install pytest
pytest test_project.py -v
```
