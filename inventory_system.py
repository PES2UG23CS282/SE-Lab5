"""
Inventory Management System
----------------------------
This module provides functions to manage a simple in-memory stock database.
It supports adding, removing, saving, loading, and checking low stock items.
"""

import json
import logging
from datetime import datetime
from ast import literal_eval  # Safe alternative to eval()

# Constants for default values (Pylint likes constants)
DEFAULT_FILE_PATH = "inventory.json"
DEFAULT_THRESHOLD = 5

def add_item(item, qty, stock_data):
    """
    Add an item to the stock with the given quantity.

    Args:
        item (str): Item name
        qty (int): Quantity to add
        stock_data (dict): The dictionary holding stock information
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid data types for item or qty. Item not added.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    
    log_time = datetime.now()
    logging.info(f"{log_time}: Added {qty} of {item}") # Use f-string


def remove_item(item, qty, stock_data):
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

    # Fix for 'bare-except'
    try:
        if item not in stock_data:
            # Raise a specific error
            raise KeyError(f"Item '{item}' not in stock.")
            
        stock_data[item] -= qty
        
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(f"Removed all of {item}. Item deleted.")
        else:
            logging.info(f"Removed {qty} of {item}. New total: {stock_data[item]}")

    except KeyError as err:
        logging.error(f"Attempted to remove an item that doesn't exist: {err}")
    except TypeError as err:
        logging.error(f"Type error during remove_item: {err}")


def get_qty(item, stock_data):
    """
    Get the quantity of a specific item.

    Args:
        item (str): Item name
        stock_data (dict): The dictionary holding stock information

    Returns:
        int: Quantity of the item
    """
    return stock_data.get(item, 0)


def load_data(file_path=DEFAULT_FILE_PATH):
    """
    Load stock data from a JSON file.

    Args:
        file_path (str): Path to the JSON file

    Returns:
        dict: Loaded stock data
    """
    # Fix for 'consider-using-with' and 'unspecified-encoding'
    try:
        with open(file_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)
            logging.info(f"Data loaded from {file_path}")
            return data
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}. Returning empty stock.")
        return {}
    except json.JSONDecodeError as err:
        logging.error(f"Error decoding JSON from {file_path}: {err}")
        return {}


def save_data(stock_data, file_path=DEFAULT_FILE_PATH):
    """
    Save stock data to a JSON file.

    Args:
        stock_data (dict): The dictionary holding stock information
        file_path (str): Path to the JSON file
    """
    # Fix for 'consider-using-with' and 'unspecified-encoding'
    try:
        with open(file_path, "w", encoding="utf-8") as outfile:
            json.dump(stock_data, outfile, indent=4)
            logging.info(f"Data saved to {file_path}")
    except OSError as err:
        logging.error(f"Error writing to file {file_path}: {err}")


def print_data(stock_data):
    """
    Print the inventory report.
    (Disabling Pylint's print warning as this is the function's purpose)
    """
    # pylint: disable=print-statement
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------")


def check_low_items(stock_data, threshold=DEFAULT_THRESHOLD):
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
    """Main function to run the inventory operations."""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    stock_data = load_data()  # Load existing data first
    if not stock_data:
        logging.info("No existing data found. Starting with empty inventory.")

    # --- Calls updated to snake_case ---
    add_item("apple", 10, stock_data=stock_data)
    add_item("banana", 2, stock_data=stock_data)
    add_item("orange", 5, stock_data=stock_data)
    
    # Test for the bug you fixed
    add_item("bread", "two", stock_data=stock_data) # Should log an error
    
    remove_item("apple", 3, stock_data=stock_data)
    remove_item("banana", 3, stock_data=stock_data) # Should remove the item

    print_data(stock_data)

    # pylint: disable=print-statement
    print(f"Apple stock: {get_qty('apple', stock_data)}")
    
    low_items = check_low_items(stock_data)
    print(f"Low items: {low_items}")
    logging.info(f"Low items: {low_models}")

    save_data(stock_data)

    # Fix for 'eval-used' (W0123) - Use literal_eval
    expression = "'Safe eval substitute working'"
    safe_output = literal_eval(expression)
    print(safe_output)


if __name__ == "__main__":
    main()
