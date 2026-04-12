from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '18brumario-seguridad')

    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        db_user = os.environ.get('DB_USER', 'postgres')
        db_pass = os.environ.get('DB_PASS', '')
        db_name = os.environ.get('DB_NAME', 'sistema_gestion_documental')
        db_host = os.environ.get('DB_HOST', '/cloudsql/gestion-documental-smadsot:us-central1:gestion-db-smadsot')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={db_host}/.s.PGSQL.5432'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'main.login'
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
