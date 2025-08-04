import pika
import os
import json
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

# Establecer conexión y canal global
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue="notifications")

class User(BaseModel):
    nombre: str
    email: str

@app.post("/register")
def register_user(user: User):
    # Simular registro de usuario
    print(f"[Users Service] Usuario registrado: {user.dict()}")

    # Enviar mensaje a la cola
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(user.dict())
    )
    print(f"📨 Mensaje enviado a RabbitMQ: {user.email}")
    return {"message": "Usuario registrado y notificación enviada"}

