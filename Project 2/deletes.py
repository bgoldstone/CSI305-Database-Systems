from mysql.connector import MySQLConnection
from mysql.connector.cursor import CursorBase

"""
    Contains all of the delete functions for Database Systems Project 2.
    Name: Ben Goldstone
    Date: 12/09/2022
"""


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
        db.commit()
        print(
            f"Your entry was successfully deleted from apps and genres!\n{entry}\n")
    except Exception as e:
        print(f"Your delete was unsuccessful! Error {e}")
