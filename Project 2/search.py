from mysql.connector.cursor import CursorBase
"""
    Contains all of the search functions for Database Systems Project 2.
    Name: Ben Goldstone
    Date: 12/09/2022
"""


def search_app(dict_cursor: CursorBase) -> None:
    """
    search_app Searches the app table for a specified app

    Args:
        db (MySQLConnection): Database connection object
        dict_cursor (CursorBase): Dictionary Cursor object
    """
    query = "SELECT * FROM apps WHERE app LIKE %s ORDER BY App"
    continue_searching = True
    # Prompts user to search for items while they want to continue searching.
    while continue_searching:
        search = input("Please select a search term for the apps table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        # Formats data to print out.
        data = "\n".join(str(entry)
                         for entry in [f'{row}\n\n' for row in dict_cursor.fetchall()])
        print(data)
        option = input("Would you like to continue searching? (y/n): ")
        continue_searching = True if option.lower()[0] == 'y' else False


def search_app_genre(dict_cursor: CursorBase) -> None:
    """
    search_app_genre Searches the app and genre table for a specified app

    Args:
        dict_cursor (CursorBase): Dictionary Cursor object
    """
    query = "SELECT * FROM genre_play_store_apps WHERE app LIKE %s ORDER BY App"
    continue_searching = True
    # Prompts user to search for items while they want to continue searching.
    while continue_searching:
        search = input(
            "Please select a search term for the app and genres table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        # Formats data to print out.
        data = "\n".join(str(entry)
                         for entry in [f'{row}\n' for row in dict_cursor.fetchall()])
        print(f'\n{data}')
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
    # Prompts user to search for items while they want to continue searching.
    while continue_searching:
        search = input(
            "Please select a search term for the app, genres, and content_rating table: ")
        dict_cursor.execute(query, (f'%{search}%',))
        # Formats data to print out.
        data = "\n".join(str(entry)
                         for entry in [f'{row}\n\n' for row in dict_cursor.fetchall()])
        print(data)
        option = input("Would you like to continue searching? (y/n): ")
        continue_searching = True if option.lower()[0] == 'y' else False
