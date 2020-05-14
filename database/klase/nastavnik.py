class Nastavnik():
    def __init__(self, sifra_zaposlenog="", ime="", prezime="", datum_rodjenja="", tip=""):
        super().__init__()
        self.sifra_zaposlenog = sifra_zaposlenog
        self.ime = ime
        self.prezime = prezime
        self.datum_rodjenja = datum_rodjenja
        self.tip = tip