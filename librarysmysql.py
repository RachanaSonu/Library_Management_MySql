import pymysql
from datetime import datetime

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password="admin",
    db='library_books',
    cursorclass=pymysql.cursors.DictCursor
)

# Create a cursor object
cursor = connection.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    year_published INT,
    person VARCHAR(255),
    taken_date DATE,
    due_date DATE
)
"""
cursor.execute(create_table_query)

def add_book():
    id = int(input("Enter book ID: "))  # Prompt the user for the book ID
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    year_published = int(input("Enter year of publication: "))
    person = input("Enter book taken person's name: ")
    taken_date = input("Enter taken date (YYYY-MM-DD): ")
    due_date = input("Enter due date (YYYY-MM-DD): ")

    insert_query = "INSERT INTO books (id, title, author, year_published, person, taken_date, due_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (id, title, author, year_published, person, taken_date, due_date))
    connection.commit()
    print("Book added successfully.")

def delete_book():
    book_id = int(input("Enter book ID to delete: "))
    delete_query = "DELETE FROM books WHERE id = %s"
    cursor.execute(delete_query, (book_id,))
    connection.commit()
    print("Book deleted successfully.")

def edit_book():
    book_id = int(input("Enter book ID to edit: "))
    title = input("Update book title: ")
    author = input("Update author name: ")
    year_published = int(input("Update year of publication: "))
    person = input("Update book taken person's name: ")
    taken_date = input("Update book taken date (YYYY-MM-DD): ")
    due_date = input("Update book due date (YYYY-MM-DD): ")

    update_query = "UPDATE books SET title = %s, author = %s, year_published = %s, person = %s, taken_date = %s, due_date = %s WHERE id = %s"
    cursor.execute(update_query, (title, author, year_published, person, taken_date, due_date, book_id))
    connection.commit()
    print("Book edited successfully.")

def check_fine():
    person_name = input("Enter person's name to check fine: ")
    select_query = "SELECT due_date FROM books WHERE person = %s"
    cursor.execute(select_query, (person_name,))
    results = cursor.fetchall()

    today = datetime.now().date()
    for result in results:
        due_date = result['due_date']
        print(f"Due Date: {due_date}")  # Add this print statement for debugging
        if today > due_date:
            days_overdue = (today - due_date).days
            fine = days_overdue * 10
            print(f"{person_name} has a fine of {fine} rs due to {days_overdue} days overdue.")
        else:
            print(f"{person_name} has no fine.")

def display_all():
    select_query = "SELECT * FROM books"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for record in records:
        print(record)

def exit_program():
    print("Exiting program. Goodbye!")
    cursor.close()
    connection.close()
    exit()

def invalid_choice():
    print("Invalid choice. Please try again.")

while True:
    print(end='\n')
    print("L I B R A R Y    M A N A G E M E N T ")
    print("1. Add Book\n2. Delete Book\n3. Edit Book\n4. Check Fine\n5. Display All\n6. Exit")
    choice = int(input("Enter your choice: "))
    print(end='\n')

    if choice == 1:
        add_book()

    elif choice == 2:
        delete_book()

    elif choice == 3:
        edit_book()

    elif choice == 4:
        check_fine()

    elif choice == 5:
        display_all()

    elif choice == 6:
        exit_program()

    else:
        invalid_choice()
