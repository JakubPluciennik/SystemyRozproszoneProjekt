https://github.com/JakubPluciennik/SystemyRozproszoneProjekt

Projekt na systemy rozproszone
Stworzyliśmy grę Connect4 za pomocą RabbitMQ i pygame (pygame używane jest tylko do generowania grafiki.) 
OPIS:
    1. W RabbitMQ tworzone jest exchange 'main_exchange', a w niej kolejka 'main_queue' przez którą wysyłany jest 
    kod wygenerowany przez klienta tworzącego sesję, kod jest jednoznaczy z ID sesji.
    Exchange i kolejka nie są usuwane.

    2. Po dołączeniu obydwu klientów do sesji tworzone są 2 exchange: 'server_message.SESSION_ID' oraz 'client_message.SESSION_ID'.
    Exchange 'server_message' jest typu fanout, klienci otrzymują z niego stan rundy w formacie JSON utworzony na serwerze.
    Nazwy kolejek tworzone są automatycznie i są różne dla każdego klienta
    'client_message' służy do wysyłania poprawnego numeru kolumny przez klientów do serwera. Kolejka ma nazwę 'queue2.SESSION_ID'.
    Wszystkie kolejki tworzone podczas sesji są automatycznie usuwane po upływie 1 godziny.
    Serwer odbiera z 'client_message' numer kolumny, którą wybrał odpowiedni gracz. Po otrzymaniu wiadomości wysyła kolejny stan gry.

Program porzebuje pakietów:
    numpy
    pygame
    pika
    
SERWER:
    Serwer uruchamiany plikiem 'Server/multithreading_server.py' (z konsoli).

GRA:
    Konsola:
        Klienci uruchamiają grę plikiem 'Client/Konsola/clientConsole.py' (z konsoli). Po uruchomieniu widoczne są opcje:
        1 - stworzenie sesji - Program generuje 4-cyfrową liczbę losową, i wysyłana jest ona na serwer. Jeśli nie ma jej
        w zbiorze ID, to jest tam dodawana, jeśli jest w zbiorze to jest usuwana i tworzona jest sesja w osobym wątku.
        2 - dołączenie do sesji - Program prosi o podanie 4-cyfrowej liczby, potem wysyła ją na serwer, i jeśli jest
        ona w zbiorze ID, to jest ona usuwana i generowana jest sesja w osobnym wątku, jeśli nie ma takiego ID to dodawane jest do zbioru.
        0 - wychodzi z programu.
        Po rozpoczęciu rozgrywki gracz wybierający opcję 1 gra 'X', gracz dołączający gra 'O'. W każdej rundzie wysyłana jest plansza z serwera
        oraz odpowiednia zmienna, która mówi kogo jest kolej.
        Po zakończeniu gry można zagrać ponownie lub wyjść z programu.

    GUI:
        Klienci uruchamiają grę plikiem 'Client/GUI/clientGUI.py' (z konsoli). Gra uruchamiana jest w oknie graficznym. Do wyboru są 3 opcje:
        'Utwórz sesję' - Program generuje 4-cyfrową liczbę losową, i oczekuje na wciśnięcie przycisku 'Oczekuj'. W tym momencie można 
        podać numer sesji rywalowi. Po wciśnięciu 'Oczekuj' program wysyła cyfrę na serwer. Jeśli nie ma jej w zbiorze ID, to jest tam 
        dodawana, jeśli jest w zbiorze to jest usuwana i tworzona jest sesja w osobym wątku.
        'Dołącz do sesji' - Program prosi o podanie 4-cyfrowej liczby, potem wysyła ją na serwer, i jeśli jest ona w zbiorze ID, to jest 
        ona usuwana i generowana jest sesja w osobnym wątku, jeśli nie ma takiego ID to dodawane jest do zbioru.
        'Wyjdź z gry' - wychodzi z programu.
        Po rozpoczęciu rozgrywki gracz tworzący sesję ma kolor czerwony, gracz dołączający ma kolor żółty.