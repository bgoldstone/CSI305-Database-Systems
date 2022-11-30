from mysql.connector import MySQLConnection
from mysql.connector.cursor import CursorBase
import re
import datetime
from typing import Callable, Union

"""
    Contains all of the insert functions for Database Systems Project 2.
    Name: Ben Goldstone
    Date: 12/09/2022
"""


def insert_app(db: MySQLConnection, cursor: CursorBase, dict_cursor: CursorBase) -> Union[int, Callable]:
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
        return insert_app(db, cursor, dict_cursor)
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
