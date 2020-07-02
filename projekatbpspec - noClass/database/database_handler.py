import pymysql
import json
# from klase.nivo_studija import NivoStudija

class DatabaseHandler:
    def __init__(self, meta_filepath, table):
        self.table = table
        self.data = []
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.metadata = {}
        self.connection = None
        self.load_data()
        try:
            with open(self.meta_filepath, "rb") as meta_file:
                self.metadata = json.load(meta_file)
        except FileNotFoundError:
            print(self.meta_filepath)
            print("Meta file nije pronadjen!")

    def connect(self):
        try:
            if self.connection == None:
                self.connection = pymysql.connect(host="localhost", user="root", password="admin", db="ustanove", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print(e)

    def disconect(self):
        self.connection.close()

    def load_data(self):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                # query = "SHOW TABLES"
                query = self.get_query(0)
                cursor.execute(query, ())
                result = cursor.fetchall()
                self.data = result
                # print(self.data)
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None
    
    def get_all(self):
        return self.data

    # def get_all(self):
    #     # ili mozda samo ici return self.data 
    #     try:
    #         self.connect()
    #         with self.connection.cursor() as cursor:
    #             # query = "SHOW TABLES"
    #             query = "Select * FROM " + self.table
    #             cursor.execute(query, ())
    #             result = cursor.fetchall()
    #             return result
    #     except pymysql.MySQLError as e:
    #         print(e)
    #     finally:
    #         self.disconect()
    #         self.connection = None
        
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
                obj = tuple(obj.values())
                cursor.execute(query, obj)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None
            # ovo je test za load_data 
            self.load_data()

    def delete_one(self, obj):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = self.get_query(2)
                primary_keys = []
                for i in self.metadata["key"]:
                    t = obj[i]
                    primary_keys.append(t)
                tuple(primary_keys)
                cursor.execute(query, primary_keys)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None
            # ovo je test za load_data
            self.load_data()

    def edit(self, obj, attr, value):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = self.get_query(3, attr, str(value))
                print(query)
                primary_keys = []
                for i in self.metadata["key"]:
                    t = obj[i]
                    primary_keys.append(t)
                tuple(primary_keys)
                cursor.execute(query, primary_keys)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconect()
            self.connection = None
            # ovo je test za load_data
            self.load_data()

    def get_query(self, num, col=None, value=None):
        query = ""
        if num == 0:
            query = "Select * FROM " + self.table
            return query
        elif num == 1:
            query = "INSERT INTO " + self.table + " ("
            for i in self.metadata["collumns"]:
                query += (i + ", ")
            query = query[:-2]
            query += ") VALUES ("
            for i in range(len(self.metadata["collumns"])):
                if self.metadata["attr_type"][i] == "date":
                    query += ("STR_TO_DATE(%s, "'%d%m%Y'")" + ", ")
                else:
                    query += ("%s" + ", ")
            query = query[:-2]
            query += ")"
            print(query)
            return query
        elif num == 2:
            query = "DELETE FROM " + self.table + " WHERE "
            for i in self.metadata["key"]:
                query += (i + " = " + "%s" + " AND ")
            query = query[:-5]
            return query
        elif num == 3:
            query = "UPDATE " + self.table + " SET " + col + "='"+ value + "' WHERE "
            for i in self.metadata["key"]:
                query += (i + " = " + "%s" + " AND ")
            query = query[:-5]
            return query
    
    def concat(self, keys):
        primary_key = ""
        for i in range(len(self.metadata["key"])):
            primary_key += str(keys[self.metadata["key"][i]])
        return primary_key

    def is_database(self):
        return True




# wat = DatabaseHandler("nivo_studija_metadata.json", "nivo_studija")
# wat.edit()
# t = NivoStudija(7, "test")
# wat.insert(t)
# wat.delete_one(t)
# wat.save_data()
# print(wat.get_all()[1][wat.metadata["collumns"][1]])
# getattr(self.selected_data, (self.data_list.metadata["collumns"][i]))
# wat.save_data()
