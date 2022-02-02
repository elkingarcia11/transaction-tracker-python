from decimal import *
import pymongo
from datetime import datetime, date

from bson import ObjectId

def connect():
    # Replace the uri string with your MongoDB deployment's connection string.
    conn_str = "mongodb://localhost:27017"
    connection = pymongo.MongoClient(conn_str)
    return connection

def get_database(connection, database_name):
    # Create the database for our example (we will use the same database throughout the tutorial
    return connection[database_name]

def get_collection(database_name, collection_name):
    return database_name[collection_name]

def insert_item(collection_name, item):
    collection_name.insert_one(item)
    print("Successfully added")
    print(item)
    return

def get_last_x_items(collection_name, number_of_transactions):
    items = collection_name.find().sort("_id", -1).limit(number_of_transactions)
    for item in items:
        print(item)

def get_item(collection_name, item):
    item = collection_name.find_one(item)
    if item is None:
        return False
    else:
        return True

def addTransaction(collection_name):
    name = str(input("Enter name: ")).lower()
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))

    searchItem = {"name" : name, "amount" : amount, "dateProcessed" : date(year, month, day).isoformat()}
    item = {"name" : name, "invoice" : invoice, "receipt" : receipt, "amount" : amount, "dateProcessed" : date(year, month, day).isoformat(), "date" : datetime.today()}

    existsInDb = get_item(collection_name, searchItem)

    if existsInDb:
        addToDb = str(input("Transaction already exists. Do you still want to add to database? (y/n): ")).lower()
        if addToDb == "y":
            print("This transaction must be unique. Adding now...")
            insert_item(collection_name, item)
        else: 
            print("Not adding to database");
    else:
        print("No existing transaction found. Adding now...")
        insert_item(collection_name, item)
    return 

def getTransaction(collection_name):
    latestTransaction = str(input("Do you want to retrieve the latest transactions? (y/n): ")).lower()
    
    if latestTransaction == "y":
        transaction_number = int(input("How many transactions do you want to retrieve? "))
        get_last_x_items(collection_name, transaction_number)
    else: 
        #totalFields = int(input("How many fields do you want to search with? "))
        return

def deleteTransaction(collection_name):
    id = str(input("Enter the id of the transaction you want to delete: "))
    collection_name.delete_one({"_id":ObjectId(id)});
    print("Transaction Removed!")

def updateTransaction(collection_name):
    id = str(input("Enter the id of the transaction you want to update: "))
    name = str(input("Enter name: ")).lower()
    invoice = int(input("Enter invoice number: "))
    receipt = int(input("Enter receipt number: "))
    amount = float(input("Enter amount paid (Format: DD.CC): "))
    month = int(input("Enter the month the zelle processed: "))
    day = int(input("Enter the day the zelle processed: "))
    year = int(input("Enter the year the zelle processed: "))
    collection_name.find_one_and_update(
        {"_id":ObjectId(id)},
        {"$set":
            {"name" : name, "invoice" : invoice, "receipt" : receipt, "amount" : amount, "dateProcessed" : date(year, month, day).isoformat(), "date" : datetime.today()}
        }
    )

def main():
    connection = connect()
    db = get_database(connection, 'transactions') 
    collection = get_collection(db, 'clients')

    while True:
        command = str(input("What do you want to do (G, A, U, D): ")).lower()
        if command == "g":
            getTransaction(collection)
            """
            input how many fields do you want to match, -1 if want to return last x numbers,
            input [which field
            input [with what value] 
            repeat for amount of fields
            return list of transactions
            """
        elif command == "a":
            addTransaction(collection)
        elif command == "u":
            updateTransaction(collection)
        elif command == "d":
            deleteTransaction(collection) 

main()