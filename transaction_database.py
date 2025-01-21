import firebase_admin
from firebase_admin import credentials, firestore


class TransactionDatabase:
    """
    A class for interacting with a Firestore database containing transactional data.

    Attributes:
        collection (firestore.CollectionReference): Reference to the Firestore collection.
    """

    def __init__(self, collection_name):
        """
        Initialize the TransactionDatabase object.

        Args:
            collection_name (str): The name of the Firestore collection to interact with.
        """
        self.collection = self.initialize_database(collection_name)

    def initialize_database(self, collection_name):
        """
        Initialize the Firestore database and return a reference to the specified collection.

        Args:
            collection_name (str): The name of the Firestore collection.

        Returns:
            firestore.CollectionReference: Reference to the specified Firestore collection.
        """
        cred = credentials.Certificate("keys/credentials.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db.collection(collection_name)

    def get_items_by_name(self, name):
        """
        Retrieve documents from the collection that match the given name.

        Args:
            name (str): The name to search for in the 'name' field of the documents.

        Returns:
            firestore.QuerySnapshot: A snapshot containing the documents matching the name criteria.
        """
        if isinstance(name, str):
            docs = self.collection.where("name", "==",name).stream()
            return docs

    def get_last_x_items(self, number):
        """
        Retrieve the last 'number' of items added to the collection.

        Args:
            number (int): The number of items to retrieve.

        Returns:
            firestore.QuerySnapshot: A snapshot containing the last 'number' of documents added to the collection.
        """
        docs = self.collection.order_by(
            "date_added", direction=firestore.Query.DESCENDING).limit(number).stream()
        return docs

    def does_exist(self, item):
        """
        Check if an item with the same name, amount, and date processed already exists in the collection.

        Args:
            item (dict): Dictionary containing the attributes of the item to check.

        Returns:
            bool: True if an item with the same attributes exists, False otherwise.
        """
        query = self.collection.where("name", "==", item["name"]).where("amount", "==", item["amount"]).where("date_processed", "==", item["date_processed"])
        docs = query.stream()
        return any(docs)

    def get_items_by_id(self, item_id):
        """
        Retrieve an item from the collection by its ID.

        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            firestore.DocumentSnapshot: A snapshot containing the document with the specified ID, or None if not found.
        """
        if isinstance(item_id, str):
            doc = self.collection.document(item_id).get()
            return doc if doc.exists else None

    def insert_item(self, item):
        """
        Insert a new item into the collection.

        Args:
            item (dict): Dictionary containing the attributes of the item to insert.
        """
        item["date_added"] = firestore.SERVER_TIMESTAMP
        self.collection.add(item)

    def update_item(self, item_id, item):
        """
        Update an existing item in the collection.

        Args:
            item_id (str): The ID of the item to update.
            item (dict): Dictionary containing the updated attributes of the item.
        """
        item["date_added"] = firestore.SERVER_TIMESTAMP
        self.collection.document(item_id).set(item)

    def delete_item(self, item_id):
        """
        Delete an item from the collection by its ID.

        Args:
            item_id (str): The ID of the item to delete.
        """
        self.collection.document(item_id).delete()
