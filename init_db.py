import os
from mi_sistema import create_app, db
from mi_sistema.models import Usuario, Rol
from werkzeug.security import generate_password_hash
from datetime import datetime

# URL para conexión manual desde Cloud Shell
os.environ['DATABASE_URL'] = "postgresql://postgres:18brumario@35.222.95.151/sistema_gestion_documental"

app = create_app()

def inicializar():
    with app.app_context():
        print("--- Iniciando Configuración SMADSOT ---")
        try:
            # 1. Limpieza Forzada (CASCADE)
            # Usamos SQL puro para ignorar las restricciones de llave foránea temporalmente
            print("Limpiando tablas con dependencias (CASCADE)...")
            db.session.execute(db.text("DROP TABLE IF EXISTS expedientes, cat_cgca, sesiones, usuario_areas, usuarios, roles CASCADE;"))
            db.session.commit()
            
            # 2. Recreación desde cero
            db.create_all()
            print("1. Tablas recreadas con la estructura correcta (incluyendo role_id).")

            # 3. Crear el Rol admin
            print("2. Creando rol 'admin'...")
            admin_role = Rol(
                nombre='admin', 
                descripcion='Administrador General del Sistema'
            )
            db.session.add(admin_role)
            db.session.commit() # Confirmamos el rol para obtener su ID

            # 4. Crear el Usuario 'postgres' vinculado al nuevo Rol
            print("3. Creando usuario 'postgres'...")
            nuevo_admin = Usuario(
                username='postgres',
                nombre_completo='Administrador del Sistema',
                correo='admin@smadsot.gob.mx',
                password=generate_password_hash('18brumario', method='pbkdf2:sha256'),
                role_id=admin_role.id, # Ahora sí encontrará la columna y el ID
                activo=True,
                creado_en=datetime.utcnow()
            )
            db.session.add(nuevo_admin)
            db.session.commit()

            print("--- Todo listo para el 18 Brumario ---")
            print("Acceso: https://sistema-smadsot-876383454438.us-central1.run.app")

        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {e}")

if __name__ == "__main__":
    inicializar()