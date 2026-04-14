from mi_sistema import create_app, db
from mi_sistema.config import config
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del .env

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # db.create_all() # Descomenta esta línea solo la primera vez para crear las tablas localmente
        pass
    
    # En desarrollo local, usa debug=True
    # En Railway (producción), usa debug=False automáticamente
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
