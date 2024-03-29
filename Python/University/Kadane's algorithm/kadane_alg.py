#Antoni Strasz

#Korzystamy z algorytmu algorytmu Kadane aby rozwiązać zadanie w czsie O(n)
def max_sublist_sum(lista : list):
    #ustawiamy wartości początkowe na pierwszy element listy (bo na początku jest on największy)
    current_max = global_max = lista[0]
    #początkowe indeksy i,j oraz ilość o jaką będziemy się cofać w przypadku konieczności zapisania indeksów
    max_global_start = 0
    max_global_end = 0
    current_backing = 0
    for index, element in enumerate(lista[1:]):

        #jeśli element jest większy niż dotychczasowa suma to podmieniamy w przeciwnym razie to nie
        if element > current_max+element:
            current_backing = 0
            current_max = element
        else:
            current_max = current_max+element
            current_backing +=1

        #Jeśli obecna sekwencja jest większa niż maksymalna to zamieniamy
        if current_max > global_max:
            global_max = current_max

            #zapisujemy indeksy(trzeba dodać jeden bo z listy usuwamy pierwszy element)
            max_global_end = index + 1
            max_global_start = index + 1 - current_backing

    return (max_global_start,max_global_end)


l1 = [10,11,12]
l2 = [5, -6, -10, 6, -4, 5, 5, -7,6]
l3 = [-10,-10,-10]

x,y = max_sublist_sum(l1)
print(f"{x},{y}  | {l1[x:y+1]}")

x,y = max_sublist_sum(l2)
print(f"{x},{y}  | {l2[x:y+1]}")

x,y = max_sublist_sum(l3)
print(f"{x},{y}  | {l3[x:+1]}")
