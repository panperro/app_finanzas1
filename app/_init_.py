from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['UPLOAD_FOLDER'] = 'static/recibos'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registro de blueprints
    from .auth import auth_bp
    from .ingresos import ingresos_bp
    from .gastos import gastos_bp
    from .presupuestos import presupuestos_bp
    from .metas import metas_bp
    from .balance import balance_bp
    from .recomendaciones import recomendaciones_bp
    from .graficas import graficas_bp
    from .recibos import recibos_bp
    from .exportaciones import exportaciones_bp
    from .admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ingresos_bp)
    app.register_blueprint(gastos_bp)
    app.register_blueprint(presupuestos_bp)
    app.register_blueprint(metas_bp)
    app.register_blueprint(balance_bp)
    app.register_blueprint(recomendaciones_bp)
    app.register_blueprint(graficas_bp)
    app.register_blueprint(recibos_bp)
    app.register_blueprint(exportaciones_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app