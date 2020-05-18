from database.data_handler import DataHandler
import json
import pickle


class SerialHandler(DataHandler):
    def __init__(self, meta_filepath, filepath=""):
        super().__init__()
        self.filepath = "database/data/" + filepath
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.data = []
        self.metadata = {}
        if filepath == "":
            self.filepath += getattr(self.metadata, "path_to_file")
        self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "rb") as dfile:
                self.data = pickle.load(dfile)
        except FileNotFoundError:
            print(self.filepath)
            print("File nije pronadjen!")
            self.save_data()
            print("File kreiran!")
        
        try:
            with open(self.meta_filepath, "rb") as meta_file:
                self.metadata = json.load(meta_file)
        except FileNotFoundError:
            print(self.meta_filepath)
            print("Meta file nije pronadjen!")

    def save_data(self):
        with open(self.filepath, "wb") as f:
            pickle.dump(self.data, f)

    def get_one(self, id):
        return self.data[self.search[id]]

    def get_all(self):
        return self.data

    def insert(self, obj):
        self.data.append(obj)
        self.save_data()

    def insert_many(self, obj_list):
        if len(obj_list) > 0:
            if not isinstance(obj_list, list):
                return
            for obj in obj_list:
                self.insert(obj)

    def edit(self, id, attr, value):
        setattr(self.data[self.search(id)], attr, value)
        self.save_data()

    def delete_one(self, id):
        self.data.remove(self.data[self.search(id)])
        self.save_data()

    def search(self, id):
        for d in range(len(self.data)):
            if getattr(self.data[d], (self.metadata["key"])) == getattr(id, (self.metadata["key"])):
                return d
        return None

