# Etapa 1: Construcción
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt /app/
COPY users_service.py /app/

# Instala dependencias en una carpeta aislada dentro de /app
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias y el código de la app
COPY --from=builder /app/deps /app/deps
COPY users_service.py /app/

# Configurar PYTHONPATH para que use las dependencias instaladas
ENV PYTHONPATH=/app/deps
EXPOSE 8000
ENV PORT=8000

# Ejecutar uvicorn desde el entorno configurado
CMD ["python", "-m", "uvicorn", "users_service:app", "--host", "0.0.0.0", "--port", "8000"]





