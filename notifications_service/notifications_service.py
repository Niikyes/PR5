import pika
import os
import json
import time

# Leer host desde variable de entorno (default: rabbitmq)
rabbit_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

def get_connection():
    for attempt in range(5):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"[Notifications Service] RabbitMQ no disponible, reintentando ({attempt+1}/5)...")
            time.sleep(5)
    raise Exception("No se pudo conectar con RabbitMQ después de varios intentos")

def callback(ch, method, properties, body):
    user = json.loads(body)
    print(f"[Notifications Service] Enviando notificación a {user['email']}")

# Conectar y consumir mensajes
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue="notifications")
channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)

print("[Notifications Service] Esperando mensajes...")
channel.start_consuming()


