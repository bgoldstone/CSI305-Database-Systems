import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import CursorBase
import time
from inserts import insert_app, insert_genre
from deletes import delete_app, delete_app_genre
from search import search_app, search_app_genre, search_app_genre_content_rating

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
                "SELECT * FROM genre_play_store_apps WHERE id=%s", (pk,))
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


if __name__ == '__main__':
    main()
