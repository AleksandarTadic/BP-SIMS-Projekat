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
