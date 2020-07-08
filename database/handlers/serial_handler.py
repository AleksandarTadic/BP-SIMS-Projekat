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
        self.data[self.search(id)][attr] = value
        self.save_data()

    def delete_one(self, id):
        self.data.remove(self.data[self.search(id)])
        self.save_data()

    def search(self, id):
        for d in range(len(self.data)):
            if self.concat(self.data[d]) == self.concat(id):
                return d
        return None

    def concat(self, keys):
        primary_key = ""
        for i in range(len(self.metadata["key"])):
            primary_key += str(keys[self.metadata["key"][i]])
        return primary_key

    def get_filtered_data(self, selected, selected_metadata):
        filtered_data = []
        for d in range(len(self.data)):
            current = ""
            filter_sel = ""
            for i in range(len(self.metadata["key"])):
                for j in range(len(selected_metadata["key"])):
                    if self.metadata["key"][i] == selected_metadata["key"][j]:
                        current += str(self.data[d][self.metadata["key"][i]])
                        filter_sel += str(selected[selected_metadata["key"][j]])
            if (current == filter_sel) and (len(current) != 0 or len(filter_sel) != 0):
                filtered_data.append(self.data[d])
        return filtered_data

    def is_database(self):
        return False