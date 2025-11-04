"""
Inventory Management System
----------------------------
This module provides functions to manage a simple in-memory stock database.
It supports adding, removing, saving, loading, and checking low stock items.
"""

import json
import logging
from datetime import datetime
from ast import literal_eval

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global variable avoided – use a function parameter instead where possible
def add_item(item=None, qty=0, logs=None, stock_data=None):
    """
    Add an item to the stock with the given quantity.
    Args:
        item (str): Item name
        qty (int): Quantity to add
        logs (list): Optional list to store logs
        stock_data (dict): The dictionary holding stock information
    """
    if item is None or stock_data is None:
        logging.warning("Invalid input: item or stock_data is None")
        return

    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid data types for item or qty.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty, stock_data=None):
    """
    Remove the given quantity of an item from stock.
    Args:
        item (str): Item name
        qty (int): Quantity to remove
        stock_data (dict): The dictionary holding stock information
    """
    if stock_data is None:
        logging.warning("Stock data not provided.")
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info("Removed %d of %s", qty, item)
    except KeyError:
        logging.error("Attempted to remove an item that doesn't exist: %s", item)
    except TypeError as err:
        logging.error("Type error during remove_item: %s", err)


def get_qty(item, stock_data=None):
    """
    Get the quantity of a specific item.
    Args:
        item (str): Item name
        stock_data (dict): The dictionary holding stock information
    Returns:
        int: Quantity of the item
    """
    if stock_data is None:
        return 0
    return stock_data.get(item, 0)


def load_data(file_path="inventory.json"):
    """
    Load stock data from a JSON file.
    Args:
        file_path (str): Path to the JSON file
    Returns:
        dict: Loaded stock data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info("Data loaded from %s", file_path)
            return data
    except FileNotFoundError:
        logging.warning("File not found: %s", file_path)
        return {}
    except json.JSONDecodeError as err:
        logging.error("Error decoding JSON: %s", err)
        return {}


def save_data(stock_data, file_path="inventory.json"):
    """
    Save stock data to a JSON file.
    Args:
        stock_data (dict): The dictionary holding stock information
        file_path (str): Path to the JSON file
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
            logging.info("Data saved to %s", file_path)
    except OSError as err:
        logging.error("Error writing to file: %s", err)


def print_data(stock_data):
    """
    Print the inventory report.
    Args:
        stock_data (dict): The dictionary holding stock information
    """
    print("\nItems Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(stock_data, threshold=5):
    """
    Check which items are below the threshold quantity.
    Args:
        stock_data (dict): The dictionary holding stock information
        threshold (int): Minimum stock threshold
    Returns:
        list: Items below the threshold
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to test the inventory operations."""
    stock_data = {}

    add_item("apple", 10, stock_data=stock_data)
    add_item("banana", -2, stock_data=stock_data)
    add_item("orange", 5, stock_data=stock_data)

    remove_item("apple", 3, stock_data=stock_data)
    remove_item("orange", 1, stock_data=stock_data)

    print(f"Apple stock: {get_qty('apple', stock_data)}")
    print(f"Low items: {check_low_items(stock_data)}")

    save_data(stock_data)
    stock_data = load_data()

    print_data(stock_data)

    # Instead of eval() - safe literal evaluation demonstration
    expression = "'Safe eval substitute working'"
    safe_output = literal_eval(expression)
    print(safe_output)


if __name__ == "__main__":
    main()
