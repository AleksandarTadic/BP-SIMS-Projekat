from database.file_handler import FileHandler

lista = [
    "visokoskolska_ustanova_metadata.json",
    "nivo_studija_metadata.json",
    "nastavni_predmet_metadata.json",
    "studijski_programi_metadata.json",
    "studenti_metadata.json",
    "plan_studijske_grupe_metadata.json",
    "tok_studija_metadata.json"
]

for l in lista:
    x = FileHandler(l).get_handler()




                # fiter test
            selected_object_model = self.data_list.get_all()[index.row()]
            for i in range(len(self.subtables)):
                self.subhandler = FileHandler(self.data_list.metadata["linked_files"][i]).get_handler()
                filtered_data = []
                for d in range(len(self.subhandler.get_all())):
                    current = ""
                    filter_sel = ""

                    for j in range(len(self.subhandler.metadata["key"])):

                        for k in range(len(self.data_list.metadata["key"])):

                            if self.subhandler.metadata["key"][j] == self.data_list.metadata["key"][k]:
                                current += self.subhandler.get_all()[d][self.subhandler.metadata["key"][j]]
                                filter_sel += selected_object_model[self.data_list.metadata["key"][k]]

                    if (current == filter_sel) and (len(current) != 0 or len(filter_sel) != 0):
                        filtered_data.append(self.subhandler.data[d])
                        print("test=", current," - ", filter_sel)




selected_object_model = self.data_list.get_all()[index.row()]
for i in range(len(self.subtables)):
    self.subhandler = FileHandler(self.data_list.metadata["linked_files"][i]).get_handler()
    filtered_data = []


    for d in range(len(self.subhandler.get_all())):
        current = ""
        filter_sel = ""

        if self.data_list.metadata["linked_keys"] != False:
            linked_keys = self.data_list.metadata["linked_keys"]
            for j in range(len(linked_keys)):
                if linked_keys[j]["name"] == self.subhandler.metadata["class"]:
                    for k in range(len(linked_keys[j]["fk"])):
                        current += self.subhandler.get_all()[d][self.subhandler.metadata["linked_keys"][j]["fk"][k]]
                        filter_sel += selected_object_model[self.data_list.metadata["linked_keys"][j]["k"][k]]


        if (current == filter_sel) and (len(current) != 0 or len(filter_sel) != 0):
            filtered_data.append(self.subhandler.data[d])
            print("test=", current," - ", filter_sel)

