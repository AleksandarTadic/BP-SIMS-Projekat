from database.klase.predmet import Predmet


class NepolozeniPredmet(Predmet):
    def __init__(self, sifra_predmeta, naziv, broj_casova_nedeljno, broj_semestra,broj_pokusaja=1, nastavnici=[]):
        super().__init__(sifra_predmeta, naziv, broj_casova_nedeljno, broj_semestra, nastavnici)
        self.broj_pokusaja = broj_pokusaja