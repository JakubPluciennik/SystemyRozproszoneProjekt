from pika import BlockingConnection, ConnectionParameters
from random import randint
import json
from rabbitmq_client import client_loop

# wybranie opcji 1, gracz zaczyna rozgrywkę,
#  generowane id sesji i wysyłane do serwera,
#  który tworzy exchange i queue z tym id


def graczX():
    # id jest losową liczbą z zakresu 1000-9999
    id = randint(1000, 9999)
    print(f"Tworzenie nowej sesji, ID sesji: {id}")
    gracz = 1
    message = {
        "id": id,
        "gracz": gracz
    }
    id = str(id)
    # konwertowanie wiadomości do JSON
    message = json.dumps(message)
    # wysłanie wiadomości do kolejki
    channel.basic_publish(exchange="main_exchange",
                          routing_key="",
                          body=message)
    print('Rozpoczęcie gry')
    client_loop(id, gracz)


def graczO():
    # wpisanie liczby z zakresu 1000-9999
    while True:
        try:
            id = int(input("Podaj ID sesji (1000 - 9999): "))
        except Exception as e:
            print("Nieprawidlowe dane")
            continue
        if(id >= 1000 and id <= 9999):
            break
        print("Nieprawidłowy zakres!")
    gracz = 2
    message = {
        "id": id,
        "gracz": gracz
    }
    id = str(id)
    # konwertowanie wiadomości do JSON
    message = json.dumps(message)
    # wysłanie wiadomości do kolejki
    channel.basic_publish(exchange="main_exchange",
                          routing_key="",
                          body=message)
    print('Rozpoczęcie gry')
    client_loop(id, gracz)


stan = True
while stan:
    stan = not stan
    host = "localhost"    # Hostname
    connection = BlockingConnection(ConnectionParameters(host))
    channel = connection.channel()
    q_name = "main_queue"
    # --- konfiguracja kanału odbierającego ---
    channel.exchange_declare(exchange="main_exchange",
                             exchange_type="fanout")
    result = channel.queue_declare(queue=q_name,
                                   durable=True)
    channel.queue_bind(exchange="main_exchange", queue=q_name)

    print('Witaj!')
    print('Gra w kółko i krzyżyk')
    print('Wpisz "1" jeśli chcesz stworzyć nową sesję')
    print('Wpisz "2" jeśli chcesz dołączyć do istniejącej sesji')
    print('Wpisz "0" jeśli chcesz zakończyć działanie programu')

    opcja = input('Wybierz opcję: ')

    match opcja:
        case '1':
            graczX()
        case '2':
            graczO()
        case '0':
            print('Wybrałeś opcję 0, zakończenie działania programu')
            stan = False
            break

    channel.close()
    connection.close()

    print('Gra zakończona')
    print('1. Zagraj ponownie')
    print('2. Wyjdź')
    opcja2 = input('Wybierz opcję: ')

    match opcja2:
        case '1':
            stan = True
        case '2':
            stan = False
