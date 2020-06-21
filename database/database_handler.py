# from database.data_handler import DataHandler
import pymysql
import json
from klase.nivo_studija import NivoStudija

class DatabaseHandler:
    def __init__(self, meta_filepath, table):
        self.connection = pymysql.connect(host="localhost", user="root", password="admin", db="projekat", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        self.table = table
        self.data = []
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.metadata = {}
        self.load_data()

    def get_connection(self):
        return pymysql.connect(host="localhost", user="root", password="admin", db="projekat", charset="utf8", cursorclass=pymysql.cursors.DictCursor)

    def load_data(self):
        self.connection = self.get_connection()
        try:
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
        finally:
            self.connection.close()

    def save_data(self):
        self.connection = self.get_connection()
        try:
            with self.connection.cursor() as cursor:
                self.connection.commit()
        finally:
            self.connection.close()

    def insert(self, obj):
        self.connection = self.get_connection()
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO " + self.table + " ("
                for i in self.metadata["collumns"]:
                    query += (i + ", ")
                query = query[:-2]
                query += ") VALUES ("
                for i in self.metadata["collumns"]:
                    query += ("%s" + ", ")
                query = query[:-2]
                query += ")"
                print(query)

                obj = tuple(vars(obj).values())
                cursor.execute(query, obj)
        finally:
            self.connection.close()
    
    # def is_database(self):
    #     return True

wat = DatabaseHandler("nivo_studija_metadata.json", "nivo_studija")
t = NivoStudija(4, "test")
wat.insert(t)
wat.save_data()
# wat.save_data()