from database.data_handler import DataHandler
import json
import pickle


class SequentialHandler(DataHandler):
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
        temp_object = self.data[self.binary_search(id)]
        if temp_object is not None:
            return temp_object
        else:
            print("Objekat nije pronadjen!")

    def get_all(self):
        return self.data

    def insert(self, obj):
        location = self.find_location_binary(obj)
        if (location == None):
            self.data.append(obj)
        else:
            self.data.insert(location, obj)
        self.save_data()

    def insert_many(self, obj_list):
        if len(obj_list) > 0:
            if not isinstance(obj_list, list):
                return
            for obj in obj_list:
                self.insert(obj)

    # def edit(self, id, col, value):
    #     change_data = self.data[self.binary_search(id)]
    #     setattr(change_data, self.metadata["collumns"][col], value)
    #     # self.save_data()

    def edit(self, id, attr, value):
        change_data = self.data[self.binary_search(id)]
        setattr(change_data, attr, value)
        self.save_data()

    def delete_one(self, id):
        temp_object = self.data[self.binary_search(id)]
        if temp_object is not None:
            self.data.remove(temp_object)
            self.save_data()
  
    def binary_search(self, id):
        start = 0
        end = len(self.data)-1
        found = False
        while (start <= end and not found):
            mid = start + (end - start)//2
            if getattr(self.data[mid], (self.metadata["key"])) == getattr(id, (self.metadata["key"])):
                found == True
                return mid
            elif getattr(self.data[mid], (self.metadata["key"])) < getattr(id, (self.metadata["key"])):
                start = mid + 1
            else:
                end = mid - 1
        return None

    # def find_location_binary(self, obj):
    #     start = 0
    #     end = len(self.data)-1
    #     while start <= end:
    #         mid = start + (end - start)//2
    #         if getattr(self.data[start], (self.metadata["key"])) > getattr(obj, (self.metadata["key"])):
    #             return start
    #         elif getattr(self.data[mid], (self.metadata["key"])) > getattr(obj, (self.metadata["key"])):
    #             return mid
    #         elif getattr(self.data[mid], (self.metadata["key"])) < getattr(obj, (self.metadata["key"])):
    #             start = mid + 1
    #         else:
    #             end = mid - 1
    #     return None

    def find_location_binary(self, obj):
        start = 0
        end = len(self.data)-1
        while start <= end:
            mid = start + (end - start)//2
            if getattr(self.data[mid], (self.metadata["key"])) > getattr(obj, (self.metadata["key"])) and getattr(self.data[mid-1], (self.metadata["key"])) < getattr(obj, (self.metadata["key"])):
                return mid
            elif getattr(self.data[mid], (self.metadata["key"])) < getattr(obj, (self.metadata["key"])):
                start = mid + 1
            else:
                end = mid - 1
        return start




