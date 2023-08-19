# import mongo_utils
from datetime import date, datetime
import configparser
import firestore_utils


def get():
    searchByName = str(
        input("Do you want to search by name? (Format: y/n) ")).lower()
    items = []
    if searchByName == "y":
        name = str(
            input("Enter the full name as it appears on the transaction: ")).lower()
        # items = mongo_utils.get_items_by_name(name)
        items = firestore_utils.get_items_by_name(name)
    else:
        transaction_number = int(
            input("Enter the number of transactions you want to retrieve: "))
        # items = mongo_utils.get_last_x_items(transaction_number)
        items = firestore_utils.get_last_x_items(transaction_number)
    for item in items:
        print(f"{item.id} => {item.to_dict()}")


def add():
    name = str(input("Enter name: ")).lower()
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))
    item = {"name": name, "invoice": invoice, "receipt": receipt,
            "amount": amount, "month": month, "day": day, "year": year}
    if is_valid(item):
        searchItem = {"name": name, "amount": amount,
                      "dateProcessed": date(year, month, day).isoformat()}
        # item_in_db = mongo_utils.does_exist(searchItem)
        item_in_db = firestore_utils.does_exist(searchItem)
        if item_in_db:
            addToDb = str(input(
                "Transaction already exists. Do you still want to add to database? (y/n): ")).lower()
            if addToDb == "y":
                print("This transaction must be unique. Adding now...")
                item = {"name": name, "invoice": invoice, "receipt": receipt, "amount": amount,
                        "dateProcessed": date(year, month, day).isoformat()}

                firestore_utils.insert_item(item)
                # mongo_utils.insert_item(item)
            else:
                print("Not adding to database")
        else:
            item = {"name": name, "invoice": invoice, "receipt": receipt,
                    "amount": amount, "dateProcessed": date(year, month, day).isoformat()}
            print("No existing transaction found. Adding now...")
            firestore_utils.insert_item(item)
            # mongo_utils.insert_item(item)
    else:
        print("Invalid input information")


def update():
    id = str(input("Enter the id of the transaction you want to update: "))
    name = str(input("Enter name: ")).lower()
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))

    item = {"name": name, "invoice": invoice, "receipt": receipt,
            "amount": amount, "month": month, "day": day, "year": year}
    if is_valid(item):
        item = {"name": name.lower(), "invoice": invoice, "receipt": receipt,
                "amount": amount, "dateProcessed": date(year, month, day).isoformat()}
        firestore_utils.update_item(id, item)
        # mongo_utils.update_item(id, item)
    else:
        print("Invalid input information")


def delete():
    id = str(input("Enter the id of the transaction you want to delete: "))
    # mongo_utils.delete_item(id)
    firestore_utils.delete_item(id)


def read_config(file_name):
    """
    Reads configuration settings from an .ini file and returns a ConfigParser object.

    Args:
        file_name (str): The name of the .ini file to read.

    Returns:
        configparser.ConfigParser: A ConfigParser object containing the parsed configuration settings.

    Description:
        This function reads configuration settings from a specified .ini file using the
        configparser module. It creates a ConfigParser object, reads the settings from the
        file, and returns the ConfigParser object for further use.

    Example:
        config = read_config("config.ini")
        value = config.get("section", "key")
    """

    config = configparser.ConfigParser()
    config.read(file_name)
    return config


def is_valid(item):
    # Validate non-empty strings
    if not all(isinstance(item[field], str) and item[field] for field in ["name", "invoice", "receipt"]):
        return False

    # Validate amount is a string containing only numbers
    if not (isinstance(item["amount"], str) and item["amount"].isdigit()):
        return False

    # Validate date is valid
    try:
        date(item["year"], item["month"], item["day"])
        return True
    except ValueError:
        return False
