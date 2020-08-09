import json
import pickle


class SerialHandler:
    def __init__(self, meta_filepath, filepath):
        super().__init__()
        self.filepath = "database/data/" + filepath
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.data = []
        self.metadata = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.meta_filepath, "r") as meta_file:
                self.metadata = json.load(meta_file)
        except FileNotFoundError:
            print("Meta file nije pronadjen!")
        try:
            with open(self.filepath, "r") as f:
                lines = f.read().splitlines()
                l_data = []
                for d in lines:
                    l_data.append(dict(zip(self.metadata["collumns"], list(d.split(" <|> ")))))
                self.data = l_data
        except FileNotFoundError:
            print(self.filepath)
            self.save_data()  

    def save_data(self):
        with open(self.filepath, "w") as f:
            for c_data in self.data:
                f.writelines(str(" <|> ".join(c_data.values())) + '\n')

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
        self.data[self.search(id)][attr] = value
        self.save_data()

    def delete_one(self, id):
        self.data.remove(self.data[self.search(id)])
        self.save_data()

    def search(self, id):
        for d in range(len(self.data)):
            if self.data[d] == id:
                return d
        return None

    # def concat(self, keys):
    #     primary_key = ""
    #     for i in range(len(self.metadata["key"])):
    #         primary_key += str(keys[self.metadata["key"][i]])
    #     return primary_key

    def is_database(self):
        return False