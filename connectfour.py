# -*- coding: utf-8 -*-

import numpy as np

def wstaw_do_planszy(numer_kolumny,plansza,pomocniczaTablica,czy_gracz_jeden):
    tmp = pomocniczaTablica[int(numer_kolumny)]
    if(tmp<0):
        print("Podana kolumna jest juz pełna!")
        return True #To jest po to żeby gracz nie tracił ruchu jesli poda zla kolumne
    
    if(czy_gracz_jeden):
        plansza[int(tmp),int(numer_kolumny)] = 5 #To X
    else:
        plansza[int(tmp),int(numer_kolumny)] = 7 #To O
    
    pomocniczaTablica[int(numer_kolumny)] -=1;
    return

def wypisz_plansze(plansza):
    print(" 0 1 2 3 4 5 6")
    #print("----------------")
    for nr_wiersza in range(6):
        linia = "|"
        for nr_kolumny in range(7):
            tmp = plansza[int(nr_wiersza),int(nr_kolumny)]
            if(tmp == 0):
                linia+=" |"
            elif(tmp == 5):
                linia+="X|"
            else:
                linia+="O|"
        print(linia)
        #print(linia+"|")
    #print("----------------")
    print(" 0 1 2 3 4 5 6")
    return

def czy_gracz_wygral(plansza, numer_kolumny,numer_wiersza):
    result = sprawdz_kolumne(plansza, numer_kolumny) or sprawdz_wiersz(plansza,numer_wiersza)
    return result

def sprawdz_kolumne(plansza,numer_kolumny):
    licznik = 0;
    czy_poprzednio_X = True #5
    for indeks in range(6):
        
        
        if(plansza[indeks,int(numer_kolumny)]==5 and czy_poprzednio_X):
            licznik+=1
        elif(plansza[indeks,int(numer_kolumny)]==5):
            czy_poprzednio_X = True
            licznik = 1
        elif(plansza[indeks,int(numer_kolumny)]==7):
            if(czy_poprzednio_X):
                 czy_poprzednio_X = False
                 licznik = 1
            else:
                licznik +=1
        else:
            licznik =0
    
        if(licznik == 4):
            print("Wygrana kolumnowa")
            return True
    return False

def sprawdz_wiersz(plansza,numer_wiersza):
    licznik = 0;
    czy_poprzednio_X = True #5
    for indeks in range(7):
        
        if(plansza[int(numer_wiersza),indeks]==5 and czy_poprzednio_X):
            licznik+=1
        elif(plansza[int(numer_wiersza),indeks]==5):
            czy_poprzednio_X = True
            licznik = 1
        elif(plansza[int(numer_wiersza),indeks]==7):
            if(czy_poprzednio_X):
                czy_poprzednio_X = False
                licznik = 1
            else:
                licznik +=1
        else:
            licznik =0
    
        if(licznik == 4):
            print("Wygrana wierszowa")
            return True
        
    return False

def sprawdz_skos(plansza,numer_kolumny,numer_wiersza):
    
    
    
    return False



plansza = np.zeros((6,7)) #inicjalizacja planszy

pomocniczaTablica = 5*np.ones(7) #tabel pomocnicza

#Testowanie
#wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
#wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
#wstaw_do_planszy(4, plansza, pomocniczaTablica, False)
#wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
#print(plansza)
#wypisz_plansze(plansza)

czy_gracz_jeden = True #X
while(True): #Pętla gry
    wypisz_plansze(plansza)
    if(czy_gracz_jeden):
        print("\tGracza X")
    else:
        print("\tGracza O")
        
    kolumna = input()
    if(int(kolumna)<0 or int(kolumna)>6):
        print("Podano niepoprawny numer kolumny!")
        continue
    
    if(wstaw_do_planszy(int(kolumna), plansza, pomocniczaTablica,czy_gracz_jeden)): #Wstawianie i sprawdzanie czy podana kolumna nie jest juz pelna
        continue
    
    numer_wiersza = pomocniczaTablica[int(kolumna)] + 1
    if(czy_gracz_wygral(plansza, kolumna,numer_wiersza)):
        print("KONIEC GRY")
        if(czy_gracz_jeden):
            print("Wygrał gracz X")
        else:
            print("Wygrał gracz O")
        wypisz_plansze(plansza)
        break
    
    if(czy_gracz_jeden): #Zamiana gracza
        czy_gracz_jeden = False
    else:
        czy_gracz_jeden = True
    
 
