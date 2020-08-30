USE ustanove;

DROP PROCEDURE IF EXISTS DobaviVisokoskolskeUstanove;
DROP PROCEDURE IF EXISTS DodajVisokoskolskuUstanovu;
DROP PROCEDURE IF EXISTS IzbrisiVisokoskolskuUstanovu;
DROP PROCEDURE IF EXISTS IzmeniVisokoskolskuUstanovu;

DELIMITER \
CREATE PROCEDURE DobaviVisokoskolskeUstanove()
BEGIN
	select * from visokoskolska_ustanova;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajVisokoskolskuUstanovu(in oznaka_in CHAR(2), in naziv_in VARCHAR(80), in adresa_in VARCHAR(80))
BEGIN
	INSERT INTO visokoskolska_ustanova (oznaka, naziv, adresa) VALUES(oznaka_in, naziv_in, adresa_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiVisokoskolskuUstanovu(in oznaka_in CHAR(2))
BEGIN
	DELETE FROM visokoskolska_ustanova WHERE visokoskolska_ustanova.oznaka = oznaka_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniVisokoskolskuUstanovu(in oznaka_in CHAR(2), in naziv_in VARCHAR(80), in adresa_in VARCHAR(80))
BEGIN
	UPDATE visokoskolska_ustanova SET visokoskolska_ustanova.naziv = naziv_in, visokoskolska_ustanova.adresa = adresa_in WHERE visokoskolska_ustanova.oznaka = oznaka_in;
END \
DELIMITER ;










DROP PROCEDURE IF EXISTS DobaviNivoStudija;
DROP PROCEDURE IF EXISTS DodajNivoStudija;
DROP PROCEDURE IF EXISTS IzbrisiNivoStudija;
DROP PROCEDURE IF EXISTS IzmeniNivoStudija;

DELIMITER \
CREATE PROCEDURE DobaviNivoStudija()
BEGIN
	select * FROM nivo_studija;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajNivoStudija(in oznaka_in CHAR(2), in naziv_in VARCHAR(80))
BEGIN
	INSERT INTO nivo_studija (oznaka, naziv) VALUES (oznaka_in, naziv_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiNivoStudija(in oznaka_in CHAR(2))
BEGIN
	DELETE FROM nivo_studija WHERE nivo_studija.oznaka = oznaka_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniNivoStudija(in oznaka_in CHAR(2), in naziv_in VARCHAR(80))
BEGIN
	UPDATE nivo_studija SET nivo_studija.naziv = naziv_in WHERE nivo_studija.oznaka = oznaka_in;
END \
DELIMITER ;










DROP PROCEDURE IF EXISTS DobaviNastavniPredmet;
DROP PROCEDURE IF EXISTS DodajNastavniPredmet;
DROP PROCEDURE IF EXISTS IzbrisiNastavniPredmet;
DROP PROCEDURE IF EXISTS IzmeniNastavniPredmet;

DELIMITER \
CREATE PROCEDURE DobaviNastavniPredmet()
BEGIN
	select * FROM nastavni_predmet;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajNastavniPredmet(in ustanova_in CHAR(2), in oznaka_in VARCHAR(6), in naziv_in VARCHAR(120), in espb_in INT)
BEGIN
	INSERT INTO nastavni_predmet (ustanova, oznaka, naziv, espb) VALUES (ustanova_in, oznaka_in, naziv_in, espb_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiNastavniPredmet(in ustanova_in CHAR(2), in oznaka_in VARCHAR(6))
BEGIN
	DELETE FROM nastavni_predmet WHERE nastavni_predmet.ustanova = ustanova_in AND nastavni_predmet.oznaka = oznaka_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniNastavniPredmet(in ustanova_in CHAR(2), in oznaka_in VARCHAR(6), in naziv_in VARCHAR(120), in espb_in INT)
BEGIN
	UPDATE nastavni_predmet SET nastavni_predmet.naziv = naziv_in, nastavni_predmet.espb = espb_in WHERE nastavni_predmet.ustanova = ustanova_in AND nastavni_predmet.oznaka = oznaka_in;
END \
DELIMITER ;








DROP PROCEDURE IF EXISTS DobaviStudijskePrograme;
DROP PROCEDURE IF EXISTS DodajStudijskiProgram;
DROP PROCEDURE IF EXISTS IzbrisiStudijskePrograme;
DROP PROCEDURE IF EXISTS IzmeniStudijskePrograme;

DELIMITER \
CREATE PROCEDURE DobaviStudijskePrograme()
BEGIN
	select * FROM studijski_programi;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajStudijskiProgram(in ustanova_in CHAR(2), in nivo_in INT, in oznaka_programa_in VARCHAR(3), in naziv_programa_in VARCHAR(120))
BEGIN
	INSERT INTO studijski_programi (ustanova, nivo, oznaka_programa, naziv_programa) VALUES (ustanova_in, nivo_in, oznaka_programa_in, naziv_programa_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiStudijskePrograme(in ustanova_in CHAR(2), in oznaka_in VARCHAR(6))
BEGIN
	DELETE FROM studijski_programi WHERE studijski_programi.ustanova = ustanova_in AND studijski_programi.oznaka_programa = oznaka_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniStudijskePrograme(in ustanova_in CHAR(2), in nivo_in INT, in oznaka_programa_in VARCHAR(3), in naziv_programa_in VARCHAR(120))
BEGIN
	UPDATE studijski_programi SET studijski_programi.nivo = nivo_in , studijski_programi.naziv_programa=naziv_programa_in WHERE ustanova = ustanova_in AND oznaka_programa = oznaka_programa_in;
END \
DELIMITER ;













DROP PROCEDURE IF EXISTS DobaviPlanStudijskeGrupe;
DROP PROCEDURE IF EXISTS DodajPlanStudijskeGrupe;
DROP PROCEDURE IF EXISTS IzbrisiPlanStudijskeGrupe;
DROP PROCEDURE IF EXISTS IzmeniPlanStudijskeGrupe;

DELIMITER \
CREATE PROCEDURE DobaviPlanStudijskeGrupe()
BEGIN
	select * FROM plan_studijske_grupe;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajPlanStudijskeGrupe(in program_ustanove_in CHAR(2), in oznaka_programa_in VARCHAR(3), in blok_in INT, in pozicija_in INT, in ustanova_predmet_in CHAR(2), in oznaka_predmeta_in VARCHAR(6))
BEGIN
	INSERT INTO plan_studijske_grupe (program_ustanove, oznaka_programa, blok, pozicija, ustanova_predmet, oznaka_predmeta) VALUES (program_ustanove_in, oznaka_programa_in, blok_in, pozicija_in, ustanova_predmet_in, oznaka_predmeta_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiPlanStudijskeGrupe(in program_ustanove_in CHAR(2), in oznaka_programa_in VARCHAR(3), in blok_in INT, in pozicija_in INT)
BEGIN
	DELETE FROM plan_studijske_grupe WHERE plan_studijske_grupe.program_ustanove = program_ustanove_in AND plan_studijske_grupe.oznaka_programa = oznaka_programa_in AND plan_studijske_grupe.blok = blok_in AND plan_studijske_grupe.pozicija = pozicija_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniPlanStudijskeGrupe(in program_ustanove_in CHAR(2), in oznaka_programa_in VARCHAR(3), in blok_in INT, in pozicija_in INT, in ustanova_predmet_in CHAR(2), in oznaka_predmeta_in VARCHAR(6))
BEGIN
	UPDATE plan_studijske_grupe SET plan_studijske_grupe.ustanova_predmet = ustanova_predmet_in, plan_studijske_grupe.oznaka_predmeta = oznaka_predmeta_in WHERE program_ustanove = program_ustanove_in AND oznaka_programa = oznaka_programa_in AND blok = blok_in AND pozicija = pozicija_in;
END \
DELIMITER ;






















DROP PROCEDURE IF EXISTS DobaviStudente;
DROP PROCEDURE IF EXISTS DodajStudenta;
DROP PROCEDURE IF EXISTS IzbrisiStudenta;
DROP PROCEDURE IF EXISTS IzmeniStudenta;

DELIMITER \
CREATE PROCEDURE DobaviStudente()
BEGIN
	select * FROM studenti;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajStudenta(in ustanova_in CHAR(2), in struka_in CHAR(2), in broj_indeksa_in VARCHAR(6), in prezime_in varchar(20), in ime_roditelja_in VARCHAR(20), in ime_in VARCHAR(20), in pol_in CHAR(1), in adresa_stanovanja_in VARCHAR(80), in telefon_in VARCHAR(20), in jmbg_in VARCHAR(13), in datum_rodjenja_in varchar(11))
BEGIN
	INSERT INTO studenti (ustanova, struka, broj_indeksa, prezime, ime_roditelja, ime, pol, adresa_stanovanja, telefon, jmbg, datum_rodjenja) VALUES (ustanova_in, struka_in, broj_indeksa_in, prezime_in, ime_roditelja_in, ime_in, pol_in, adresa_stanovanja_in, telefon_in, jmbg_in, STR_TO_DATE(datum_rodjenja_in, '%d-%m-%Y'));
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiStudenta(in ustanova_in CHAR(2), in struka_in CHAR(2), in broj_indeksa_in VARCHAR(6))
BEGIN
	DELETE FROM studenti WHERE studenti.ustanova = ustanova_in AND studenti.struka = struka_in AND studenti.broj_indeksa = broj_indeksa_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniStudenta(in ustanova_in CHAR(2), in struka_in CHAR(2), in broj_indeksa_in VARCHAR(6), in prezime_in varchar(20), in ime_roditelja_in VARCHAR(20), in ime_in VARCHAR(20), in pol_in CHAR(1), in adresa_stanovanja_in VARCHAR(80), in telefon_in VARCHAR(20), in jmbg_in VARCHAR(13), in datum_rodjenja_in DATE)
BEGIN
	UPDATE studenti SET studenti.prezime = prezime_in, studenti.ime_roditelja = ime_roditelja_in, studenti.ime = ime_in, studenti.pol = pol_in, studenti.adresa_stanovanja = adresa_stanovanja_in, studenti.telefon = telefon_in, studenti.jmbg = jmbg_in, studenti.datum_rodjenja = datum_rodjenja_in WHERE studenti.ustanova = ustanova_in AND studenti.struka = struka_in AND studenti.broj_indeksa = broj_indeksa_in;
END \
DELIMITER ;

-- CALL DobaviStudente();
-- CALL IzmeniStudenta("1", "1", "1", "markovic", "petar", "marko", "m", "nema", "234456", "1234567", "2020-05-21");
-- CALL DodajStudenta("1", "1", "11", "markovic", "petar", "marko", "m", "nema", "234456", "1234567", "05-10-2001");
-- CALL IzbrisiStudenta("1", "1", "11");






DROP PROCEDURE IF EXISTS DobaviTokStudija;
DROP PROCEDURE IF EXISTS DodajTokStudija;
DROP PROCEDURE IF EXISTS IzbrisiTokStudija;
DROP PROCEDURE IF EXISTS IzmeniTokStudija;

DELIMITER \
CREATE PROCEDURE DobaviTokStudija()
BEGIN
	select * FROM tok_studija;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE DodajTokStudija(in ustanova_in CHAR(2), in oznaka_programa_in VARCHAR(3), in student_iz_ustanove_in CHAR(2), in struka_in char(2), in broj_indeksa_in VARCHAR(6), in skolska_godina_in INT, in godina_studija_in INT, in blok_in INT, in redni_broj_upisa_in INT, in datum_upisa_in VARCHAR(11), in datum_overe_in VARCHAR(11), in espb_pocetni_in INT, in espb_krajnji_in INT)
BEGIN
	INSERT INTO tok_studija (ustanova, oznaka_programa, student_iz_ustanove, struka, broj_indeksa, skolska_godina, godina_studija, blok, redni_broj_upisa, datum_upisa, datum_overe, espb_pocetni, espb_krajnji) VALUES (ustanova_in, oznaka_programa_in, student_iz_ustanove_in, struka_in, broj_indeksa_in, skolska_godina_in, godina_studija_in, blok_in, redni_broj_upisa_in, STR_TO_DATE(datum_upisa_in, '%d-%m-%Y'), STR_TO_DATE(datum_overe_in, '%d-%m-%Y'), espb_pocetni_in, espb_krajnji_in);
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzbrisiTokStudija(in ustanova_in CHAR(2), in oznaka_programa_in VARCHAR(3), in student_iz_ustanove_in CHAR(2), in struka_in char(2), in broj_indeksa_in VARCHAR(6), in skolska_godina_in INT, in godina_studija_in INT, in blok_in INT, in redni_broj_upisa_in INT)
BEGIN
	DELETE FROM tok_studija WHERE tok_studija.ustanova = ustanova_in AND tok_studija.oznaka_programa = oznaka_programa_in AND tok_studija.student_iz_ustanove = student_iz_ustanove_in AND tok_studija.struka = struka_in AND tok_studija.broj_indeksa = broj_indeksa_in AND tok_studija.skolska_godina = skolska_godina_in AND tok_studija.godina_studija = godina_studija_in AND tok_studija.blok = blok_in AND tok_studija.redni_broj_upisa = redni_broj_upisa_in;
END \
DELIMITER ;

DELIMITER \
CREATE PROCEDURE IzmeniTokStudija(in ustanova_in CHAR(2), in oznaka_programa_in VARCHAR(3), in student_iz_ustanove_in CHAR(2), in struka_in char(2), in broj_indeksa_in VARCHAR(6), in skolska_godina_in INT, in godina_studija_in INT, in blok_in INT, in redni_broj_upisa_in INT, in datum_upisa_in DATE, in datum_overe_in DATE, in espb_pocetni_in INT, in espb_krajnji_in INT)
BEGIN
	UPDATE tok_studija SET tok_studija.datum_upisa = datum_upisa_in, tok_studija.datum_overe = datum_overe_in, tok_studija.espb_pocetni = espb_pocetni_in, tok_studija.espb_krajnji = espb_krajnji_in WHERE tok_studija.ustanova = ustanova_in AND tok_studija.oznaka_programa = oznaka_programa_in AND tok_studija.student_iz_ustanove = student_iz_ustanove_in AND tok_studija.struka = struka_in AND tok_studija.broj_indeksa = broj_indeksa_in AND tok_studija.skolska_godina = skolska_godina_in AND tok_studija.godina_studija = godina_studija_in AND tok_studija.blok = blok_in AND tok_studija.redni_broj_upisa = redni_broj_upisa_in;
END \
DELIMITER ;

-- CALL DobaviTokStudija();
-- CALL IzmeniTokStudija("1", "1", "1", "1", "1", 0, 0, 0, 0, "2020-01-01", "2020-01-01", 2, 2);
-- CALL DodajTokStudija("1", "1", "1", "1", "1", 1, 1, 2, 2, "2020-01-01", "01-01-2000", 2, 2);
-- CALL IzbrisiTokStudija("1", "1", "1", "1", "1", 0, 0, 0, 0);



















