import mysql.connector


def main():
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        username="root",
        password=""
    )
    cursor = db.cursor()
    print("Cursor Column Names: ", cursor.column_names)
    cursor.execute("USE world")
    cursor.execute("SELECT * FROM city")
    print("City Column Names:", cursor.column_names)
    print("City Row Count:", cursor.rowcount)
    allRows = cursor.fetchall()
    print("All Entries\n", allRows)
    for row in allRows:
        print(row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
