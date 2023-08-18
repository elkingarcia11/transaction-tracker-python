
import configparser
import mongo_utils
import utils

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

    Example:
        config = read_config('config.ini')
        value = config.get('section', 'key')
    """

    config = configparser.ConfigParser()
    config.read(file_name)
    return config

def main():
    """    
        This function serves as the entry point for the script. It initializes the database
        connection and offers an interactive interface for the user to interact with the database.
    
    Args:
        None

    Returns:
        None

    Example:
        Run the script, and the user will be prompted to enter a command ("G", "A", "U", "D").
        Depending on the command, the script will interact with the MongoDB collection
        based on user actions.

    Description:
        
        This function reads configuration settings from an .ini file, establishes a
        connection to a MongoDB database, and then enters a loop where the user can
        perform various actions on the database such as retrieving, adding, updating,
        and deleting transactions.

        The user can input the following commands (Case insensitive):
        - "G": Get a transaction
        - "A": Add a new transaction
        - "U": Update an existing transaction
        - "D": Delete a transaction

        The script will continue to loop until manually terminated.

    Note:
        Ensure you have a valid '.ini' file containing configuration settings.
    """

    conf = read_config('.ini')
    connection = mongo_utils.connect(conf)
    db = mongo_utils.get_database(connection, conf['PROD']['db_name']) 
    collection = mongo_utils.get_collection(db, conf['PROD']['db_collection'])

    while True:
        command = str(input("Enter what you want to do (G, A, U, D): ")).lower()
        if command == "g":

            mongo_utils.get_item(collection)
        elif command == "a":
            mongo_utils.add_item(collection)
        elif command == "u":
            mongo_utils.update_item(collection)
        elif command == "d":
            mongo_utils.delete_item(collection) 

main()