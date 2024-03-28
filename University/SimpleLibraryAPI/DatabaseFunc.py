#Antoni Strasz

from __future__ import annotations
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, ForeignKey,String, Boolean,create_engine
from sqlalchemy.orm import relationship, mapped_column,Mapped,sessionmaker
from sqlalchemy.orm import validates
import datetime
import re
import argparse
from typing import List
from sqlalchemy.inspection import inspect
import requests


from flask import Flask, request, jsonify





base = declarative_base()


class Ksiazka(base):
    __tablename__ = 'Ksiazki'

    id = mapped_column(Integer, primary_key=True)

    autor = mapped_column(String, nullable=False)
    tytul = mapped_column(String, nullable=False)
    rok_wydania = mapped_column(Integer, nullable=False)
    dostepna = mapped_column(Boolean, default=True)



    @validates("rok_wydania")
    def validate_rok_wydania(self, key, rok_wydania):
        if rok_wydania > datetime.date.today().year :
            raise ValueError("Nazwisko za krótkie")
        return rok_wydania

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    



class Znajomy(base):
    __tablename__ = 'Znajomi'

    id = mapped_column(Integer, primary_key=True)

    imie = mapped_column(String, nullable=False)
    nazwisko = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)

    wypozyczenia: Mapped[List[Wypozyczenie]] = relationship("Wypozyczenie", back_populates="znajomy")


    @validates("email")
    def validate_email(self, key, mail):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(email_pattern,mail) :
            raise ValueError("Nazwisko za krótkie")
        return mail

    @validates("imie")
    def validate_imie(self, key, imie):
        if len(imie) < 2:
            raise ValueError("Imie musi zawierać przynajmniej 2 znaki")
        return imie

    @validates("nazwisko")
    def validate_nazwisko(self, key, nazwisko):
        if len(nazwisko) < 2:
            raise ValueError("Nazwisko musi zawierać przynajmniej 2 znaki")
        return nazwisko

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


class Wypozyczenie(base):
    __tablename__ = 'Wypozyczenia'

    id = mapped_column(Integer, primary_key=True)

    #Początkowo zadeklarowany czas wypozyczenia książki zadeklarowany przez wypożyczającego
    czas_wypozyczenia = mapped_column(Integer, nullable=False)

    ksiazka_id = mapped_column(Integer, ForeignKey('Ksiazki.id'))
    ksiazka = relationship(Ksiazka, uselist=False)

    znajomy_id = mapped_column(Integer, ForeignKey('Znajomi.id'))
    znajomy = relationship("Znajomy", back_populates="wypozyczenia")

    @validates("czas_wypozyczenia")
    def validate_czas_wypozyczeniaa(self, key, czas_wypozyczenia):
        if czas_wypozyczenia <= 0:
            raise ValueError("Czas wypożyczenia musi wynosić przynajmniej 1 dzień")
        return czas_wypozyczenia

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}



def inicjalizuj():
    engine = create_engine('sqlite:///biblioteka.db', echo=True)
    base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def dodaj_znajomego(session, imie, nazwisko,email):
    if session.query(Znajomy).filter_by(imie=imie, nazwisko=nazwisko, email=email).first() is not None :
        print("Znajomy jest na liście")
        return False
    if session.query(Znajomy).filter_by(email=email).first() is not None:
        print("Email nie może się powtarzać")
        return False
    znajomy = Znajomy(imie=imie, nazwisko=nazwisko , email=email)
    session.add(znajomy)
    session.commit()
    print(f"Dodano {imie} {nazwisko} do bazy znajomych")
    return True



def wyswietl_znajomych(session):
    znajomi = session.query(Znajomy).all()
    if znajomi:
        print("Zarejestrowani Znajomi:")
        for znajomy in znajomi:
            print(f"{znajomy.imie} {znajomy.nazwisko} {znajomy.email}")
    else:
        print("Baza znajomych pusta")


def wyswietl_ksiazki(session):
    ksiazki = session.query(Ksiazka).all()
    if ksiazki:
        print("Zbior Ksiażek: ")
        for ksiazka in ksiazki:
            print(f"'{ksiazka.tytul}' autorstwa {ksiazka.autor}  wydana w {ksiazka.rok_wydania}")
    else:
        print("Baza Książek Pusta")


def dodaj_ksiazke(session, autor, tytul, rok):
    if session.query(Ksiazka).filter_by(tytul=tytul, autor=autor, rok_wydania=rok).first() is not None:
        print("Ksiazka jest na liście")
        return
    nowa_ksiazka = Ksiazka(autor=autor, tytul=tytul, rok_wydania=rok)
    session.add(nowa_ksiazka)
    session.commit()
    print(f"Dodano nową książkę: {tytul} autorstwa {autor} ({rok}r.)")


def wypozycz_ksiazke(session, tytul, autor, email, czas_wypozyczenia):
    ksiazka = session.query(Ksiazka).filter_by(tytul=tytul, autor=autor, dostepna=True).first()
    znajomy = session.query(Znajomy).filter_by(email=email).first()

    if ksiazka and znajomy:
        wypozyczenie = Wypozyczenie(ksiazka=ksiazka, znajomy=znajomy,czas_wypozyczenia=czas_wypozyczenia)
        ksiazka.dostepna = False
        session.add(wypozyczenie)
        session.commit()
        print(f"{znajomy.imie} wypożyczył(a) książkę: {tytul}")
    else:
        print("Coś poszło nie tak, nie udało się wypożyczyć :(")


def znajdz_wypozyczona_ksiazke(wypozyczenia, tytul, autor):
    for wypozyczenie in wypozyczenia:
        if wypozyczenie.ksiazka.tytul == tytul and wypozyczenie.ksiazka.autor == autor:
            return wypozyczenie.ksiazka
    return None


def oddaj_ksiazke(session, tytul, autor, email):
    znajomy = session.query(Znajomy).filter_by(email=email).first()
    if znajomy:
        ksiazka = znajdz_wypozyczona_ksiazke(znajomy.wypozyczenia,tytul=tytul,autor=autor)
        if ksiazka:
            wypozyczenie = session.query(Wypozyczenie).filter_by(ksiazka=ksiazka, znajomy=znajomy).first()
            ksiazka.dostepna = True
            session.delete(wypozyczenie)
            session.commit()
            print(f"{znajomy.imie} oddał(a) książkę: {tytul}")
        else:
            print("Coś poszło nie tak podczas szukania ksiażki :(")

    else:
        print("Coś poszło nie tak podczas wyszukiwania znajomego :(")


def wypisz_wypozyczenia(session):
    wypozyczenia = session.query(Wypozyczenie).all()
    if wypozyczenia:
        print("Lista Wypożyczeń: ")
        for wypozyczenie in wypozyczenia:
            print(f"'{wypozyczenie.ksiazka.tytul}' autorstwa {wypozyczenie.ksiazka.autor}  została wyporzyczona przez {wypozyczenie.znajomy.imie}")
    else:
        print("Rejestr wypożyczeń pusty")





