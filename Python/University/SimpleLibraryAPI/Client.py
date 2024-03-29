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
import DatabaseFunc as dbf

server = 'http://127.0.0.1:5000'


def main():
    session = dbf.inicjalizuj()
    parser = argparse.ArgumentParser(description="Biblioteka")
    parser.add_argument("access", choices=["api", "direct"], help="Wybierz sposób dostępu")
    parser.add_argument("operacja", choices=["dodaj_ksiazke", "dodaj_znajomego", "wypozycz_ksiazke", "oddaj_ksiazke", "wypisz_ksiazki", "wypisz_znajomych","wypisz_wypozyczenia", "aktualizuj_znajomego", "usun_znajomego"], help="Wybierz operację")
    parser.add_argument("--autor", help="Dane Autora Ksiazki", required=False)
    parser.add_argument("--tytul", help="Tytuł Książki", required=False)
    parser.add_argument("--rok", type=int, help="Rok wydania książki", required=False)
    parser.add_argument("--czas_wypozyczenia", type=int, help="Czas na jaki wyporzyczyć książkę", required=False)
    parser.add_argument("--imie", help="Imię znajomego", required=False)
    parser.add_argument("--nazwisko", help="Nazwisko znajomego", required=False)
    parser.add_argument("--email", help="Email znajomego", required=False)
    parser.add_argument("--znajomy_id", help="Id znajomego", required=False)


    args = parser.parse_args()

    if args.access == "direct":
        match args.operacja:
            case "dodaj_znajomego":
                dbf.dodaj_znajomego(session, args.imie, args.nazwisko, args.email)
            case "wypisz_znajomych":
                dbf.wyswietl_znajomych(session)
            case "wypisz_ksiazki":
                dbf.wyswietl_ksiazki(session)
            case "dodaj_ksiazke":
                dbf.dodaj_ksiazke(session, args.autor, args.tytul, args.rok)
            case "wypozycz_ksiazke":
                dbf.wypozycz_ksiazke(session, args.tytul, args.autor, args.email, args.czas_wypozyczenia)
            case "oddaj_ksiazke":
                dbf.oddaj_ksiazke(session, args.tytul, args.autor, args.email)
            case "wypisz_wypozyczenia":
                dbf.wypisz_wypozyczenia(session)
            case _:
                print("Operacja dostępna poprzez API")
    elif args.access == "api":
        match args.operacja:
            case "dodaj_znajomego":
                data = {'imie': args.imie, "nazwisko" : args.nazwisko, "email": args.email}
                resp = requests.post(server+"/api/users", json=data)
                print(resp.text)
            case "aktualizuj_znajomego":
                data = {'imie': args.imie, "nazwisko" : args.nazwisko, "email": args.email}
                resp = requests.put(server+"/api/users/"+args.znajomy_id, json=data)
                print(resp.text)
            case "usun_znajomego":
                resp = requests.delete(server+"/api/users/"+args.znajomy_id)
                print(resp.text)
            case "wypisz_znajomych":
                resp = requests.get(server+"/api/users")
                print(resp.text)
            case _:
                print("Operacja dostępna bezposrednio")


if __name__ == "__main__":
    main()
