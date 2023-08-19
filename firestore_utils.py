import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

def initialize_database(collection_name):
    cred = credentials.Certificate("keys/credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection(collection_name)
    return collection

def get_items_by_name(name):
    if type(name) == str:
        docs = (collection.where(filter=FieldFilter("name", "==", name)).stream())
        return docs

def get_last_x_items(number):
    docs = (collection.order_by("dateProcessed", direction=firestore.Query.DESCENDING).limit(number).stream())
    return docs

def does_exist(item):
    query = collection.where(filter=FieldFilter("name", "==", item["name"])).where(
    filter=FieldFilter("amount", "==", item["amount"])).where(
    filter=FieldFilter("dateProcessed", "==", item["dateProcessed"]))
    docs = query.stream()
    for doc in docs:
        return True
    return False
    
def insert_item(item):
    collection.document().set(item)

def update_item(id, item):
    collection.document(id).set(item)

def delete_item(id):
    collection.document(id).delete()


collection = initialize_database("clients")
