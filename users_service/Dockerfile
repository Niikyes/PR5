# Etapa 1: Construcción
FROM python:3.11-slim AS builder

WORKDIR /app
COPY users_service.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Etapa 2: Imagen final (solo dependencias y código necesario)
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY users_service.py /app/

ENV PYTHONPATH=/app/deps
EXPOSE 8000

CMD ["python", "users_service.py"]


