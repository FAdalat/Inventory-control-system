import csv
import os
import pytest

from project import calculate_total, find_product, process_sale, DATA_FILE, save_inventory, ensure_csv


def test_calculate_total_basic():
    assert calculate_total([10.0, 20.0, 5.50]) == 35.5


def test_calculate_total_empty():
    assert calculate_total([]) == 0


def test_calculate_total_strings():
    """Prices stored in CSV come back as strings — must still work."""
    assert calculate_total(["9.99", "4.01"]) == 14.0


def test_calculate_total_single_item():
    assert calculate_total([49.95]) == 49.95


SAMPLE_ROWS = [
    {"id": "001", "kind": "T-Shirt", "cost": "5.0", "shp": "1.0", "price": "15.0", "q": "10"},
    {"id": "002", "kind": "Jeans",   "cost": "20.0","shp": "2.0", "price": "60.0", "q": "5"},
]


def test_find_product_exists():
    result = find_product(SAMPLE_ROWS, "001")
    assert result is not None
    assert result["kind"] == "T-Shirt"


def test_find_product_not_found():
    assert find_product(SAMPLE_ROWS, "999") is None


def test_find_product_second_item():
    result = find_product(SAMPLE_ROWS, "002")
    assert result["kind"] == "Jeans"


@pytest.fixture(autouse=True)
def temp_csv(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp directory for each test."""
    import project as proj
    fake_path = str(tmp_path / "data.csv")
    monkeypatch.setattr(proj, "DATA_FILE", fake_path)

    # Pre-populate with known inventory
    with open(fake_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=proj.FIELDNAMES)
        writer.writeheader()
        writer.writerows([
            {"id": "A1", "kind": "Dress", "cost": "30", "shp": "3", "price": "90", "q": "3"},
            {"id": "A2", "kind": "Scarf", "cost": "5",  "shp": "1", "price": "20", "q": "1"},
        ])
    yield fake_path


def test_process_sale_success():
    success, price = process_sale("A1", 2)
    assert success is True
    assert price == 90.0


def test_process_sale_reduces_stock():
    import project as proj
    process_sale("A1", 1)
    rows = proj.load_inventory()
    dress = find_product(rows, "A1")
    assert int(dress["q"]) == 2   # started at 3, sold 1


def test_process_sale_insufficient_stock():
    success, price = process_sale("A2", 5)  # only 1 in stock
    assert success is False
    assert price is None


def test_process_sale_unknown_product():
    success, price = process_sale("Z9", 1)
    assert success is False
    assert price is None

