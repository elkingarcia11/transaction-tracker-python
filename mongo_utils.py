import pymongo
from bson.objectid import ObjectId
from datetime import datetime, date


def connect(conf):
    """
    Establishes a connection to a MongoDB database using the provided configuration.

    Args:
        conf (configparser.ConfigParser): The configuration object containing database settings.

    Returns:
        pymongo.MongoClient: A MongoDB connection object.

    Description:
        This function takes a configuration object containing the necessary settings,
        including the URI of the MongoDB database. It uses the 'pymongo' library to
        establish a connection to the specified database and returns the connection object.

    Example:
        conf = read_config('config.ini')
        connection = connect(conf)
        db = connection[conf['PROD']['db_name']]
    """

    uri = conf['PROD']['db_uri']
    connection = pymongo.MongoClient(uri)
    return connection


def delete_item(collection, id):
    collection.delete_one({"_id": ObjectId(id)})


def does_exist(collection, item):
    item = collection.find_one(item)
    if item is None:
        return False
    else:
        return True


def get_database(connection, database_name):
    return connection[database_name]


def get_collection(database_name, collection):
    return database_name[collection]


def get_items_by_name(collection, name):
    items = collection.find({"name": name}).sort("_id", -1)
    return items


def get_last_x_items(collection, number):
    items = collection.find().sort("_id", -1).limit(number)
    return items


def insert_item(collection, item):
    collection.insert_one(item)

def update_item(collection, id, name, invoice, receipt, amount, month, day, year):
    collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set":
            {"name": name.upper(), "invoice": invoice, "receipt": receipt, "amount": amount,
             "dateProcessed": date(year, month, day).isoformat(), "date": datetime.today()}
         }
    )
