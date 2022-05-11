from email import message
from pika import BlockingConnection, ConnectionParameters


def callback(ch, method, properties, body):
    msg = body.decode()
    global message_global
    message_global = msg
    print(f"Received: {msg}")
    ch.stop_consuming()  # Zatrzymaj odbieranie wiadomości

def server_message(json_data):  # Wysyłanie wiadomości do klienta i odbieranie odpowiedzi
    message = json_data
    print(f"Sending: {message}")

    connection = BlockingConnection(ConnectionParameters(host="localhost"))
    q_name_send = "queue1"
    q_name_receive = "queue2"
    channel = connection.channel()

    # --- konfiguracja kanału wysyłającego ---
    channel.exchange_declare(exchange="server_message",
                                  exchange_type="fanout")
    result_send = channel.queue_declare(queue=q_name_send,
                                             durable=True)
    channel.queue_bind(exchange="server_message",
                            queue=q_name_send)
    # ----------------------------------------
    # Wysyłanie wiadomości
    channel.basic_publish(exchange="server_message",
                               routing_key="",
                               body=message)

    # --- konfiguracja kanału odbierającego ---
    channel.exchange_declare(exchange="client_message",
                                     exchange_type="fanout")
    result_receive = channel.queue_declare(queue=q_name_receive,
                                                   durable=True)
    channel.queue_bind(exchange="client_message",
                               queue=q_name_receive)
    # -----------------------------------------

    # Odbieranie wiadomości
    channel.basic_consume(queue=q_name_receive,
                                  on_message_callback=callback,
                                  auto_ack=True)
    channel.start_consuming()
    channel.close()
    connection.close()
    return message_global
