import json
import logging
from datetime import datetime

# Global variable
stock_data = {}


# A global dictionary to store stock data
stock_data = {}

def addItem(item, qty, logs=None):
    """
    Adds a specified quantity of an item to the inventory.
    Fixes:
    1. Mutable default argument 'logs=[]' changed to 'logs=None'.
    2. Added input validation to ensure 'qty' is an integer.
    """
    # [cite_start]Fix for mutable default argument 
    if logs is None:
        logs = []

    # [cite_start]Fix for input validation [cite: 77]
    if not isinstance(qty, int):
        print(f"Error: Quantity '{qty}' is not a valid number. Item '{item}' not added.")
        return  # Stop the function if qty is not an integer

    # Original logic, now safe to run
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"Added {qty} of {item}")
    print(f"Added {qty} of {item}.")

    # This code below will now only run if qty is a valid integer
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"Added {qty} of {item}")
    print(f"Added {qty} of {item}.")

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except:
        pass

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
    f = open(file, "r")
    global stock_data
    stock_data = json.loads(f.read())
    f.close()

def saveData(file="inventory.json"):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    eval("print('eval used')")  # dangerous

main()


