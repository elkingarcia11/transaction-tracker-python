from transaction_database import TransactionDatabase
from datetime import date


class TransactionManager:
    def __init__(self):
        self.db = TransactionDatabase()

    def get(self):
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
            items = self.db.get_items_by_name(name)
            # items = mongo_utils.get_items_by_name(name)
        else:
            transaction_number = int(
                input("Enter the number of transactions you want to retrieve: "))
            items = self.db.get_last_x_items(transaction_number)
            # items = mongo_utils.get_last_x_items(transaction_number)
        for item in items:
            print(f"{item.id} => {item.to_dict()}")

    def add(self):
        """
        Adds a new transaction record to the database based on user input.

        Args:
            None

        Returns:
            None

        Description:
            This function interacts with the user to receive input for required fields.
            If inputs are valid, the month, day and year fields are combined
            into a date_processed field. Then the function checks if the transaction is a duplicate, 
            and then proceeds to add the transaction based on user responses.

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
        if self.is_valid(item):
            new_item = {key: value for key, value in item.items() if key not in [
                "day", "month", "year"]}
            new_item["date_processed"] = date(int(item["year"]), int(
                item["month"]), int(item["day"])).isoformat()
            item_in_db = self.db.does_exist(new_item)
            if item_in_db:
                addToDb = str(input(
                    "Transaction already exists. Do you still want to add it to the database? (y/n): ")).lower()
                if addToDb == "y":
                    self.db.insert_item(new_item)
                    print("Adding duplicate now...")
                else:
                    print("Not adding duplicate to the database")
            else:
                self.db.insert_item(new_item)
                print("No existing transaction found. Adding now...")
        else:
            print("Invalid input information")

    def update(self):
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

        id = input("Enter the ID of the transaction you want to update: ")
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
            if self.db.get_items_by_id(id):
                new_item = {key: value for key, value in item.items() if key not in [
                    "day", "month", "year"]}
                new_item["date_processed"] = date(int(item["year"]), int(
                    item["month"]), int(item["day"])).isoformat()
                print("Updated successfully")
                self.db.update_item(id, new_item)
            else:
                print("Invalid ID")
        else:
            print("Invalid input information")

    def delete(self):
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

        id = str(input("Enter the ID of the transaction you want to delete: "))
        self.db.delete_item(id)

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
        except (ValueError, TypeError):
            return False


# Example usage:
if __name__ == "__main__":
    manager = TransactionManager()
    while True:
        action = input(
            "What do you want to do? (get/add/update/delete/exit): ")
        if action == "get":
            manager.get()
        elif action == "add":
            manager.add()
        elif action == "update":
            manager.update()
        elif action == "delete":
            manager.delete()
        elif action == "exit":
            break
        else:
            print("Invalid action")
