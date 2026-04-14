from mi_sistema import create_app, db

# Creamos la instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Este bloque asegura que las tablas se creen si no existen 
    # (Útil para pruebas locales rápidas)
    with app.app_context():
        # db.create_all() # Descomenta esta línea solo la primera vez para crear las tablas localmente
        pass

    # Ejecución en modo depuración para ver errores en tiempo real
    # El puerto 8080 es el estándar que espera Google Cloud Run
    app.run(host='0.0.0.0', port=8080, debug=False)