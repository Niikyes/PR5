# Etapa 1: Construcción
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt /app/
COPY users_service.py /app/

RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY users_service.py /app/

ENV PYTHONPATH=/app/deps
EXPOSE 8000

# 🚀 Aquí arrancamos el servidor en vez de terminar el script
CMD ["uvicorn", "users_service:app", "--host", "0.0.0.0", "--port", "8000"]




