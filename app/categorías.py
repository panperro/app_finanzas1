from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/', methods=['GET', 'POST'])
@login_required
def categorias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']  # ingreso o gasto
        nueva = Categoria(nombre=nombre, tipo=tipo, usuario_id=current_user.id)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('categorias.categorias'))

    lista = Categoria.query.filter_by(usuario_id=current_user.id).all()
    return render_template('categorias.html', categorias=lista)