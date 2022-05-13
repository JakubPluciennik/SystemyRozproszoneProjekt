from email import message
from pika import BlockingConnection, ConnectionParameters

def callback(ch, method, properties, body):
    msg = body.decode()
    global message_global
    message_global = msg
    print(f"Received: {msg}")
    ch.stop_consuming()  # Zatrzymaj odbieranie wiadomości


def server_message(json_data, id):  # Wysyłanie wiadomości do klienta i odbieranie odpowiedzi
    message = json_data

    connection = BlockingConnection(ConnectionParameters(host="localhost"))
    q_name_send = "queue1." + id
    q_name_receive = "queue2." + id
    channel = connection.channel()

    # --- konfiguracja kanału wysyłającego ---
    channel.exchange_declare(exchange="server_message."+id,
                             exchange_type="fanout",
                             durable=True,
                             auto_delete=True)
    """
    result_send = channel.queue_declare(queue=q_name_send,
                                        durable=True,
                                        )
    channel.queue_bind(exchange="server_message."+id,
                       queue=q_name_send)
    """
    # ----------------------------------------
    # Wysyłanie wiadomości
    channel.basic_publish(exchange="server_message."+id,
                          routing_key="",
                          body=message)
    print(f"Sending to: {id}")

    # --- konfiguracja kanału odbierającego ---
    channel.exchange_declare(exchange="client_message."+id,
                             exchange_type="fanout",
                             durable=True,
                             auto_delete=True)
    result_receive = channel.queue_declare(queue=q_name_receive,
                                           durable=True,
                                           arguments={"x-expires": 60*60*1000})
    channel.queue_bind(exchange="client_message."+id,
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
