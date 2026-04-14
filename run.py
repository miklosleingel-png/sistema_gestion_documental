from mi_sistema import create_app, db
from mi_sistema.config import config
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # db.create_all() # Descomenta solo la primera vez para crear las tablas
        pass
    
    # En desarrollo local, usa debug=True
    # En Railway (producción), usa debug=False automáticamente
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)