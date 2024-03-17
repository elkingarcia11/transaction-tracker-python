import pymongo
import configparser
from bson.objectid import ObjectId
from datetime import datetime


class MongoDBManager:
    def __init__(self, conf_file=".ini"):
        self.conf = self.read_config(conf_file)
        self.connection = self.connect()
        self.collection = self.get_collection()

    def connect(self):
        """
        Establishes a connection to a MongoDB database using configuration settings.

        Returns:
            pymongo.MongoClient: A MongoDB connection object.

        Description:
            This function takes a configuration object containing the necessary settings,
            including the URI of the MongoDB database. It uses the "pymongo" library to
            establish a connection to the specified database.
        """
        uri = self.conf["PROD"]["mongo_db_uri"]
        connection = pymongo.MongoClient(uri)
        return connection

    def get_collection(self):
        """
        Retrieves a MongoDB collection based on the connection and configuration settings.

        Returns:
            pymongo.collection.Collection: The MongoDB collection object.

        Description:
            This function takes a MongoDB connection object and a configuration object containing
            the necessary settings to retrieve a specific collection from a MongoDB database.
        """
        database = self.connection[self.conf["PROD"]["mongo_db_name"]]
        collection = database[self.conf["PROD"]["mongo_db_collection"]]
        return collection

    def delete_item(self, item_id):
        """
        Deletes an item from a MongoDB collection based on its unique ObjectId.

        Args:
            item_id (str): The ObjectId of the item to be deleted.

        Returns:
            None

        Description:
            This function takes an ObjectId as input and uses it to delete the corresponding item
            from a MongoDB collection.
        """
        self.collection.delete_one({"_id": ObjectId(item_id)})

    def does_exist(self, item):
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
        """
        result = self.collection.find_one(item)
        return result is not None

    def get_items_by_name(self, name):
        """
        Retrieves items from a MongoDB collection based on a specific name.

        Args:
            name (str): The name to search for in the collection.

        Returns:
            pymongo.cursor.Cursor: A cursor containing the retrieved items.

        Description:
            This function queries a MongoDB collection to retrieve items that match a specific name.
            The items are sorted by their processed date in descending order.
        """
        items = self.collection.find({"name": name}).sort("date_processed", -1)
        return items

    def get_last_x_items(self, number):
        """
        Retrieves the last x items from a MongoDB collection.

        Args:
            number (int): The number of items to retrieve.

        Returns:
            pymongo.cursor.Cursor: A cursor containing the retrieved items.

        Description:
            This function queries a MongoDB collection to retrieve the last x items based on
            their processed date in descending order.
        """
        items = self.collection.find().sort("date_processed", -1).limit(number)
        return items

    def get_item_by_id(self, item_id):
        """
        Retrieves an item from a MongoDB collection based on its unique ObjectId.

        Args:
            item_id (str): The ObjectId of the item to retrieve.

        Returns:
            dict or None: The retrieved item as a dictionary, or None if not found.

        Description:
            This function retrieves an item from a MongoDB collection based on its unique ObjectId.
        """
        return self.collection.find_one({"_id": ObjectId(item_id)})

    def insert_item(self, item):
        """
        Inserts an item into a MongoDB collection.

        Args:
            item (dict): The item to insert.

        Returns:
            None

        Description:
            This function inserts a new item into a MongoDB collection.
        """
        item["date_added"] = datetime.now()
        self.collection.insert_one(item)

    def update_item(self, item_id, item):
        """
        Updates an item in a MongoDB collection based on its unique ObjectId.

        Args:
            item_id (str): The ObjectId of the item to be updated.
            item (dict): The new data for the item.

        Returns:
            None

        Description:
            This function updates an existing item in a MongoDB collection based on its unique ObjectId.
        """
        self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set":
                {"name": item["name"].lower(), "invoice": item["invoice"], "receipt": item["receipt"],
                 "amount": item["amount"], "date_processed": item["date_processed"], "date_added": datetime.now()}
             }
        )

    @staticmethod
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
        """
        config = configparser.ConfigParser()
        config.read(file_name)
        return config
