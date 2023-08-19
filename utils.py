from datetime import date
import configparser
import firestore_utils
# import mongo_utils


def get():
    searchByName = str(input("Do you want to search by name? (Format: y/n) ")).lower()
    items = []
    if searchByName == "y":
        name = str(input("Enter the full name as it appears on the transaction: ")).lower()
        # items = mongo_utils.get_items_by_name(name)
        items = firestore_utils.get_items_by_name(name)
    else:
        transaction_number = int(input("Enter the number of transactions you want to retrieve: "))
        # items = mongo_utils.get_last_x_items(transaction_number)
        items = firestore_utils.get_last_x_items(transaction_number)
    for item in items:
        print(f"{item.id} => {item.to_dict()}")


def add():
    item= {
        'name' : input("Enter name: "),
        'invoice' : input("Enter invoice number: "),
        'receipt' : input("Enter receipt number: "),
        'amount' : input("Enter amount paid (Format: DD.CC): "),
        'month' : input("Enter the month the zelle processed: "),
        'day' : input("Enter the day the zelle processed: "),
        'year' : input("Enter the year the zelle processed: ")
    }
    if is_valid(item):
        new_item = {key: value for key, value in item.items() if key not in ['day', 'month', 'year']}
        new_item['dateProcessed'] = date(int(item['year']), int(item['month']), int(item['day'])).isoformat()
        # item_in_db = mongo_utils.does_exist(searchItem)
        item_in_db = firestore_utils.does_exist(new_item)
        if item_in_db:
            addToDb = str(input("Transaction already exists. Do you still want to add to database? (y/n): ")).lower()
            if addToDb == "y":
                firestore_utils.insert_item(item)
                # mongo_utils.insert_item(item)
                print("Adding duplicate now...")
            else:
                print("Not adding duplicate to database")
        else:
            firestore_utils.insert_item(item)
            # mongo_utils.insert_item(item)
            print("No existing transaction found. Adding now...")
    else:
        print("Invalid input information")


def update():
    id = input("Enter the id of the transaction you want to update: ")
    item= {
        'name' : input("Enter name: "),
        'invoice' : input("Enter invoice number: "),
        'receipt' : input("Enter receipt number: "),
        'amount' : input("Enter amount paid (Format: DD.CC): "),
        'month' : input("Enter the month the zelle processed: "),
        'day' : input("Enter the day the zelle processed: "),
        'year' : input("Enter the year the zelle processed: ")
    }
    if is_valid(item):
        newItem = {key: value for key, value in item.items() if key not in ['day', 'month', 'year']}
        newItem['dateProcessed'] = date(int(item['year']), int(item['month']), int(item['day'])).isoformat()
        print("Updated successfully")
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
    if not all(isinstance(item[field], str) and item[field] for field in ["name", "invoice", "receipt", "amount","year","day","month"]):
        print("Not a valid string inputs")
        return False
    if not (item['day'].isdigit() and item['month'].isdigit() and item['year'].isdigit()):
        print("Not valid number inputs")
        return False
    try:
        date(int(item["year"]), int(item["month"]), int(item["day"]))
        return True
    except (ValueError, TypeError):
        print("date invalid")
        return False
