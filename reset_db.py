from mi_sistema import create_app, db
import os

app = create_app()
with app.app_context():
    # Aseguramos que la carpeta instance exista
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    print("Creando base de datos desde cero...")
    db.create_all()
    print("\n--- ESTRUCTURA RECREADA CON ÉXITO ---")
    print("El archivo instance/sistema.db ya está listo y limpio.")
