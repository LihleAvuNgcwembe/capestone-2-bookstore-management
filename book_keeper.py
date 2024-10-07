'''Import necessary libraries'''

import sqlite3
import sys
import os

'''-----------------------Book Class Starts------------------------------'''

"""Book class will be used to create an book obkect that contains a title,
author, and quantity attribute. It contains method edit data stored in an
object
"""


class Book:

    # Initialize an instance of a book class
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty
    # Remove book from list and database

    def remove_book(self):
        try:
            with sqlite3.connect('ebookstore.db') as db:
                cursor = db.cursor()
                cursor.execute(
                    "DELETE FROM book WHERE title = ? AND author = ?",
                    (self.title, self.author))
                db.commit()

        except sqlite3.Error as error:
            print(f"Error: {error}")
            db.rollback()
            raise error

    # Change title
    def set_title(self):
        try:
            old_title = self.title
            new_title = input("Enter the new title: ")
            self.title = new_title

            with sqlite3.connect('ebookstore.db') as db:
                cusror = db.cursor()
                cusror.execute(
                    "UPDATE book SET title = ? WHERE title = ? AND author = ?",
                    (new_title, old_title, self.author))
            print("Update Successfull")
            db.commit()

        except sqlite3.Error as error:
            print(f"Error: {error}")
            db.rollback()
            raise error

    # Change author
    def set_author(self):
        try:
            old_author = self.author
            new_author = input("Enter name of the author: ")
            self.author = new_author

            with sqlite3.connect('ebookstore.db') as db:
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE book SET author =? WHERE title =? AND author =?",
                    (new_author, self.title, old_author))
            print("Update Successfull")
            db.commit()

        except sqlite3.Error as error:
            print(f"Error: {error}")
            db.rollback()
            raise error

    # Change quantity
    def set_qty(self):
        try:
            new_qty = int(input("Enter the quantity: "))
            self.qty = new_qty

            with sqlite3.connect('ebookstore.db') as db:
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE book SET qty = ? WHERE title = ? AND author = ?",
                    (new_qty, self.title, self.author))
            print("Update Successfull")
            db.commit()

        except (sqlite3.Error, ValueError) as error:
            print(f"Error: {error}")
            db.rollback()
            raise error


'''------------------------User-define functions-------------------------'''

"""The create_book_method will create the book table in the ebookstore
database if the book table doesn't exist"""


def create_book_table():
    try:
        with sqlite3.connect('ebookstore.db') as db:
            cursor = db.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS book(
                    id INTEGET PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    qty INTEGER)''')
        db.commit()
    except (sqlite3.Error, Exception) as error:
        print(f"Error: {error}")
        db.rollback()
        raise error


"""The add_book method will ask the user for the title, author, and quantity
of the book they wish to enter> Then it will create a new book object with
those attributes then insert those details in both the database and list
"""


def add_book(list):
    try:
        title = input("Enter title name: ")
        author = input("Enter name of author: ")
        qty = int(input("Enter quantity of book: "))

        book = Book(title, author, qty)
        insert_book(book)
        list.append(book)

    except ValueError as error:
        print(f"Error: {error}")


"""The insert_book method will insert book object's data into the database"""


def insert_book(book):
    try:
        with sqlite3.connect('ebookstore.db') as db:
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO book(title, author, qty) VALUES(?, ?, ?)''',
                (book.title, book.author, book.qty))
            print("New record added!")
            db.commit()

    except sqlite3.Error as error:
        print("Failed to send data to sqlite table", error)
        db.rollback()
        raise error


''' The search_book() asks the user for either the title or author name.
It will then search in the list for an item that contains this theses
characters
'''


def search_book(list):
    matches = []

    # Determine which attribute to use when searching for a book
    print("Enter t/T to search for title")
    print("Enter a/A to search for author")
    search_attr = input("Enter here: ").lower()

    # search using title of the book
    if search_attr == 't':
        search_title = input("Enter name of the book: ")
        for match in list:

            # Made everthing lower to make more case insensitive
            if search_title.lower() in match.title.lower():
                matches.append(match)

    # Search using the author of the book
    elif search_attr == 'a':
        search_author = input("Enter authors name: ")
        for match in list:
            if search_author.lower() in match.author.lower():
                matches.append(match)

    # If input is not any of the listed option
    else:
        print("You have enterd an non-optional letter")
    if len(matches) == 0:
        print("We have found nothing!")
    else:
        for count, item in enumerate(matches):
            print(f'''{count} - {item.title} by {item.author}
current stock: {item.qty}''')

    return matches


'''The primary function for this method is to clear and update the list
everytime it is called'''


# Insert data from database into list
def update_book_list(list):
    try:

        '''
         I wanted remove all data in list so that the same data
         Won't be copied each time the list is updated
        '''

        list.clear()
        with sqlite3.connect('ebookstore.db') as db:
            cursor = db.cursor()

            # Get all data from the database
            cursor.execute('''SELECT title, author, qty FROM book''')

            # Insert all data into a empty list
            for row in cursor:
                list.append(Book(row[0], row[1], row[2]))
            print("Book list has been successfully updated!")

    except Exception as e:
        db.rollback()
        raise e


"""The delete_book() method will search for specific record in list then
delete that book record from database then update the list
"""


def delete_book(list):
    filtered_list = search_book(list)
    if len(filtered_list) == 0:
        print("list is empty")
    if len(filtered_list) > 1:
        try:

            # Choose the item based on the index
            user_input = int(input("Please enter the index here: "))

            target_book = filtered_list[user_input]
            print(f'''
You have chosen '{target_book.title}' by {target_book.author}
current stock {target_book.qty}''')

            delete = int(input(
                "do you wish to delete: \n1 - yes \n2 - no \nEnter here: "))

            if delete == 1:
                target_book.remove_book()
                update_book_list(list)

            if delete == 2:
                print(
                    f"delection of '{target_book.title}' has been terminated")

        except (ValueError, IndexError) as error:
            print(f"Error: {error}")

    elif len(filtered_list) == 1:
        try:
            delete = int(input(
                "do you wish to delete: \n1 - yes \n2 - no \nEnter here: "))

            if delete == 1:
                filtered_list[0].remove_book()
                update_book_list(list)

            if delete == 2:
                print(
                    f"deletion of '{filtered_list[0].title}' terminated")

        except ValueError as error:
            print(f"Error: {error}")


"""The update method will be used to update a single record
in both the database and the list
"""


def update_book(list):

    filtered_list = search_book(list)

    if len(filtered_list) == 0:
        print("List is empty")

    elif len(filtered_list) >= 1:
        try:
            # Choose the item based on the index
            user_input = int(input("Please enter the index here: "))

            target_book = filtered_list[user_input]

            print(f''''{target_book.title}' by {target_book.author}
            current stock {target_book.qty}''')
            print('''which attribute do you wish to update:
1 - Name
2 - Author
3 - Quantity''')

            update_value = int(input("Enter here: "))

            # Update title
            if update_value == 1:
                target_book.set_title()

            # Update author
            elif update_value == 2:
                target_book.set_author()

            # Update quantity
            elif update_value == 3:
                target_book.set_qty()

            update_book_list(list)

        except ValueError as error:
            print(f"Error: {error}")


'''------------------------------Main Function----------------------------'''

# Change directory to current path
script_dr = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dr)

# A list to store all books object from the database
book_list = []

# Create book table in ebookstore if does not exist
create_book_table()

# Populate the list with data from the database
update_book_list(book_list)

menu = True
while menu == True:

    try:

        user_input = int(input('''\n Would you like to:
    1. Enter a new book
    2. Update existing book
    3. Delete book
    4. Search for a book
    0. Exit
    Enter a index here: '''))

        # To exit out of the program
        if user_input == 0:
            print('Goodbye!!!')
            menu = False  # The loop will terminate

        # Add a book
        elif user_input == 1:
            add_book(book_list)

        # Update book deltails stored in database and list
        elif user_input == 2:
            update_book(book_list)

        # Delete a book record
        elif user_input == 3:
            delete_book(book_list)

        # Search for a specific book
        elif user_input == 4:
            search_book(book_list)

        # If number is not listed in options
        else:
            print('Index does not exist!')

    # To catch any value errors
    except ValueError as error:
        print("Error: {0}".format(error))
