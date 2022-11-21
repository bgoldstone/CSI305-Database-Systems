# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:57:07 2022

@author: Benjamin Goldstone
"""

import mysql.connector


def main():
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        username="root",
        password="",
        database="characters"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM npcs")
    allRows = cursor.fetchall()
    print(cursor.column_names)
    for row in allRows:
        print(row)
    print()

    # cursor.execute(
    # """INSERT
    # INTO
    # npcs
    # VALUES (
    #   11,
    #  'Breia',
    #  'De Marlo',
    #  'gnome',
    #   '120',
    #   'bard',
    #   'good')
    # """)
    # print(cursor.rowcount)
    # for row in allRows:
    #    print(row)
    # print()
    insertQuery = """INSERT
        INTO
        npcs
        VALUES (
            %s,%s,%s,%s,%s,%s,%s)
        """
    insertData = (11,
                  'Breia',
                  'De Marlo',
                  'gnome',
                  '120',
                  'bard',
                  'good')
    cursor.execute(
        insertQuery, insertData)
    db.commit()

    print(cursor.rowcount)
    insertQueryResult = cursor.fetchall()
    cursor.execute("SELECT * FROM npcs")
    allRows = cursor.fetchall()
    allRowsTuple = tuple(allRows)
    print(allRowsTuple)
    for row in allRows:
        print(row)
    print()

    cursor.execute("DELETE FROM npcs WHERE id=11")
    db.commit()
    print(cursor.rowcount)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
