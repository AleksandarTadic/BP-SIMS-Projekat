import pymysql
import json

class DatabaseScheme:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            if self.connection == None:
                with open("database/db/db.json", "r") as fdb:
                    fdata = json.load(fdb)
                self.connection = pymysql.connect(host="localhost", user=fdata["user"], password=fdata["pass"], db="ustanove", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print(e)

    def disconect(self):
        self.connection.close()

    def get_scheme(self):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = "SHOW TABLES"
                cursor.execute(query, ())
                result = cursor.fetchall()
                tables = []
                for i in result:
                    tables.append(i["Tables_in_ustanove"])
                return tables
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None