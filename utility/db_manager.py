import sqlite3
import sys

DB_NAME = "db/responses.db"

def add_to_db(table, response):
    '''
    Adds a response to the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Add the response to the database
    c.execute(f"INSERT INTO {table} VALUES (?)", (response,))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Response added to database")

def delete_from_db(table, response):
    '''
    Deletes a response from the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete the response from the database
    c.execute(f"DELETE FROM {table} WHERE response = ?", (response,))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Response deleted from database")

def list_responses(table):
    '''
    Lists all the responses in the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Get all the responses
    c.execute(f"SELECT * FROM {table}")
    responses = c.fetchall()
    
    # Close the connection
    conn.close()
    
    # Print the responses
    for response in responses:
        print(response[0])

def clear(table):
    '''
    Clears all the responses from the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete all the responses from the database
    c.execute(f"DELETE FROM {table}")
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Responses cleared from database")

def list_tables():
    '''
    Lists all the tables in the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Get all the tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    
    # Close the connection
    conn.close()
    
    # Print the tables
    for table in tables:
        print(table[0])

def create_table(table):
    '''
    Creates a table in the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create the table
    c.execute(f"CREATE TABLE {table} (response TEXT)")
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print(f"Created table {table}")

def delete_table(table):
    '''
    Deletes a table from the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete the table
    c.execute(f"DROP TABLE {table}")
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print(f"Deleted table {table}")

def get_random_response(table):
    '''
    Gets a random response from the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Get a random response
    c.execute(f"SELECT response FROM {table} ORDER BY RANDOM() LIMIT 1")
    response = c.fetchone()[0]
    
    # Close the connection
    conn.close()
    
    return response

def run_query(query):
    '''
    Runs a query on the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Run the query
    c.execute(query)
    result = c.fetchall()
    
    # Close the connection
    conn.close()
    
    return result

def help():
    print("add <table> <response> - Adds a response to the database")
    print("delete <table> <response> - Deletes a response from the database")
    print("list <table> - Lists all the responses in the database")
    print("clear <table> - Clears all the responses from the database")
    print("list_tables - Lists all the tables in the database")
    print("create_table <table> - Creates a table in the database")
    print("delete_table <table> - Deletes a table from the database")
    print("get_random_response <table> - Gets a random response from the database")
    print("run_query <query> - Runs a query on the database")
    print("help - Shows this help message")

# Run the script from the command line
if __name__ == "__main__":
    # Get the arguments
    args = sys.argv[1:]

    if len(args) == 0:
        help()
        sys.exit()
    
    # Check if the arguments are valid
    if len(args) < 2 and args[0] != "help" and args[0] != "list_tables":
        print("Invalid arguments")
        sys.exit()
    
    # Get the command and the response
    command = args[0]
    table = args[1] if len(args) > 1 else None
    response = " ".join(args[2:])
    
    # Check the command
    if command == "add":
        add_to_db(table, response)
    elif command == "delete":
        delete_from_db(table, response)
    elif command == "list":
        list_responses(table)
    elif command == "clear":
        clear(table)
    elif command == "list_tables":
        list_tables()
    elif command == "create_table":
        create_table(response)
    elif command == "delete_table":
        delete_table(table)
    elif command == "get_random_response":
        print(get_random_response(table))
    elif command == "run_query":
        print(run_query(response))
    elif command == "help":
        help()
    else:
        print("Invalid command")