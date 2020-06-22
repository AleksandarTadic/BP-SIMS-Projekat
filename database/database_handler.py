# from database.data_handler import DataHandler
import pymysql
import json
from klase.nivo_studija import NivoStudija

class DatabaseHandler:
    def __init__(self, meta_filepath, table):
        self.table = table
        self.data = []
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.metadata = {}
        self.connection = None
        self.load_data()

    def connect(self):
        try:
            if self.connection == None:
                self.connection = pymysql.connect(host="localhost", user="root", password="admin", db="projekat", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print(e)

    def disconect(self):
        self.connection.close()

    def load_data(self):
        try:
            self.connect()
            try:
                with open(self.meta_filepath, "rb") as meta_file:
                    self.metadata = json.load(meta_file)
            except FileNotFoundError:
                print(self.meta_filepath)
                print("Meta file nije pronadjen!")
            with self.connection.cursor() as cursor:
                # query = "SHOW TABLES"
                query = "Select * FROM " + self.table
                cursor.execute(query, ())
                result = cursor.fetchall()
                self.data = result
                print(self.data)
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None

    def save_data(self):
        try:
            self.connect()
            self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None

    def insert(self, obj):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = self.get_query(1)
                obj = tuple(vars(obj).values())
                cursor.execute(query, obj)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None

    def delete_one(self, obj):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = self.get_query(2)
                primary_keys = []
                for i in self.metadata["key"]:
                    t = getattr(obj, i)
                    primary_keys.append(t)
                tuple(primary_keys)
                cursor.execute(query, primary_keys)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None

    def edit(self, id, attr, value):
        print("radi")



    def get_query(self, num):
        query = ""
        if num == 1:
            query = "INSERT INTO " + self.table + " ("
            for i in self.metadata["collumns"]:
                query += (i + ", ")
            query = query[:-2]
            query += ") VALUES ("
            for i in self.metadata["collumns"]:
                query += ("%s" + ", ")
            query = query[:-2]
            query += ")"
            return query

        elif num == 2:
            query = "DELETE FROM " + self.table + " WHERE "
            for i in self.metadata["key"]:
                query += (i + " = " + "%s" + " AND ")
            query = query[:-5]
            return query
    
    def is_database(self):
        return True

wat = DatabaseHandler("nivo_studija_metadata.json", "nivo_studija")
t = NivoStudija(7, "test")
# wat.insert(t)
wat.delete_one(t)
wat.save_data()
# wat.save_data()