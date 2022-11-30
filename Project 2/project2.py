import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import CursorBase
import datetime
import re
import time
from typing import List

"""
     Name: Ben Goldstone
     Date: 12/09/2022
     Description: A program that interacts with a MySQL database table called google_play_store to perform inserts, reads, and deletes.
"""


def main() -> None:
    """
    main Main function of the dbms.
    """
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        username="root",
        password="",
        database="google_play_store"
    )
    cursor = db.cursor()
    dict_cursor = db.cursor(dictionary=True)
    menu(db, cursor, dict_cursor)
    cursor.close()
    dict_cursor.close()
    db.disconnect()


def menu(db: MySQLConnection, cursor: CursorBase, dict_cursor: CursorBase) -> None:
    """
    menu Menu for Database Management System.

    Args:
        db (MySQLConnection): Database connection
        cursor (CursorBase): Regular Cursor
        dict_cursor (CursorBase): Dictionary cursor
    """
    option = ''
    while option.upper() != 'E':
        time.sleep(1)
        print("\n\n\n")
        option = input('''Welcome to the Google Play Store Database Management System!
(I)nsert Data into the apps table
(D)elete data from the apps table
(O)utput data from the apps table
(In)sert data into the apps and genre tables
(De)lete data from the apps and genre tables
(Ou)tput data from the apps and genre tables
(Out)put data from the apps, genre, and content_rating tables
(E)xit the program\n\n
Please enter an option: ''')
        if option.upper() == 'I':
            insert_app(db, cursor, dict_cursor)
        elif option.upper() == 'D':
            delete_app(db, dict_cursor)
        elif option.upper() == 'O':
            search_app(dict_cursor)
        elif option.upper() == 'IN':
            print("Inserting App Entry ...")
            pk = insert_app(db, cursor, dict_cursor)
            insert_genre(pk, db, cursor, dict_cursor)
            dict_cursor.execute(
                "SELECT * FROM genre_play_store_apps WHERE id=%s", pk)
            entry = dict_cursor.fetchone()
            print(
                f"Your app and genre have been successfully inserted!\n{entry}\n")
        elif option.upper() == 'DE':
            delete_app_genre(db, cursor, dict_cursor)
        elif option.upper() == 'OU':
            search_app_genre(dict_cursor)
        elif option.upper() == 'OUT':
            search_app_genre_content_rating(dict_cursor)
        elif option.upper() == 'E':
            print("\nThank your for using this Google Play Store Database.\nGoodbye!\n")
        else:
            print("Please enter a valid option")


def insert_app(db: MySQLConnection, cursor: CursorBase, dict_cursor: CursorBase) -> int:
    """
    insert_app inserts these attributes into the apps table:
        App
        rating
        reviews
        size
        is_free
        price
        last_updated
        current_version
        android_version
    Args:
        db (MySQLConnection): Database connection object
        cursor (CursorBase): Cursor object
        dict_cursor (CursorBase): Dictionary cursor object
    Returns:
        int: ID of item that was inserted
    """
    inputs = []
    check_app_name = "SELECT * FROM apps WHERE App=(%s)"
    query = "INSERT INTO apps(App,rating,reviews,size,is_free,price,last_updated,current_version,android_version) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute("SELECT * FROM apps")
    cursor.fetchall()

    name = ""
    while cursor.rowcount > 0:
        if name != "":
            print(
                "That App name already exists in the database. Please enter a new App name\n")
        name = input(
            "Please enter a App name for your application to insert: ")
        try:
            cursor.execute(check_app_name, (name,))
            cursor.fetchone()
        except ValueError as e:
            print(f'An error occurred: {e}')
    inputs.append(name)
    inputs.append(float(
        input("Please enter a rating for your app to insert (Between 1.0 and 5.0): ")))
    inputs.append(int(
        input("Please enter a review count for your app to insert: ")))
    size = float(
        input("Please enter a size for your app to insert (in Megabytes): "))
    inputs.append(f'{size}M')
    is_free = None
    while is_free is None:
        is_free = input("Is your app free (Y/N)? ")
        if is_free.upper().startswith("Y"):
            is_free = 1
            price = 0.0
        elif is_free.upper().startswith("N"):
            is_free = 0
            try:
                price = float(input("What is the price of your app(in USD): "))
            except ValueError:
                print("Please enter a floating point value!")
                is_free = None
        else:
            is_free = None
    inputs.append(is_free)
    inputs.append(price)

    # DATE VALIDATION
    print("Next, we will be asking you when the last time you updated your app was.\n")
    year = "00000000"
    while not re.match(r'^[\d]{4}$', year):
        try:
            year = input("\tWhat is the year when your app was last updated?")
        except ValueError:
            print("\tPlease enter a valid year in four digit format (Ex. YYYY)!\n")
    month = "00000000"
    while not re.match(r'^[\d]{1,2}$', month):
        try:
            month = input(
                "\tWhat is the month when your app was last updated?")
        except ValueError:
            print("\tPlease enter a valid month in numerical format (Ex. MM)!\n")
    day = "00000000"
    while not re.match(r'^[\d]{1,2}$', day):
        try:
            day = input("\tWhat is the day when your app was last updated?")
        except ValueError:
            print("\tPlease enter a valid day in numerical format (Ex. DD)!\n")
    # END DATE VALIDATION and DATE insert
    try:
        inputs.append(datetime.datetime(int(year), int(month), int(day)))
    except ValueError:
        print("The date your have entered is not valid. Please try again.\n\n")
        insert_app(db, cursor, dict_cursor)
        return
    inputs.append(
        input("Please enter a current version of the app(Ex. 4.0.0): "))
    inputs.append(input(
        "Please enter the android_version of the app(Ex. 4.0.0): ") + " and up")
    inputs = tuple([str(inp) for inp in inputs])
    # INSERT app entry
    try:
        print(
            f"The query executing will be: {query, (inputs)}\n\n")
        cursor.execute(query, inputs)
        db.commit()
        dict_cursor.execute("SELECT * FROM apps ORDER BY id DESC LIMIT 1")
        inserted_entry = dict_cursor.fetchall()
        print(
            f"Database Entry successfully inserted!!\n\n{inserted_entry}")
    except Exception as e:
        print(
            f'An error has occurred while trying to inserting your app into the database: {e}')
    return inserted_entry[0]['id'] if inserted_entry else -1


def delete_app(db: MySQLConnection, cursor_dict: CursorBase) -> None:
    """
    delete_app Deletes an app from the app table

    Args:
        db (MySQLConnection): Database connection object
        cursor_dict (CursorBase): Dictionary cursor object
    """
    cursor_dict.execute("SELECT * FROM apps WHERE id=-1")
    cursor_dict.fetchone()
    app_name = None
    while cursor_dict.rowcount == 0:
        if app_name is not None:
            print("Please enter a full app name!\n")
        app_name = input("What is the name of the app you want to delete? ")
        print(app_name)
        cursor_dict.execute("SELECT * FROM apps WHERE App=%s", (app_name,))
        entry = cursor_dict.fetchone()
    cursor_dict.execute("DELETE FROM apps WHERE App=%s", (app_name,))
    cursor_dict.fetchone()
    db.commit()
    # Returns deleted entry to the user
    print(f"Successfully deleted app {app_name}\n\t{entry}")


def search_app(dict_cursor: CursorBase) -> None:
    """
    search_app Searches the app table for a specified app

    Args:
        db (MySQLConnection): Database connection object
        dict_cursor (CursorBase): Dictionary Cursor object
    """
    query = "SELECT * FROM apps WHERE app LIKE %s ORDER BY App"
    continue_searching = True
    while continue_searching:

        search = input("Please select a search term for the apps table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        data = "\n".join(str(attr)
                         for attr in [f'{row}\n\n' for row in dict_cursor.fetchall()])
        print(data)
        option = input("Would you like to continue searching? (y/n): ")
        continue_searching = True if option.lower()[0] == 'y' else False


def insert_genre(pk: int, db: MySQLConnection, cursor: CursorBase, dict_cursor: CursorBase) -> None:
    """
    insert_genre Inserts a genre in the database.

    Args:
        pk (int): primary key of the app to insert the genre
        db (MySQLConnection): Database connection object
        cursor (CursorBase): Cursor object
        dict_cursor (CursorBase): Dictionary cursor object
    """
    print("Inserting genre entry...")
    cursor.execute("SELECT DISTINCT Genres FROM genres;")
    query = "INSERT INTO genres(app_id, Genres) VALUES( % s, % s)"
    genres = cursor.fetchall()
    genre = -1
    while genre > len(genres) and genre < 0:
        if genre != -1:
            print("Please type in a valid index!")
        try:
            genre = int(input(
                f"Genres: {[f'{(index,genre)}' for index,genre in enumerate(genres)]}\n\nPlease Select a genre(1,2,3): "))
        except ValueError:
            print("Please enter a valid integer!")
    try:
        cursor.execute(query, (pk, genres[genre]))
        db.commit()
        dict_cursor.execute(
            "SELECT app_id,Genres FROM genres WHERE app_id=%s AND Genre=%s", (pk, genres[genre]))
        print(
            f"Genre entry has successfully been inserted! {dict_cursor.fetchall()}")
    except Exception as e:
        print(f'The genre could not be inserted. Error:{e}')


def delete_app_genre(db: MySQLConnection, cursor: CursorBase, dict_cursor: CursorBase) -> None:
    """
    delete_app_genre Deletes an app and genre entry from the database given the primary key.

    Args:
        db (MySQLConnection): Database connection object
        cursor (CursorBase): Cursor object
        dict_cursor (CursorBase): Dictionary cursor object
    """
    cursor.execute("SELECT id FROM genre_play_store_apps")
    primary_keys = [int(item[0]) for item in cursor.fetchall()]
    pk = -1
    while pk not in primary_keys:
        input("Please enter a valid id to remove from the app and genre tables:")
    dict_cursor.execute("SELECT * FROM genre_play_store_apps WHERE id=%s", pk)
    entry = dict_cursor.fetchone()
    try:
        cursor.execute("DELETE FROM genres WHERE app_id=%s", pk)
        cursor.execute("DELETE FROM apps WHERE App=%s", pk)
        print(
            f"Your entry was successfully deleted from apps and genres!\n{entry}\n")
    except Exception as e:
        print(f"Your delete was unsuccessful! Error {e}")


def search_app_genre(dict_cursor: CursorBase) -> None:
    """
    search_app_genre Searches the app and genre table for a specified app

    Args:
        dict_cursor (CursorBase): Dictionary Cursor object
    """
    query = "SELECT * FROM genre_play_store_apps WHERE app LIKE %s ORDER BY App"
    continue_searching = True
    while continue_searching:

        search = input(
            "Please select a search term for the app and genres table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        data = "\n".join(str(attr)
                         for attr in [f'{row}\n' for row in dict_cursor.fetchall()])
        print(data)
        option = input("Would you like to continue searching? (y/n): ")
        continue_searching = True if option.lower()[0] == 'y' else False


def search_app_genre_content_rating(dict_cursor: CursorBase) -> None:
    """
    search_app_genre_contentRating Searches the app, genre, and content_rating tables for a specified app

    Args:
        dict_cursor (CursorBase): Dictionary Cursor object
    """
    query = "SELECT genre_play_store_apps.id as id,App,genres,`Content Rating`,rating,reviews,size,is_free,price,last_updated,current_version,android_version FROM google_play_store.genre_play_store_apps JOIN (SELECT id,content_rating_id FROM apps) as contentRating ON genre_play_store_apps.id=contentRating.id JOIN content_rating ON contentRating.content_rating_id= content_rating.id WHERE app LIKE %s ORDER BY App"
    continue_searching = True
    while continue_searching:

        search = input(
            "Please select a search term for the app, genres, and content_rating table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        data = "\n".join(str(attr)
                         for attr in [f'{row}\n\n' for row in dict_cursor.fetchall()])
        print(data)
        option = input("Would you like to continue searching? (y/n): ")
        continue_searching = True if option.lower()[0] == 'y' else False


if __name__ == '__main__':
    main()
