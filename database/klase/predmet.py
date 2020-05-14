class Predmet():
    def __init__(self, sifra_predmeta="", naziv="", silabus="", broj_casova_nedeljno=0, broj_semestra=0, nastavnici=[]):
        super().__init__()
        self.sifra_predmeta = sifra_predmeta
        self.naziv = naziv
        self.silabus = silabus
        self.broj_casova_nedeljno = broj_casova_nedeljno
        self.broj_semestra = broj_semestra
        self.nastavnici = nastavnici
