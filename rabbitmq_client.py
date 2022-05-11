from pika import BlockingConnection, ConnectionParameters

global opcja
def callback(ch, method, properties, body):
    msg = body.decode()
    print(f"Received: {msg}")
    if(msg != opcja):
        return
    message = input()

    channel_send.basic_publish(exchange="client_message",
                               routing_key="",
                               body=message)
    print(f"Sending: {message}")

#-----------------------------------------------------------------------

opcja = input("Wybierz opcje (1, 2): ")
connection = BlockingConnection(ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="server_message",
                         exchange_type="fanout",
                          auto_delete=True)
result = channel.queue_declare(queue="", exclusive=True)
q_name = result.method.queue
channel.queue_bind(exchange="server_message", queue=q_name)

channel_send = connection.channel()
channel_send.exchange_declare(exchange="client_message",
                              exchange_type="fanout",
                              auto_delete=True)

channel.basic_consume(queue=q_name,
                      on_message_callback=callback,
                      auto_ack=True)
channel.start_consuming()
connection.close()
