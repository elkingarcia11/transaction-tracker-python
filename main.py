from transaction_manager import TransactionManager


def main():
    """    
        This function serves as the entry point for the script. 
        It offers an interactive interface for the user to interact with the database.

    Args:
        None

    Returns:
        None

    Description:

        This function enters a loop where the user can perform various actions on the database such as retrieving, adding, updating,
        and deleting transactions.

        The user can input the following commands (Case insensitive):
        - "G": Get a transaction
        - "A": Add a new transaction
        - "U": Update an existing transaction
        - "D": Delete a transaction

        The script will continue to loop until manually terminated.

    Example:
        Run the script, and the user will be prompted to enter a command ("G", "A", "U", "D").
        Depending on the command, the script will interact with the database collection
        based on user actions.
    """

    while True:
        manager = TransactionManager()
        command = str(
            input("Enter what you want to do (G, A, U, D): ")).lower()
        if command == "g":
            manager.get()
        elif command == "a":
            manager.add()
        elif command == "u":
            manager.update()
        elif command == "d":
            manager.delete()


main()
