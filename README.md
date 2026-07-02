# Inventory & POS System
#### Video Demo: `https://youtu.be/3NDfyQ6Kmkw`
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
test_project.py   ← pytest test suite (11 tests across 3 functions)
requirements.txt  ← pytest
data.csv          ← auto-created on first run
README.md
```

### File breakdown

**`project.py`** (~190 lines)
The entire application lives here. Organised into four layers:

- **Constants** (`DATA_FILE`, `FIELDNAMES`) — one place to change the filename or column layout
- **CSV helpers** (`ensure_csv`, `load_inventory`, `save_inventory`) — all file I/O is isolated here; nothing else touches the disk directly
- **Core logic** (`calculate_total`, `find_product`, `process_sale`) — pure or near-pure functions with no `input()` calls, making them straightforward to unit-test
- **Modes** (`buy_mode`, `sell_mode`, `print_report`) — thin interactive shells that call the core logic and handle user I/O

**`test_project.py`** (~70 lines)
Covers the three testable functions required by CS50P:

| Function | Tests | What is checked |
|---|---|---|
| `calculate_total` | 4 | empty list, floats, strings from CSV, single item |
| `find_product` | 3 | match, no match, second item in list |
| `process_sale` | 4 | success, stock reduction, insufficient stock, unknown ID |

Each `process_sale` test runs against a temporary CSV created by a `pytest` fixture so the real `data.csv` is never touched.

**`requirements.txt`** (1 line)
Only external dependency is `pytest`. The main program uses only the Python standard library (`csv`, `sys`, `os`).

**`data.csv`** (grows with use)
Auto-created on first run by `ensure_csv()`. Columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Unique product identifier (e.g. `SKU-001`) |
| `kind` | string | Product name or description |
| `cost` | float | Purchase / cost price |
| `shp` | float | Shipping cost paid when buying |
| `price` | float | Selling price to customer |
| `q` | int | Current stock quantity |

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
