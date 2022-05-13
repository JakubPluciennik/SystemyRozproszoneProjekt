from re import L
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
    player = '1' if gameState['gracz_1'] else '2'

    if gameState['wygrana'] == True:
        print(gameState['kto_wygral'])
        message = "END"
        ch.basic_publish(exchange="client_message."+session_id,
                         routing_key="",
                         body=message)
        print(f"Sending: end message")
        ch.stop_consuming()
    else:
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
        ch.basic_publish(exchange="client_message."+session_id,
                         routing_key="",
                         body=message)
        print(f"Sending: {message}")


# -----------------------------------------------------------------------


def client_loop(id, gracz):
    global session_id
    session_id = id

    global opcja
    opcja = str(gracz)

    host = "localhost"    # Hostname
    connection = BlockingConnection(ConnectionParameters(host))
    channel = connection.channel()

    #q_name_1 = 'queue1.' + id
    q_name_2 = 'queue2.' + id
    # --- konfiguracja kanału odbierającego ---
    channel.exchange_declare(exchange="server_message." + id,
                             exchange_type="fanout",
                             durable=True,
                             auto_delete=True)
    result = channel.queue_declare(queue="",
                                   durable=True,
                                   exclusive=True,
                                   arguments={"x-expires": 60*60*1000})
    q_name_1 = result.method.queue
    channel.queue_bind(exchange="server_message." + id,
                       queue=q_name_1)
    # -----------------------------------------

    # --- konfiguracja kanału wysyłającego ---
    channel.exchange_declare(exchange="client_message." + id,
                             exchange_type="fanout",
                             durable=True,
                             auto_delete=True)
    result = channel.queue_declare(queue=q_name_2,
                                   durable=True,
                                   arguments={"x-expires": 60*60*1000})
    channel.queue_bind(exchange="client_message." + id,
                       queue=q_name_2)
    # ----------------------------------------

    # Odbieranie wiadomości
    channel.basic_consume(queue=q_name_1,
                          on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()
    connection.close()
