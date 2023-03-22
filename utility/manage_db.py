'''
Allows the user to enter strings to be added to the database
'''

import sqlite3
import sys

DB_NAME = "db/responses.db"

def add_to_db():
    '''
    Allows the user to enter strings to be added to the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS sick_responses
                 (response text)''')
    
    # Get the response from the user
    response = input("Enter a response: ")
    
    # Add the response to the database
    c.execute("INSERT INTO sick_responses VALUES (?)", (response,))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Response added to database")

def delete_from_db(response):
    '''
    Deletes a response from the database
    
    Parameters:
        response (str): The response to delete
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete the response from the database
    c.execute("DELETE FROM sick_responses WHERE response = ?", (response,))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Response deleted from database")

def list_responses():
    '''
    Lists all the responses in the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Get all the responses
    c.execute("SELECT * FROM sick_responses")
    responses = c.fetchall()
    
    # Close the connection
    conn.close()
    
    # Print the responses
    for response in responses:
        print(response[0])

def clear():
    '''
    Clears all the responses from the database
    '''
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete all the responses
    c.execute("DELETE FROM sick_responses")
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Responses cleared from database")

if __name__ == "__main__":
    # Get the first argument
    arg = sys.argv[1]

    # If the argument is "add"
    if arg == "add":
        add_to_db()
        
    # If the argument is "delete"
    elif arg == "delete":
        delete_from_db(sys.argv[2])
        
    # If the argument is "list"
    elif arg == "list":
        list_responses()
            
    # If the argument is "clear"
    elif arg == "clear":
        # Get the confirmation
        confirmation = input("Are you sure you want to clear the database? (y/n): ")
        if confirmation == "y":
            clear()
        
    # If the argument is "help"
    elif arg == "help":
        print("Usage: python manage_db.py [add|delete|list|clear]")
        
    # If the argument is not valid
    else:
        print("Invalid argument")
        print("Usage: python manage_db.py [add|delete|list|clear]")