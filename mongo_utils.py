import pymongo
import utils
from bson.objectid import ObjectId
from datetime import datetime, date


def connect(conf):
    """
    Establishes a connection to a MongoDB database using configuration settings.

    Args:
        conf (configparser.ConfigParser): The configuration object containing database settings.

    Returns:
        pymongo.MongoClient: A MongoDB connection object.

    Description:
        This function takes a configuration object containing the necessary settings,
        including the URI of the MongoDB database. It uses the "pymongo" library to
        establish a connection to the specified database.

    Example:
        conf = utils.read_config("config.ini")
        connection = connect(conf)
    """

    uri = conf["PROD"]["mongo_db_uri"]
    connection = pymongo.MongoClient(uri)
    return connection


def get_collection(connection, conf):
    """
    Retrieves a MongoDB collection based on a provided connection and configuration settings.

    Args:
        connection (pymongo.MongoClient): The MongoDB connection object.
        conf (configparser.ConfigParser): The configuration object containing database settings.

    Returns:
        pymongo.collection.Collection: The MongoDB collection object.

    Description:
        This function takes a MongoDB connection object and a configuration object containing
        the necessary settings to retrieve a specific collection from a MongoDB database.

    Example:
        connection = connect(conf)
        collection = get_collection(connection, conf)
    """

    database = connection[conf["PROD"]["mongo_db_name"]]
    collection = database[conf["PROD"]["mongo_db_collection"]]
    return collection


def delete_item(id):
    """
    Deletes an item from a MongoDB collection based on its unique ObjectId.

    Args:
        id (str): The ObjectId of the item to be deleted.

    Returns:
        None

    Description:
        This function takes an ObjectId as input and uses it to delete the corresponding item
        from a MongoDB collection.

    Example:
        delete_item("5f8a08f74cb5c576fa7c7f3a")
    """

    if not connection.is_locked:
        collection.delete_one({"_id": ObjectId(id)})
    else:
        print("Connection is locked or closed.")
        return None


def does_exist(item):
    """
    Checks if an item exists in a MongoDB collection.

    Args:
        item (dict): The query to search for the item in the collection.

    Returns:
        bool: True if the item exists, False otherwise.

    Description:
        This function queries a MongoDB collection to check if the provided item exists
        based on the given query. It returns True if the item is found, and False if it
        is not found.

    Example:
        item_to_check = {"name": "example"}
        exists = does_exist(item_to_check)
        if exists:
            print("Item exists in the collection.")
        else:
            print("Item does not exist in the collection.")
    """

    if not connection.is_locked:
        item = collection.find_one(item)
        if item is None:
            return False
        else:
            return True
    else:
        print("Connection is locked or closed.")
        return None


def get_items_by_name(name):
    """
    Retrieves items from a MongoDB collection based on a specific name.

    Args:
        name (str): The name to search for in the collection.

    Returns:
        pymongo.cursor.Cursor: A cursor containing the retrieved items.

    Description:
        This function queries a MongoDB collection to retrieve items that match a specific name.
        The items are sorted by their processed date in descending order.

    Example:
        items = get_items_by_name("example")
    """

    if not connection.is_locked:
        items = collection.find({"name": name}).sort("dateProcessed", -1)
        return items
    else:
        print("Connection is locked or closed.")
        return None


def get_last_x_items(number):
    """
    Retrieves the last x items from a MongoDB collection.

    Args:
        number (int): The number of items to retrieve.

    Returns:
        pymongo.cursor.Cursor: A cursor containing the retrieved items.

    Description:
        This function queries a MongoDB collection to retrieve the last x items based on
        their processed date in descending order.

    Example:
        last_items = get_last_x_items(10)
    """

    if not connection.is_locked:
        items = collection.find().sort("dateProcessed", -1).limit(number)
        return items
    else:
        print("Connection is locked or closed.")
        return None


def insert_item(item):
    """
    Inserts an item into a MongoDB collection.

    Args:
        item (dict): The item to insert.

    Returns:
        None

    Description:
        This function inserts a new item into a MongoDB collection.

    Example:
        new_item = {"name": "new_example"}
        insert_item(new_item)
    """

    if not connection.is_locked:
        collection.insert_one(item)
    else:
        print("Connection is locked or closed.")
        return None


def update_item(id, item):
    """
    Updates an item in a MongoDB collection based on its unique ObjectId.

    Args:
        id (str): The ObjectId of the item to be updated.
        name (str): The new name for the item.
        invoice (str): The new invoice number for the item.
        receipt (str): The new receipt number for the item.
        amount (float): The new amount for the item.
        month (int): The month component of the processing date.
        day (int): The day component of the processing date.
        year (int): The year component of the processing date.

    Returns:
        None

    Description:
        This function updates an existing item in a MongoDB collection based on its unique ObjectId.
        The item is updated with the provided details.

    Example:
        update_item("5f8a08f74cb5c576fa7c7f3a", "updated_example", "123", "456", 100.0, 8, 18, 2023)
    """

    if not connection.is_locked:
        collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set":
                {"name": item["name"].upper(), "invoice": item["invoice"], "receipt": item["receipt"], "amount": item["amount"],
                 "dateProcessed": item["dateProcessed"]}
             }
        )
    else:
        print("Connection is locked or closed.")
        return None


conf = utils.read_config(".ini")
connection = connect(conf)
collection = get_collection(connection, conf)
