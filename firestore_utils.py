import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

def initialize_database(collection_name):
    """
    Initializes and returns a Firestore collection for database operations.

    Args:
        collection_name (str): The name of the collection to interact with.

    Returns:
        google.cloud.firestore.CollectionReference: A reference to the initialized Firestore collection.

    Description:
        This function initializes the Firebase Admin SDK using the Cloud Firestore service account 
        credentials, establishes a connection to the Firestore database, and returns a reference 
        to the specified collection. 

    Example:
        collection = initialize_database("transactions")
    """

    cred = credentials.Certificate("keys/credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection(collection_name)
    return collection

def get_items_by_name(name):
    """
    Retrieves transaction items matching the provided name.

    Args:
        name (str): The name to search for in transaction items.

    Returns:
        google.cloud.firestore.QuerySnapshot: A snapshot containing transaction items that match the provided name.
    
    Description:
        This function queries the database collection to retrieve transaction items that match the provided name if name is a valid string.

    Example:
        items = get_items_by_name("John Doe")
    """

    if type(name) == str:
        docs = (collection.where(filter=FieldFilter("name", "==", name)).stream())
        return docs

def get_last_x_items(number):
    """
    Retrieves the last "x" transaction items based on timestamp.

    Args:
        number (int): The number of transaction items to retrieve.

    Returns:
        google.cloud.firestore.QuerySnapshot: A snapshot containing the last "x" transaction items.

    Description:
        This function queries the database collection to retrieve the specified number of most recent 
        transaction items added to the database.

    Example:
        items = get_last_x_items(10)
    """

    docs = (collection.order_by("date_added", direction=firestore.Query.DESCENDING).limit(number).stream())
    return docs

def does_exist(item):
    """
    Checks if a transaction item already exists in the database.

    Args:
        item (dict): The transaction item data to check for existence.

    Returns:
        bool: True if the transaction item exists, False otherwise.

    Description:
        This function checks whether a transaction item with the same name, amount, and date_processed already exists.

    Example:
        if does_exist(new_item):
            # Handle existing item case
    """

    query = collection.where(filter=FieldFilter("name", "==", item["name"])).where(
    filter=FieldFilter("amount", "==", item["amount"])).where(
    filter=FieldFilter("date_processed", "==", item["date_processed"]))
    docs = query.stream()
    for doc in docs:
        return True
    return False

def get_items_by_id(id):
    """
    Retrieves a transaction item by its unique identifier (ID).

    Args:
        id (str): The ID of the transaction item to retrieve.

    Returns:
        google.cloud.firestore.DocumentSnapshot or None: A snapshot of the transaction item or None if not found.

    Description:
        This function retrieves a transaction item from the database based on its unique ID.

    Example:
        item = get_items_by_id("123456789")
        if item:
            print(item.to_dict())
    """

    if type(id) == str:
        doc = collection.document(id).get()
        if doc.exists:
            return doc
        else:
            return None
    
def insert_item(item):
    """
    Inserts a new transaction item into the database.

    Args:
        item (dict): The data of the transaction item to insert.

    Returns:
        None

    Description:
        This function inserts a new transaction item into the database collection 
        with an autogenerated ID and a timestamp of its added date.

    Example:
        new_item = {...}  # Dictionary containing item data
        insert_item(new_item)
    """

    item["date_added"] = firestore.SERVER_TIMESTAMP
    collection.document().set(item)

def update_item(id, item):
    """
    Updates a transaction item in the database.

    Args:
        id (str): The ID of the transaction item to update.
        item (dict): The updated data of the transaction item.

    Returns:
        None

    Description:
        This function updates an existing transaction item in the database collection 
        based on its ID and updates timestamp of its added date to current time

    Example:
        item_id = "123456789"
        updated_item = {...}  # Dictionary containing updated item data
        update_item(item_id, updated_item)
    """

    item["date_added"] = firestore.SERVER_TIMESTAMP
    collection.document(id).set(item)

def delete_item(id):
    """
    Deletes a transaction item from the database.

    Args:
        id (str): The ID of the transaction item to delete.

    Returns:
        None
        
    Description:
        This function deletes a transaction item from the database collection based on its ID.

    Example:
        item_id = "123456789"
        delete_item(item_id)
    """

    collection.document(id).delete()

collection = initialize_database("clients")
