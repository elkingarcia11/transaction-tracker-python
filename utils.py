import mongo_utils
from datetime import datetime, date

def get(collection):
    searchByName = str(input("Do you want to search by name? (Format: y/n) ")).lower()
    items = []
    if searchByName == "y":
        name = str(input("Enter the full name as it appears on the transaction: ")).lower()
        items = mongo_utils.get_items_by_name(collection,name)
    else:
        transaction_number = int(input("Enter the number of transactions you want to retrieve: "))
        items = mongo_utils.get_last_x_items(collection, transaction_number)
    for item in items:
        print(item)

def add(collection):
    name = str(input("Enter name: ")).lower()
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))
    searchItem = {"name": name, "amount": amount,
                  "dateProcessed": date(year, month, day).isoformat()}
    item_in_db = mongo_utils.does_exist(collection,searchItem)
    if item_in_db:
        addToDb = str(input("Transaction already exists. Do you still want to add to database? (y/n): ")).lower()
        if addToDb == "y":
            print("This transaction must be unique. Adding now...")
            item = {"name": name, "invoice": invoice, "receipt": receipt, "amount": amount,
                    "dateProcessed": date(year, month, day).isoformat()}
            mongo_utils.insert_item(collection, item)
        else:
            print("Not adding to database")
    else:
        print("No existing transaction found. Adding now...")
        mongo_utils.insert_item(collection, item)

def update(collection):
    id = str(input("Enter the id of the transaction you want to update: "))
    name = str(input("Enter name: "))
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))
    mongo_utils.update_item(collection, id, name, invoice, receipt, amount, month, day, year)
def delete(collection):
    id = str(input("Enter the id of the transaction you want to delete: "))
    mongo_utils.delete_item(collection,id)