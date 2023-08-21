#import firestore_utils
import mongo_utils
from datetime import date


def get():
    """
    Retrieves transaction records based on user input.

    Args:
        None

    Returns:
        None

    Description:
        This function interacts with the user to retrieve transaction records from the database.
        Users can choose to search by name or retrieve a specific number of recent transactions.
        Retrieved transaction records are displayed in the console.

    Example:
        get()
    """

    searchByName = str(
        input("Do you want to search by name? (Format: y/n) ")).lower()
    items = []
    if searchByName == "y":
        name = str(
            input("Enter the full name as it appears on the transaction: ")).lower()
        # items = firestore_utils.get_items_by_name(name)                       # CFS Command
        items = mongo_utils.get_items_by_name(name)                             # MongoDB Command
    else:
        transaction_number = int(
            input("Enter the number of transactions you want to retrieve: "))
        # items = firestore_utils.get_last_x_items(transaction_number)          # CFS Command
        items = mongo_utils.get_last_x_items(transaction_number)                # MongoDB Command
    for item in items:
        #print(f"{item.id} => {item.to_dict()}")                                # CFS Command
        print(f"{item}")                                                        # MongoDB Command


def add():
    """
    Adds a new transaction record to the database based on user input.

    Args:
        None

    Returns:
        None

    Description:
        This function interacts with the user to receive input for required fields.
        If inputs are valid, the month, day and year fields are combined
        into a date_processed field. Then the fuction checks if transaction is a duplicate, 
        and then proceeds to add transaction based on user responses.

    Example:
        add()
    """

    item = {
        "name": input("Enter name: ").lower(),
        "invoice": input("Enter invoice number: ").lower(),
        "receipt": input("Enter receipt number: ").lower(),
        "amount": input("Enter amount paid (Format: DD.CC): "),
        "month": input("Enter the month the zelle processed: "),
        "day": input("Enter the day the zelle processed: "),
        "year": input("Enter the year the zelle processed: ")
    }
    if is_valid(item):
        new_item = {key: value for key, value in item.items() if key not in [
            "day", "month", "year"]}
        new_item["date_processed"] = date(int(item["year"]), int(
            item["month"]), int(item["day"])).isoformat()                       
        # item_in_db = firestore_utils.does_exist(new_item)                     # CFS Command
        item_in_db = mongo_utils.does_exist(new_item)                           # MongoDB Command
        if item_in_db:
            addToDb = str(input(
                "Transaction already exists. Do you still want to add to database? (y/n): ")).lower()
            if addToDb == "y":
                # firestore_utils.insert_item(new_item)                             # CFS Command
                mongo_utils.insert_item(new_item)                                   # MongoDB Command
                print("Adding duplicate now...")
            else:
                print("Not adding duplicate to database")
        else:
            # firestore_utils.insert_item(new_item)                                 # CFS Command
            mongo_utils.insert_item(new_item)                                       # MongoDB Command
            print("No existing transaction found. Adding now...")
    else:
        print("Invalid input information")


def update():
    """
    Updates a transaction record in the database based on user input.

    Args:
        None

    Returns:
        None

    Description:
        This function interacts with the user to update an existing transaction record in the database.
        Users need to provide the ID of the transaction they want to update, and then they can input
        new values for the transaction fields. If the inputs are valid and the transaction exists,
        the updated data is then saved to the database.

    Example:
        update()
    """

    id = input("Enter the id of the transaction you want to update: ")
    item = {
        "name": input("Enter name: "),
        "invoice": input("Enter invoice number: "),
        "receipt": input("Enter receipt number: "),
        "amount": input("Enter amount paid (Format: DD.CC): "),
        "month": input("Enter the month the zelle processed: "),
        "day": input("Enter the day the zelle processed: "),
        "year": input("Enter the year the zelle processed: ")
    }
    if is_valid(item):
        #if firestore_utils.get_items_by_id(id):                                     # CFS Command
        if mongo_utils.get_items_by_id(id):                                         # MongoDB Command
            new_item = {key: value for key, value in item.items() if key not in [
                "day", "month", "year"]}
            new_item["date_processed"] = date(int(item["year"]), int(
                item["month"]), int(item["day"])).isoformat()
            print("Updated successfully")
            #firestore_utils.update_item(id, new_item)                                  # CFS Command
            mongo_utils.update_item(id, new_item)                                       # MongoDB Command
        else:
            print("Invalid id")
    else:
        print("Invalid input information")


def delete():
    """
    Deletes a transaction record from the database based on user input.

    Args:
        None

    Returns:
        None

    Description:
        This function interacts with the user to delete an existing transaction record from the database.
        Users need to provide the ID of the transaction they want to delete. The specified transaction
        record is then permanently removed from the database.

    Example:
        delete()
    """

    id = str(input("Enter the id of the transaction you want to delete: "))
    #firestore_utils.delete_item(id)                                                # CFS Command 
    mongo_utils.delete_item(id)                                                     # MongoDB Command

def is_valid(item):
    """
    Validates the input data for a transaction item.

    Args:
        item (dict): Dictionary containing transaction data.

    Returns:
        bool: True if the item data is valid, False otherwise.

    Description:
        This function checks whether the input data for a transaction item is valid.
        It verifies that required fields are strings and not empty, and that date-related 
        fields are valid integers and valid dates.

    Example:
        if is_valid(item_data):
            # Perform further actions
    """

    if not all(isinstance(item[field], str) and item[field] for field in ["name", "invoice", "receipt", "amount", "year", "day", "month"]):
        return False
    if not (item["day"].isdigit() and item["month"].isdigit() and item["year"].isdigit()):
        return False
    try:
        date(int(item["year"]), int(item["month"]), int(item["day"]))
        return True
    except (ValueError, TypeError):
        return False
