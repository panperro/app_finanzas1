from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Ingreso, Categoria

ingresos_bp = Blueprint('ingresos', __name__, url_prefix='/ingresos')

@ingresos_bp.route('/', methods=['GET', 'POST'])
@login_required
def ingresos():
    categorias = Categoria.query.filter_by(usuario_id=current_user.id, tipo='ingreso').all()

    if request.method == 'POST':
        monto = request.form['monto']
        categoria = request.form['categoria']
        nuevo_ingreso = Ingreso(monto=monto, categoria=categoria, usuario_id=current_user.id)
        db.session.add(nuevo_ingreso)
        db.session.commit()
        return redirect(url_for('ingresos.ingresos'))

    lista = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    return render_template('ingresos.html', ingresos=lista, categorias=categorias)