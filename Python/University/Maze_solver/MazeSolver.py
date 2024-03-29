#Antoni Strasz
from collections import deque

# Funkcja zwróci nam obiekt na pozycji index w liście l o ile pozycja ta istnieje wpp. zwraca None lub wybraną przy wywołaniu wartość
def get_item(l : list, index : int, default=None):
    if index < 0 or index > len(l) - 1:
        return default
    else:
        return l[index]

#zakładam poprawny labirynt ma wymiary n x m
#W opisie zadania nie było podane nic o identyfikacji wyjścia więc uznałem że wyjściem jest pole oznaczone literą 'W'
#Algorytm - BFS
def maze_solver(maze : list, cords : tuple):
    #lista możliwych kroków
    cords_options = [(-1,0),(0,-1),(0,1),(1,0)]

    # lista odwiedzonych pól
    visited = [cords]
    #drogi do odwiedzenia
    queue = deque()
    queue.append([cords])
    while len(queue) > 0:
        # path to dotychczasowa przebyta droga a current to obecne koordynaty
        path = queue.popleft()
        current = path[-1]
        #Sprawdzamy możliwe kroki
        for i in cords_options:
            #tworzymy nowe koordynaty i sprawdzamy czy krok jest wykonalny
            y,x = current[0]+i[0], current[1]+i[1]
            move_y = get_item(maze,y)
            if move_y != None:
                move_x = get_item(move_y, x)
                if move_x == ' ' and (y,x) not in visited:
                    #Jeśli krok znajduje sięw naszej tablicy, jest przestrzenią wolną oraz nie został jeszcze odwiedzony to dodajemy go do kolejki oraz do odwiedzonych
                    visited.append((y,x))
                    queue.append(path+[(y,x)])

                elif move_x == 'W':
                    #Jeśli znaleźliśmy wyjście to zwracamy przebytą drogę
                    path.append((y,x))
                    reversed(path)
                    return path
    #W przypadku braku drogi zwracamy None
    return None




maze1 = [['X','X','X','X',' ','X','X' ],
        ['X','X','X','X',' ','X','X' ],
        ['X','X',' ',' ',' ',' ','X' ],
        ['X',' ',' ','X','X',' ','X' ],
        ['X','X','X','W',' ',' ','X' ]
        ]

maze2 = [['X','X','X','X',' ','X','X' ],
        ['X','X','X','X',' ','X','X' ],
        ['X','X','X',' ',' ',' ','X' ],
        ['X',' ',' ',' ','X','X','X' ],
        ['X','X','X','W','X','X','X' ]
        ]

print(maze_solver(maze1,(0,4)))
print(maze_solver(maze2,(0,4)))


