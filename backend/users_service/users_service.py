import pika
import os
import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

rabbit_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

def get_connection():
    for attempt in range(10):  # Up to 10 tries
        try:
            print(f"🔧 Intento {attempt+1}/10: conectando a RabbitMQ en {rabbit_host}...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
            print("Conexión exitosa a RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"RabbitMQ no disponible: {e}. Reintentando en 5s...")
            time.sleep(5)
    raise Exception("No se pudo conectar a RabbitMQ después de 10 intentos")

# Conection with RabbitMQ
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue="notifications")

# Temporal list memory
usuarios_registrados = []

class User(BaseModel):
    nombre: str
    email: str

@app.post("/register")
def register_user(user: User):
    """Registrar un usuario y enviarlo a RabbitMQ, además de guardarlo en memoria."""
    print(f"[Users Service] Usuario registrado: {user.dict()}")

    # Save users in memory
    usuarios_registrados.append(user.dict())

    # Publish messegae in RabbitMQ
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(user.dict())
    )
    print(f"📨 Mensaje enviado a RabbitMQ: {user.email}")
    return {"message": "Usuario registrado y notificación enviada", "usuarios": usuarios_registrados}

@app.get("/usuarios")
def obtener_usuarios():
    """Obtener la lista de usuarios registrados temporalmente en memoria."""
    return {"usuarios": usuarios_registrados}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
