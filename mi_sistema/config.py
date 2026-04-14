import os

class Config:
    """Configuración base de la aplicación"""
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo local"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción (Railway)"""
    DEBUG = False

class TestingConfig(Config):
    """Configuración para pruebas"""
    DEBUG = True
    TESTING = True

# Seleccionar configuración según el entorno
env = os.getenv('FLASK_ENV', 'production')

if env == 'development':
    config = DevelopmentConfig()
elif env == 'testing':
    config = TestingConfig()
else:
    config = ProductionConfig()