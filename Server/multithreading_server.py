from connectfour import gameLoop
from pika import BlockingConnection, ConnectionParameters
from threading import Thread
import json

def callback(ch, method, properties, body):
    #wykonuje się w momencie otrzymania wiadomosci
    #przy każdym wykonaniu otwiera nowy wątek
    msg = body.decode() # w msg kod 4-cyfrowy sesji gry
    #decode JSON
    sessionData = json.loads(msg)
    id = str(sessionData['id'])
    gracz = sessionData['gracz']

    # Jeśli nie ma ID w zbiorze to dodaje go. Jeśli jest, to jest usuwany i tworzona nowa sesja
    if id in ids:
        ids.remove(id)
        t = Thread(target=gameLoop, args=[id])
        t.start()
    else: 
        ids.add(id)
    

ids = set()
host = "localhost"    # Hostname
connection = BlockingConnection(ConnectionParameters(host,heartbeat=0))
channel = connection.channel()
q_name = "main_queue"
# --- konfiguracja kanału odbierającego ---
channel.exchange_declare(exchange="main_exchange",
                         exchange_type="fanout")
result = channel.queue_declare(queue=q_name,
                               durable=True)
channel.queue_bind(exchange="main_exchange", queue=q_name)
# -----------------------------------------


# Odbieranie wiadomości
channel.basic_consume(queue=q_name,
                      on_message_callback=callback,
                      auto_ack=True)
channel.start_consuming()
connection.close()
