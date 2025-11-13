#config.py                   ← Configuración de conexión a PostgreSQL

# config.py
import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sistema de Gestión Documental",
        user="postgres",
        password="18 brumario"
    )
