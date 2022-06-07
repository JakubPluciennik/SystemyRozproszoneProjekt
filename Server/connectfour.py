# -*- coding: utf-8 -*-

import numpy as np
import json
from rabbitmq_server import server_message
from time import sleep

class ConnectFour:
    def __init__(self, gracz_1, planszaCon, wygrana, kto_wygral, plansza):
        self.gracz_1 = gracz_1
        self.planszaCon = planszaCon
        self.wygrana = wygrana
        self.kto_wygral = kto_wygral
        self.plansza = plansza

def wstaw_do_planszy(numer_kolumny, plansza, pomocniczaTablica, czy_gracz_jeden):
    tmp = pomocniczaTablica[int(numer_kolumny)]
    if(tmp < 0):
        print("Podana kolumna jest juz pełna!")
        return True  # To jest po to żeby gracz nie tracił ruchu jesli poda zla kolumne

    if(czy_gracz_jeden):
        plansza[int(tmp), int(numer_kolumny)] = 5  # To X
    else:
        plansza[int(tmp), int(numer_kolumny)] = 7  # To O

    pomocniczaTablica[int(numer_kolumny)] -= 1
    return

def wypisz_plansze(plansza):
    planszaCon = ""
    #print(" 0 1 2 3 4 5 6")
    planszaCon += " 0 1 2 3 4 5 6 \n"
    # print("----------------")
    for nr_wiersza in range(6):
        linia = "|"
        for nr_kolumny in range(7):
            tmp = plansza[int(nr_wiersza), int(nr_kolumny)]
            if(tmp == 0):
                linia += " |"
            elif(tmp == 5):
                linia += "X|"
            else:
                linia += "O|"
        # print(linia)
        planszaCon += linia + "\n"
        # print(linia+"|")
    # print("----------------")
    #print(" 0 1 2 3 4 5 6")
    planszaCon += " 0 1 2 3 4 5 6"

    # print(planszaCon)
    return planszaCon

def sprawdz_remis(plansza):
    if 0.0 in plansza: 
        return False
    return True

def czy_gracz_wygral(plansza, numer_kolumny, numer_wiersza):
    result = sprawdz_kolumne(plansza, numer_kolumny) or sprawdz_wiersz(plansza, numer_wiersza) or sprawdz_skos1(
        plansza, numer_kolumny, numer_wiersza) or sprawdz_skos2(plansza, numer_kolumny, numer_wiersza) or sprawdz_remis(plansza)
    return result

def sprawdz_kolumne(plansza, numer_kolumny):
    licznik = 0
    czy_poprzednio_X = True  # 5
    for indeks in range(6):

        if(plansza[indeks, int(numer_kolumny)] == 5 and czy_poprzednio_X):
            licznik += 1
        elif(plansza[indeks, int(numer_kolumny)] == 5):
            czy_poprzednio_X = True
            licznik = 1
        elif(plansza[indeks, int(numer_kolumny)] == 7):
            if(czy_poprzednio_X):
                czy_poprzednio_X = False
                licznik = 1
            else:
                licznik += 1
        else:
            licznik = 0

        if(licznik == 4):
            print("Wygrana kolumnowa")
            return True
    return False

def sprawdz_wiersz(plansza, numer_wiersza):
    licznik = 0
    czy_poprzednio_X = True  # 5
    for indeks in range(7):

        if(plansza[int(numer_wiersza), indeks] == 5 and czy_poprzednio_X):
            licznik += 1
        elif(plansza[int(numer_wiersza), indeks] == 5):
            czy_poprzednio_X = True
            licznik = 1
        elif(plansza[int(numer_wiersza), indeks] == 7):
            if(czy_poprzednio_X):
                czy_poprzednio_X = False
                licznik = 1
            else:
                licznik += 1
        else:
            licznik = 0

        if(licznik == 4):
            print("Wygrana wierszowa")
            return True

    return False

def sprawdz_skos1(plansza, numer_kolumny, numer_wiersza):
    B = int(numer_wiersza) - int(numer_kolumny)
    napis = ""
    for i in range(7):
        y = i + B
        if(y < 0 or y > 5):
            continue
        napis += str(plansza[y, i])+" "
    wynik = ("5.0 5.0 5.0 5.0" in napis) or ("7.0 7.0 7.0 7.0" in napis)

    return wynik

def sprawdz_skos2(plansza, numer_kolumny, numer_wiersza):
    B = int(numer_wiersza) + int(numer_kolumny)
    napis = ""
    for i in range(7):
        y = -i + B
        if(y < 0 or y > 5):
            continue
        napis += str(plansza[y, i])+" "
    wynik = ("5.0 5.0 5.0 5.0" in napis) or ("7.0 7.0 7.0 7.0" in napis)

    return wynik

def gameLoop(id):
    # Zaczęcie rundy po dołączeniu graczy
    sleep(1)    # Czekanie 1 sekundy na dołączenie graczy
    plansza = np.zeros((6, 7))  # inicjalizacja planszy
    pomocniczaTablica = 5*np.ones(7)  # tabel pomocnicza

    # Testowanie
    #wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
    #wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
    #wstaw_do_planszy(4, plansza, pomocniczaTablica, False)
    #wstaw_do_planszy(4, plansza, pomocniczaTablica, True)
    # print(plansza)
    # wypisz_plansze(plansza)

    czy_gracz_jeden = True  # X
    while(True):  # Pętla gry

        # Wypisanie planszy, wyświetlenie kto gra
        """
        print(wypisz_plansze(plansza))
        if(czy_gracz_jeden):
            print("\tGracza X")
        else:
            print("\tGracza O")
        """
        # Wysłanie stanu gry do klienta, zwracany indeks kolumny
        planszaCon = wypisz_plansze(plansza)
        gameState = ConnectFour(czy_gracz_jeden, planszaCon, False, "", plansza.tolist())
        json_gameState = json.dumps(gameState.__dict__)

        # kolumna = input()   #Wprowadzenie kolumny

        while True:
            try:
                kolumna = server_message(json_gameState, id)  # zwracana kolumna
            except Exception as e:
                print("Nieprawidlowe dane")
                continue
            if(int(kolumna) >= 0 and int(kolumna) <= 6):
                break
            print("Nieprawidłowy wiersz!")

        # Wstawianie i sprawdzanie czy podana kolumna nie jest juz pelna
        if(wstaw_do_planszy(int(kolumna), plansza, pomocniczaTablica, czy_gracz_jeden)):
            continue

        numer_wiersza = pomocniczaTablica[int(kolumna)] + 1
        if(czy_gracz_wygral(plansza, kolumna, numer_wiersza)):
            gameState = ConnectFour(czy_gracz_jeden, planszaCon, True, "", plansza.tolist())
            print("KONIEC GRY")
            if(sprawdz_remis(plansza)): 
                gameState.kto_wygral = "Remis"
            else: 
                if(czy_gracz_jeden):
                    print("Wygrał gracz X")
                    gameState.kto_wygral = "1"
                else:
                    print("Wygrał gracz O")
                    gameState.kto_wygral = "2"
                
            json_gameState = json.dumps(gameState.__dict__)
            server_message(json_gameState, id)
            print(f"Ending session: {id}")
            return

        czy_gracz_jeden = not czy_gracz_jeden
    
