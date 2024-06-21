import sqlite3
import pandas as pd
import os


class SQLiteDB:
    def __init__(self):
        pass

    def table_creation(self):
        """
            Method Name: table_creation
            Description: This method is used to create a new table in database .
            Output:  Returns html table created from input data.
            On Failure: None
            Written By: Digiotai
            Version: 1.0
            Revisions: None
        """

        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                cursor = c.cursor()
                query = """
                CREATE TABLE user_tracking (
                  user_id INT PRIMARY KEY,
                  Quota VARCHAR(40) NOT NULL DEFAULT FREE,
                  count INT DEFAULT 10
                  );"""
                cursor.execute(query)
                c.commit()
        except Exception as e:
            print(e)

    def table_deletion(self):
        """
            Method Name: tabledeletion
            Description: This method is used to delete an existing table from database .
            Output:  None
            On Failure: None

            Written By: Digiotai
            Version: 1.0
            Revisions: None
        """
        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                cursor = c.cursor()
                query = """
                DROP TABLE {name}
                  );"""
                cursor.execute(query)
                c.commit()
        except Exception as e:
            print(e)

    def add_user(self, user_id):
        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                cursor = c.cursor()
                query = f"""
                INSERT INTO user_tracking (user_id) VALUES('{user_id}');"""
                cursor.execute(query)
                c.commit()
        except Exception as e:
            print(e)

    def get_user_data(self, user_id):
        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                cursor = c.cursor()
                query = f"""SELECT * from user_tracking where user_id='{user_id}'"""
                cursor.execute(query)
                res = cursor.fetchone()
                print(res)
                c.commit()
                return res
        except Exception as e:
            print(e)

    def update_count(self, user_id):
        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                cursor = c.cursor()
                query = f"""UPDATE user_tracking SET count = count - 1 where user_id='{user_id}'"""
                cursor.execute(query)
                res = cursor.fetchone()
                c.commit()
                return res
        except Exception as e:
            print(e)


if __name__ == "__main__":
    db = SQLiteDB()
    # db.table_creation()
    db.add_user('kpi')
    print(db.get_user_data('test'))
    # print(db.update_count('Rami'))
    # print(db.get_user_data('Rami'))
