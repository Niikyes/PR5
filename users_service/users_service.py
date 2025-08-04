from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- ESTE IMPORT ES NECESARIO
import pika
import json

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (en pruebas)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (POST, GET, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)

# Conexión a RabbitMQ
def publish_event(event_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="eventos")
    channel.basic_publish(exchange="", routing_key="eventos", body=json.dumps(event_data))
    connection.close()

@app.post("/register")
def register_user(user: dict):
    print(f"[Users Service] Usuario registrado: {user}")
    publish_event({"tipo": "nuevo_usuario", "datos": user})
    return {"mensaje": "Usuario registrado con éxito"}
