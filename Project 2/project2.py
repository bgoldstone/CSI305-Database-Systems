import mysql.connector
import datetime
import re
import time
from typing import List

DB = mysql.connector.connect(
    host="localhost",
    port=3306,
    username="root",
    password="",
    database="google_play_store"
)
CURSOR = DB.cursor()
DATE_FORMAT = r'[\d]{4}-[\d]{1,2}-[\d]{1,2}'
HAS_BEEN_RESET = False
CURSOR.execute("SHOW COLUMNS FROM apps")
APP_COLUMNS = [item[0] for item in CURSOR.fetchall()]


def main():
    menu()
    CURSOR.close()
    DB.disconnect()


def menu():
    option = ''
    while option.upper() != 'E':
        time.sleep(1)
        print("\n\n\n")
        option = input('''Welcome to the Google Play Store Database Management System!
(I)nsert Data into the apps table
(D)elete data from the apps table
(O)utput date from the apps table
(In)sert data into the apps and genre tables
(De)lete data from the apps and genre tables
(Ou)tput data from the apps and genre tables
(Out)put data from the apps, genre, and content_rating tables
(R)eset Database
(E)xit the program\n\n
Please enter an option: ''')
        if option.upper() == 'I':
            insert_app()
        else:
            print("Please enter a valid option")


def insert_app():
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
    """
    inputs = []
    check_app_name = "SELECT * FROM apps WHERE App=(%s)"
    query = "INSERT INTO apps(App,rating,reviews,size,is_free,price,last_updated,current_version,android_version) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    CURSOR.execute("SELECT * FROM apps")
    CURSOR.fetchall()

    name = ""
    while CURSOR.rowcount > 0:
        if name != "":
            print(
                "That App name already exists in the database. Please enter a new App name\n")
        name = input(
            "Please enter a App name for your application to insert: ")
        try:
            CURSOR.execute(check_app_name, (name,))
            CURSOR.fetchone()
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
    inputs.append(datetime.datetime(int(year), int(month), int(day)))
    inputs.append(
        input("Please enter a current version of the app(Ex. 4.0.0): "))
    inputs.append(input(
        "Please enter the android_version of the app(Ex. 4.0.0): ") + " and up")
    inputs = tuple([str(inp) for inp in inputs])
    try:
        print(
            f"The query executing will be: {query, (inputs)}")
        CURSOR.execute(query, inputs)
        DB.commit()
        CURSOR.execute("SELECT * FROM apps ORDER BY id DESC LIMIT 1")
        print(
            f"Database Entry successfully inserted!!\n{APP_COLUMNS}\n{CURSOR.fetchall()}")
    except Exception as e:
        print(
            f'An error has occurred while trying to inserting your app into the database: {e}')


if __name__ == '__main__':
    main()
