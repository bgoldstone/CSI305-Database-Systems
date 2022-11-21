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
    cursor.execute("SELECT * FROM city WHERE CountryCode='AFG'")
    print("City Column Names:", cursor.column_names)
    afganistanCities = cursor.fetchall()
    print("City Row Count:", cursor.rowcount)
    for row in afganistanCities:
        print(row)

    cursor.execute("SELECT * FROM city WHERE CountryCode='GGG'")
    print("City Column Names:", cursor.column_names)
    GGGCities = cursor.fetchall()
    print("City Row Count:", cursor.rowcount)
    for row in GGGCities:
        print(row)
    print()
    cursor.close()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM city WHERE CountryCode='AFG'")
    afganistanCititesDict = cursor.fetchall()
    for row in afganistanCititesDict:
        print(row['Name'])
    print()
    cursor.execute(
        "SELECT avg(Population), CountryCode FROM city GROUP BY CountryCode")
    afganCountryPop = cursor.fetchall()
    for pop in afganCountryPop:
        print(pop)
    cursor.execute(
        "SELECT avg(Population) as avgPop, CountryCode FROM city GROUP BY CountryCode")
    afganCountryPop = cursor.fetchall()
    for pop in afganCountryPop:
        print(f'{pop["avgPop"]:.2f}\n{pop["CountryCode"]}')
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
