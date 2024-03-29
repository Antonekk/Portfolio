
def DHondt(glosy, miejsca):
    #tworzymy listę miejsc które dostanie partia
    liczba_miejsc = [0 for i in range(len(glosy))]

    #sprawdzamy czy partia przekroczyła próg
    all_votes = sum(glosy)
    glosy = [ 0 if i < all_votes * 0.05 else i for i in glosy]

    #do czasu aż są miejsca do rozdysponowania wykonujemy
    while miejsca != 0:
        #sprawdzamy wynik zależny od liczby miejsc już zajętej
        obecne_wyniki = [glosy[i]/(j+1) for i,j in enumerate(liczba_miejsc) ]
        #Wybieramy wygranego dla kolejnego miejsca
        wygrany = obecne_wyniki.index(max(obecne_wyniki))
        liczba_miejsc[wygrany] += 1
        miejsca-=1
    return liczba_miejsc

print(DHondt([720,300,480],8))


