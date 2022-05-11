from pika import BlockingConnection, ConnectionParameters
import json


def callback(ch, method, properties, body):
    msg = body.decode()
    gameState = json.loads(msg)
    # print(f"Received: {msg}")
    
    if opcja == '1':
        print('Gracz X')
    elif opcja == '2':
        print('Gracz O')

    print(gameState['planszaCon'])
    player = '1' if gameState['gracz_1'] else '2'\

    if gameState['wygrana'] == True:
        print(gameState['kto_wygral'])
        ch.basic_publish(exchange="client_message",
                         routing_key="",
                         body='END')
        ch.stop_consuming()
        return
    if(player != opcja):
        return

    while True:
        try:
            message = int(input("Podaj wiersz: (0-6):"))
        except Exception as e:
            print("Nieprawidlowe dane")
            continue
        if(message >= 0 and message <= 6):
            break
        print("Nieprawidłowy wiersz!")

    message = str(message)
    channel.basic_publish(exchange="client_message",
                          routing_key="",
                          body=message)
    print(f"Sending: {message}")

# -----------------------------------------------------------------------


print('Witaj w grze kółko i krzyżyk!')
opcja = input("Wybierz opcje (1,2): ")
connection = BlockingConnection(ConnectionParameters(host="localhost"))
q_name_1 = "queue1"
q_name_2 = "queue2"
channel = connection.channel()

# --- konfiguracja kanału odbierającego ---
channel.exchange_declare(exchange="server_message",
                         exchange_type="fanout")
result = channel.queue_declare(queue="",
                               exclusive=True,
                               durable=True)
q_name = result.method.queue
channel.queue_bind(exchange="server_message", queue=q_name)
# -----------------------------------------

# --- konfiguracja kanału wysyłającego ---
channel.exchange_declare(exchange="client_message",
                         exchange_type="fanout")
result = channel.queue_declare(queue=q_name_2,
                               durable=True)
channel.queue_bind(exchange="client_message",
                   queue=q_name_2)
# ----------------------------------------

# Odbieranie wiadomości
channel.basic_consume(queue=q_name,
                      on_message_callback=callback,
                      auto_ack=True)
channel.start_consuming()
connection.close()
