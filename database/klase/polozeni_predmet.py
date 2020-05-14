from database.klase.predmet import Predmet

class PolozeniPredmet(Predmet):
    def __init__(self, sifra_predmeta, naziv, broj_casova_nedeljno, broj_semestra, ocena=6, nastavnici=[]):
        super().__init__(sifra_predmeta, naziv, broj_casova_nedeljno, broj_semestra, nastavnici)
        self.ocena = ocena