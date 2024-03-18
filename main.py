from transaction_database import TransactionDatabase
from datetime import date


class TransactionManager:
    def __init__(self):
        pass

    def is_valid(self, item):
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
        except Exception as e:
            # Handle the exception
            print("An error occurred:", e)
            return False

    def main(self):
        db = TransactionDatabase()

        while True:
            command = input(
                "Enter what you want to do (G, A, U, D): ").strip().lower()
            if command in ['g', 'a', 'u', 'd']:
                if command == "g":
                    searchByName = str(
                        input("Do you want to search by name? (Format: y/n) ")).lower()
                    items = []
                    if searchByName == "y":
                        name = str(
                            input("Enter the full name as it appears on the transaction: ")).lower()
                        items = db.get_items_by_name(name)
                    else:
                        x = int(
                            input("Enter the number of transactions you want to retrieve: "))
                        items = db.get_last_x_items(x)
                    for item in items:
                        print(f"{item.id} => {item.to_dict()}")
                elif command == "a":
                    item = {
                        "name": input("Enter name: ").lower(),
                        "invoice": input("Enter invoice number: ").lower(),
                        "receipt": input("Enter receipt number: ").lower(),
                        "amount": input("Enter amount paid (Format: DD.CC): "),
                        "month": input("Enter the month the zelle processed: "),
                        "day": input("Enter the day the zelle processed: "),
                        "year": input("Enter the year the zelle processed: ")
                    }

                    if self.is_valid(item):
                        new_item = {key: value for key, value in item.items() if key not in [
                            "day", "month", "year"]}
                        new_item["date_processed"] = date(int(item["year"]), int(
                            item["month"]), int(item["day"])).isoformat()
                        item_in_db = db.does_exist(new_item)
                        if item_in_db:
                            addToDb = str(input(
                                "Transaction already exists. Do you still want to add it to the database? (y/n): ")).lower()
                            if addToDb == "y":
                                db.insert_item(new_item)
                                print("Adding duplicate now...")
                            else:
                                print("Not adding duplicate to the database")
                        else:
                            db.insert_item(new_item)
                            print("No existing transaction found. Adding now...")
                    else:
                        print("Invalid input information")
                elif command == "u":
                    id = input(
                        "Enter the ID of the transaction you want to update: ")
                    item = {
                        "name": input("Enter name: "),
                        "invoice": input("Enter invoice number: "),
                        "receipt": input("Enter receipt number: "),
                        "amount": input("Enter amount paid (Format: DD.CC): "),
                        "month": input("Enter the month the zelle processed: "),
                        "day": input("Enter the day the zelle processed: "),
                        "year": input("Enter the year the zelle processed: ")
                    }
                    if self.is_valid(item):
                        if db.get_items_by_id(id):
                            new_item = {key: value for key, value in item.items() if key not in [
                                "day", "month", "year"]}
                            new_item["date_processed"] = date(int(item["year"]), int(
                                item["month"]), int(item["day"])).isoformat()
                            print("Updated successfully")
                            db.update_item(id, new_item)
                        else:
                            print("Invalid ID")
                    else:
                        print("Invalid input information")
                elif command == "d":
                    id = str(
                        input("Enter the ID of the transaction you want to delete: "))
                    db.delete_item(id)
                else:
                    print("Invalid input. Please enter one of: G, A, U, D.")


# Instantiate the TransactionManager class and run the main function
if __name__ == "__main__":
    manager = TransactionManager()
    manager.main()
