from flask import Flask
from flask_login import LoginManager
from app.models import db, Usuario

# Importar blueprints
from app.auth import auth_bp
from app.ingresos import ingresos_bp
from app.gastos import gastos_bp
from app.presupuestos import presupuestos_bp
from app.metas import metas_bp
from app.balance import balance_bp
from app.exportar import exportar_bp
from app.categorias import categorias_bp
from app.proyecciones import proyecciones_bp
from app.recomendaciones import recomendaciones_bp  # 👈 Nuevo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ingresos_bp)
app.register_blueprint(gastos_bp)
app.register_blueprint(presupuestos_bp)
app.register_blueprint(metas_bp)
app.register_blueprint(balance_bp)
app.register_blueprint(exportar_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(proyecciones_bp)
app.register_blueprint(recomendaciones_bp)  # ✅ Ya integrado

# Ruta raíz opcional
@app.route('/')
def index():
    return "Aplicación de Finanzas funcionando correctamente"

if __name__ == '__main__':
    app.run(debug=True)