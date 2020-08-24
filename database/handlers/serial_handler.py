import json
import pickle

class SerialHandler:
    def __init__(self, meta_filepath, filepath):
        super().__init__()
        self.filepath = "database/data/" + filepath
        self.meta_filepath = "database/metadata/" + meta_filepath
        self.metadata = {}
        self.load_metadata()

    def load_metadata(self):
        try:
            with open(self.meta_filepath, "r") as meta_file:
                self.metadata = json.load(meta_file)
        except FileNotFoundError:
            print("Meta file nije pronadjen!")

    def get_all(self):
        try:
            with open(self.filepath, "r") as f:
                lines = f.read().splitlines()
                data = []
                for d in lines:
                    data.append(self.to_dict(d))
                return data
        except FileNotFoundError:
            print(self.filepath)

    def insert(self, obj):
        try:
            with open(self.filepath, "a") as f:
                f.write(self.to_text(obj))
        except FileNotFoundError:
            print(self.filepath)

    def edit(self, id, attr, value):
        with open(self.filepath, "r+") as f:
            lines = f.read().splitlines()
            f.seek(0)
            found = False
            for ln in lines:
                current_line = self.to_dict(ln)
                if id == current_line and found == False:
                    new_value= id
                    new_value[attr] = value
                    found = True
                    f.write(self.to_text(new_value))
                else:
                    f.write(ln + '\n')
            f.truncate()

    def delete_one(self, obj):
        # with open(self.filepath, "r+") as f:
        #     deleted = False
        #     while True:
        #         line = f.readline().strip()
        #         if line == "":
        #             break
        #         current_line = self.to_dict(line)
        #         if obj == current_line and deleted == False:
        #             deleted = True
        #             continue
        #         f.write(line + "\n")
            
        with open(self.filepath, "r+") as f:
            lines = f.read().splitlines()
            f.seek(0)
            deleted = False
            for ln in lines:
                current_line = self.to_dict(ln)
                if obj == current_line and deleted == False:
                    deleted = True
                    continue
                f.write(ln + '\n')
            f.truncate()
            
    def to_dict(self, line):
        return dict(zip(self.metadata["collumns"], list(line.split(" <|> "))))

    def to_text(self, current_dict):
        return str(" <|> ".join(current_dict.values())) + '\n'

    def is_database(self):
        return False