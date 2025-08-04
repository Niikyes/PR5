import pika
import os
import json
import time

rabbit_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

# Conexión con reintentos
def get_connection():
    for attempt in range(5):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"Intento {attempt+1}/5: RabbitMQ no está disponible, reintentando...")
            time.sleep(5)
    raise Exception("No se pudo conectar con RabbitMQ después de 5 intentos")

def callback(ch, method, properties, body):
    user = json.loads(body)
    print(f"[Notifications Service] Enviando notificación a: {user['email']}")

# Conectar y consumir mensajes
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue="notifications")
channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)

print("[Notifications Service] Esperando mensajes...")
channel.start_consuming()
