from fastapi import FastAPI
import pika
import os
import json
import time

app = FastAPI()

# Obtener host de RabbitMQ desde variable de entorno
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

@app.post("/register")
def register_user(user: dict):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="notifications")
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(user)
    )
    connection.close()
    print(f"[Users Service] Usuario registrado: {user}")
    return {"message": "Usuario registrado y evento enviado a RabbitMQ"}
