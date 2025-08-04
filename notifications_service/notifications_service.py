import pika
import json

def callback(ch, method, properties, body):
    event = json.loads(body)
    if event["tipo"] == "nuevo_usuario":
        print(f"[Notifications Service] Enviando email de bienvenida a {event['datos']['email']}")

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="eventos")
channel.basic_consume(queue="eventos", on_message_callback=callback, auto_ack=True)

print("📩 [Notifications Service] Esperando eventos...")
channel.start_consuming()
