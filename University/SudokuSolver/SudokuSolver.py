#Antoni Strasz Zad7 (Sudoku Solver)
import itertools


#Pomocnicza funkcja "spłaszczająca" listę
def flatten(l: list):
    return [elem for subl in l for elem in subl]


#Pomocnicza funkcja znajdująca wszystkike puste pozycje
def find_empty(sudoku: list) -> list:
    return [(i,j) for i,e1 in enumerate(sudoku) for j,e2 in enumerate(e1) if e2 is None]


#Pomocnicza funkcja zwracająca nową planszę sudoku z pozycjami wypełnionymi na podstawnie podanego słownika
def fill_sudoku(sudoku : list, val_dict : dict):
    return [ [val_dict[(i,j)] if elem is None else elem for j,elem in enumerate(row)] for i,row in enumerate(sudoku) ]



#Sprawdzamy czy w podanym zbiorze 9 liczb nie ma powtórki
def check_sudoku_list(l: list):
    return sum(set(l))== sum(l)


#Wypełnione sudoku -> True jeśli poprawne wpp False
def check_sudoku(sudoku : list):
    #Sprawdzamy warunek dla wierszy
    if not all([check_sudoku_list(l=i) for i in sudoku]):
        return False
    #"Odpakowujemy" sudoku po czym używamy zipa na rzędach przez co zamieniamy rzędy i kolumny
    roteted_sudoku_board = list(zip(*sudoku))
    #Sprawdzamy warunek dla kolumn
    if not all([check_sudoku_list(l=i) for i in roteted_sudoku_board]):
        return False
    #Sprawdzamy warunek dla każdego z kwadratów
    for row_index in range(0,7,3):
        for elem_index in range(0,7,3):
            square = [sudoku[i+row_index][elem_index:elem_index+3] for i in range(3)]
            if not check_sudoku_list(l=flatten(square)):
                return False
    return True






#Głowna funkcja rozwiązująca sudoku
#Nierozwiązane sudoku -> Rozwiązane sudoku lub None jeśli go nie ma
def rozwiązanie_sudoku(sudoku : list):
    empty_fields = find_empty(sudoku=sudoku)
    #Tworzymy generator, aby nie tworzyć niepotrzebnych nieużytków
    values_generator = itertools.product(range(1,10), repeat=len(empty_fields))
    for val in values_generator:
        #Tworzymy nowy słownik gdzie kluczami są wolne pola a wartościami wygenerowane liczby (1-9)
        val_dict = dict(zip(empty_fields,val))
        filled_sudoku = fill_sudoku(sudoku=sudoku,val_dict=val_dict)
        if check_sudoku(sudoku=filled_sudoku):
            return filled_sudoku
    return None





def print_sudoku(sudoku):
    for i in range(9):
        if i in [3,6]:
            print("------@-------@--------")
        for j in range(9):
            if j in [3,6]:
                print("|", end=" "),
            print(sudoku[i][j],end=" ")
        print()


x = None

sudoku = [[5, 3, x, 6, 7, 8, 9, 1, 2],
          [6, 7, 2, 1, 9, 5, x, 4, 8],
          [1, 9, 8, 3, 4, 2, 5, 6, 7],
          [8, 5, 9, 7, 6, 1, 4, 2, 3],
          [4, 2, x, 8, 5, 3, 7, 9, 1],
          [7, 1, 3, 9, 2, 4, 8, 5, 6],
          [9, 6, 1, 5, 3, 7, x, 8, 4],
          [2, 8, 7, x, 1, 9, 6, 3, 5],
          [3, x, 5, 2, 8, 6, 1, 7, 9]]


print_sudoku(rozwiązanie_sudoku(sudoku))





