# 1. Usamos una imagen ligera de Python 3.9
FROM python:3.9-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalamos las dependencias necesarias para PostgreSQL y compilación
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos el archivo de requerimientos e instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código de tu proyecto al contenedor
COPY . .

# 6. Exponemos el puerto que usará Cloud Run (8080 por defecto)
EXPOSE 8080

# 7. Ejecutamos la aplicación usando Gunicorn (servidor de producción)
# 'run:app' se refiere a tu archivo run.py y la variable app que contiene
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app