import psycopg2

def conectar_bd():
    """
    Establece conexión con la base de datos PostgreSQL del Sistema de Gestión Documental.
    Retorna un objeto de conexión activo.
    """
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Sistema de Gestión Documental",
        user="postgres",
        password="18brumario"
    )