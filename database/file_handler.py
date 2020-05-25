import json
from database.sequential_handler import SequentialHandler
from database.serial_handler import SerialHandler

class FileHandler():
    def __init__(self, meta_filepath):
        self.meta_filepath = meta_filepath
        self.temp_metadata = None
        try:
            with open("database/metadata/" +  self.meta_filepath, "rb") as temp_meta_file:
                self.temp_metadata = json.load(temp_meta_file)
        except FileNotFoundError:
            print("Metadata file nije pronadjen!")
    def get_handler(self):
        if self.temp_metadata["type"] == "sequential":
            return SequentialHandler(self.meta_filepath, self.temp_metadata["path_to_file"])
        else:
            return SerialHandler(self.meta_filepath, self.temp_metadata["path_to_file"])
