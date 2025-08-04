import pika
import os
import json
import time

rabbit_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

def get_connection():
    for attempt in range(10):  # hasta 10 intentos
        try:
            print(f"🔧 Intento {attempt+1}/10: conectando a RabbitMQ en {rabbit_host}...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
            print("Conexión exitosa a RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"RabbitMQ no disponible: {e}. Reintentando en 5s...")
            time.sleep(5)
    raise Exception("No se pudo conectar a RabbitMQ después de 10 intentos")

# Conectar y consumir
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue="notifications")

def callback(ch, method, properties, body):
    user = json.loads(body)
    print(f"[Notifications Service] Enviando notificación a: {user['email']}")

print("[Notifications Service] Esperando mensajes...")
channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)
channel.start_consuming()


