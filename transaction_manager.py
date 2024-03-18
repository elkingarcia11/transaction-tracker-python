from transaction_database import TransactionDatabase
from datetime import date


class TransactionManager:
    """
    A class for managing transactions including validation, retrieval, addition, updating, and deletion.

    Attributes:
        None
    """

    def __init__(self):
        self.db = TransactionDatabase("clients")

    # VALIDATION FUNCTIONS
    def get_valid_string_input(self, prompt):
        """
        Prompt user for string input and validate it.
        """
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print("Input cannot be empty. Please try again.")

    def get_valid_numeric_input(self, prompt):
        """
        Prompt user for numeric input and validate it.
        """
        while True:
            user_input = input(prompt).strip()
            if user_input.isdigit():
                return user_input
            print("Invalid input. Please enter a valid number.")

    def get_valid_amount_input(self, prompt):
        """
        Prompt user for amount input and validate it.
        """
        while True:
            user_input = input(prompt).strip()
            try:
                # Check if input can be converted to float
                float(user_input)
                # Assuming DD.CC format, check if it has two decimal places
                if len(user_input.split('.')[1]) == 2:
                    return user_input
                else:
                    print("Invalid amount format. Please enter in DD.CC format.")
            except ValueError:
                print("Invalid input. Please enter a valid amount.")

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
            print("An error occurred:", e)
            return False
    # GETTERS

    def get_user_command(self):
        """
        Get user command for action.

        Returns:
            str: User command for action (G, A, U, D).
        """
        return input("Enter what you want to do (G, A, U, D): ").strip().lower()

    def get_items(self, searchByName=False, name=None, x=None):
        """
        Get transaction items based on user input.

        Args:
            searchByName (bool): Flag indicating whether to search by name.
            name (str): Name to search if searchByName is True.
            x (int): Number of transactions to retrieve if searchByName is False.

        Returns:
            list: List of transaction items.
        """
        items = []
        if searchByName:
            items = self.db.get_items_by_name(name)
        else:
            items = self.db.get_last_x_items(x)
        return items

    # SETTERS

    def add_transaction(self):
        """
        Add a new transaction to the database.
        """
        item = {
            "name": self.get_valid_string_input("Enter name: ").lower(),
            "invoice": self.get_valid_string_input("Enter invoice number: ").lower(),
            "receipt": self.get_valid_string_input("Enter receipt number: ").lower(),
            "amount": self.get_valid_amount_input("Enter amount paid (Format: DD.CC): "),
            "month": self.get_valid_numeric_input("Enter the month the zelle processed: "),
            "day": self.get_valid_numeric_input("Enter the day the zelle processed: "),
            "year": self.get_valid_numeric_input("Enter the year the zelle processed: ")
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

    def update_transaction(self):
        """
        Update an existing transaction in the database.
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

    def delete_transaction(self):
        """
        Delete a transaction from the database.
        """
        id = str(input("Enter the ID of the transaction you want to delete: "))
        self.db.delete_item(id)

    def main(self):
        """
        Main function to interact with the TransactionDatabase.

        Allows users to perform actions like retrieving, adding, updating, and deleting transactions.
        """

        while True:
            command = self.get_user_command()
            if command in ['g', 'a', 'u', 'd']:
                if command == "g":
                    searchByName = str(
                        input("Do you want to search by name? (Format: y/n) ")).lower()
                    if searchByName == "y":
                        name = str(
                            input("Enter the full name as it appears on the transaction: ")).lower()
                        items = self.get_items(
                            searchByName=True, name=name)
                    else:
                        x = int(
                            input("Enter the number of transactions you want to retrieve: "))
                        items = self.get_items(x=x)
                    for item in items:
                        print(f"{item.id} => {item.to_dict()}")
                elif command == "a":
                    self.add_transaction()
                elif command == "u":
                    self.update_transaction()
                elif command == "d":
                    self.delete_transaction()
            else:
                print("Invalid input. Please enter one of: G, A, U, D.")
