#Antoni Strasz - Zad2 Lista 5

import abc
import itertools


#Błąd w przypadku braku wartości zmiennej w słowniku
class BrakWartosciZmiennej(Exception):
    def __init__(self,message):
        super().__init__(f"Nie znaleziono warości zmiennej {message} w podanym słowniku")


#Błąd przy podaniu błędnego typu w konstruktorze
class ZlaFormula(Exception):
    def __init__(self,message):
        super().__init__(f"Podano typ {message[0]} | Oczekiwano : {message[1]}")


#Abstrakcyjna klasa formuła
class Formula(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def oblicz(self, zmienne : dict):
        pass

    @abc.abstractmethod
    def __str__(self):
        return "Formula"

    def __add__(self, val):
        return Or(self,val)

    def __mul__(self, val):
        return And(self, val)

    #Znajduje wszystkie zmienne w wyrazeniu
    # (Ważne) Wartości mogą się powtarzać
    @abc.abstractmethod
    def znajdz_zmienne(self):
        pass

    #sprawdza czy dla każdego wartościowania obliczona formuła zwraca prawdę
    def tautologia(self):
        zmienne = set(self.znajdz_zmienne())
        wartosciowania = itertools.product([True,False], repeat=len(zmienne))
        for wartosciowanie in wartosciowania:
            wartosci = dict(zip(zmienne,wartosciowanie))
            if not self.oblicz(wartosci):
                return False
        return True



    def uprosc(self):
        return self



#klasa stałej
class Stala(Formula):
    def __init__(self,wartosc: bool):
        if type(wartosc) is not bool:
            raise ZlaFormula((type(wartosc),bool))
        self.wartosc = wartosc


    def oblicz(self, zmienne : dict):
        return self.wartosc



    def __str__(self):
        return str(self.wartosc)



    def znajdz_zmienne(self):
        return []

#klasa zmiennej
class Zmienna(Formula):
    def __init__(self,nazwa: str):
        if type(nazwa) is not str:
            raise ZlaFormula((type(nazwa),str))
        self.nazwa = nazwa


    #sprawdza czy zmienna występuje w słowniku jeśli tak to zwraca jej wartość wpp podnosi błąd
    def oblicz(self, zmienne : dict):
        try:
            return zmienne[self.nazwa]
        except:
            raise BrakWartosciZmiennej(self.nazwa)


    def __str__(self):
        return self.nazwa



    def znajdz_zmienne(self):
        return [self.nazwa]


#Klasa dla koniunkcji
class And(Formula):
    def __init__(self,f1: Formula, f2: Formula):
        if not issubclass(type(f1),Formula):
            raise ZlaFormula((type(f1),Formula))
        if not issubclass(type(f2),Formula):
            raise ZlaFormula((type(f2),Formula))
        self.f1 = f1
        self.f2 = f2



    def oblicz(self, zmienne : dict):
        return self.f1.oblicz(zmienne=zmienne) and self.f2.oblicz(zmienne=zmienne)


    def __str__(self):
        return f"({self.f1} ∧ {self.f2})"




    #Upraszcza wyrażenie postaci  p ∧ false ≡ false
    def uprosc(self):
        f1_u = self.f1.uprosc()
        f2_u = self.f2.uprosc()
        if  type(f2_u) == Stala and f2_u.wartosc == False:
            return f2_u
        elif type(f1_u) == Stala and f1_u.wartosc == False:
            return f2_u
        else:
            return And(f1_u, f2_u)

    def znajdz_zmienne(self):
        return self.f1.znajdz_zmienne() + self.f2.znajdz_zmienne()


#Klasa dla alternatywy
class Or(Formula):
    def __init__(self,f1: Formula, f2: Formula):
        if not issubclass(type(f1),Formula):
            raise ZlaFormula((type(f1),Formula))
        if not issubclass(type(f2),Formula):
            raise ZlaFormula((type(f2),Formula))
        self.f1 = f1
        self.f2 = f2


    #TODO  DODAĆ WYJĄTEK
    def oblicz(self, zmienne : dict):
        return self.f1.oblicz(zmienne=zmienne) or self.f2.oblicz(zmienne=zmienne)


    def __str__(self):
        return f"({self.f1} ∨ {self.f2})"


    #Upraszcza wyrażenie postaci false ∨ p ≡ p
    def uprosc(self):
        f1_u = self.f1.uprosc()
        f2_u = self.f2.uprosc()
        if type(f1_u) == Stala and f1_u.wartosc == False:
            return self.f2.uprosc()
        elif type(f2_u) == Stala and f2_u.wartosc == False:
            return self.f1.uprosc()
        else:
            return Or(f1_u , f2_u)

    def znajdz_zmienne(self):
        return self.f1.znajdz_zmienne() + self.f2.znajdz_zmienne()


class Not(Formula):
    def __init__(self,f1: Formula,):
        if not issubclass(type(f1),Formula):
            raise ZlaFormula((type(f1),Formula))
        self.f1 = f1


    def oblicz(self, zmienne : dict):
        return not self.f1.oblicz(zmienne=zmienne)


    def __str__(self):
        return f"¬{self.f1}"

    #Upraszcza wyrażenie postaci ¬True/False
    def uprosc(self):
        f1_u = self.f1.uprosc()
        if type(f1_u) == Stala:
            f1_u.wartosc = not f1_u.wartosc
            return f1_u
        return Not(f1_u)

    def znajdz_zmienne(self):
        return self.f1.znajdz_zmienne()


print("--------------------Test1-----------------------")

test = Or(Zmienna("x"), And(Zmienna("y"), Stala(True)))
print(test)
print(f"x: False | y : True  |  Wynik : {test.oblicz({'y': True, 'x' : False})}")
print(f"Czy tautologia? {test.tautologia()}")
print()



print("--------------------Testy Tautologii-----------------------")

test_taut = Or(Zmienna("x"),  Stala(True))
print(test_taut)
print(f"Czy tautologia? {test_taut.tautologia()}")
print()



test_taut_not =  Not(And(Zmienna("x"),  Stala(False)))
print(test_taut_not)
print(f"Czy tautologia? {test_taut_not.tautologia()}")
print()


test_taut_not =  Not(Or(Zmienna("x"),  Stala(False)))
print(test_taut_not)
print(f"Czy tautologia? {test_taut_not.tautologia()}")
print()

test_taut_n = Or(Zmienna("x"), Not(Zmienna("x")))
print(test_taut_n)
print(f"Czy tautologia? {test_taut_n.tautologia()}")
print()




print("--------------------Testy operacji dodawania i mnożenia -----------------------")

test_add = Or(Zmienna("x"),  Stala(True)) + Not(Or(Zmienna("x"),  Stala(True)))
print(test_add)
print(f"x: False | y : True  |  Wynik : {test_add.oblicz({'x' : False})}")
print(f"Czy tautologia? {test_add.tautologia()}")
print()


test_mul = Or(Zmienna("x"),  Stala(True)) * Not(Or(Zmienna("x"),  Stala(True)))
print(test_mul)
print(f"x: False | y : True  |  Wynik : {test_mul.oblicz({'x' : False})}")
print(f"Czy tautologia? {test_mul.tautologia()}")
print()





print("--------------------Testy Uproszczń-----------------------")

test_uprosc_or = Or(Zmienna("x"),  Stala(False))
print(f"Przed uproszczeniem : {test_uprosc_or}")
test_uprosc_or = test_uprosc_or.uprosc()
print(f"Po uproszczeniu : {test_uprosc_or}")
print()

test_uprosc_and = Not(Or(And(Zmienna("x"),  Stala(False)), Zmienna("y")))
print(f"Przed uproszczeniem : {test_uprosc_and}")
test_uprosc_and = test_uprosc_and.uprosc()
print(f"Po uproszczeniu : {test_uprosc_and}")
print()


test_uprosc_and2 = Not(And(Or(Zmienna("x"),  Stala(False)), And(Zmienna("x"), Stala(False))))
print(f"Przed uproszczeniem : {test_uprosc_and2}")
test_uprosc_and2 = test_uprosc_and2.uprosc()
print(f"Po uproszczeniu : {test_uprosc_and2}")
print()






#Testy Błędów
print("--------------------Testy Błędów-----------------------")
test_exception = Or(Zmienna("x"), And(Zmienna("y"), Stala(True)))
print(test)
try:
    print(f"x: False | y : True  |  Wynik : {test.oblicz({ 'x' : False})}")
except BrakWartosciZmiennej as e:
    print(e)

print()

try:
    Stala("s")
except ZlaFormula as z:
    print(z)

try:
    Not(1)
except ZlaFormula as z:
    print(z)

try:
    And(Stala(True), Stala(False)) + 1
except ZlaFormula as z:
    print(z)












