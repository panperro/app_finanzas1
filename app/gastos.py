from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Gasto, Categoria

gastos_bp = Blueprint('gastos', __name__, url_prefix='/gastos')

@gastos_bp.route('/', methods=['GET', 'POST'])
@login_required
def gastos():
    categorias = Categoria.query.filter_by(usuario_id=current_user.id, tipo='gasto').all()

    if request.method == 'POST':
        monto = request.form['monto']
        categoria = request.form['categoria']
        nuevo_gasto = Gasto(monto=monto, categoria=categoria, usuario_id=current_user.id)
        db.session.add(nuevo_gasto)
        db.session.commit()
        return redirect(url_for('gastos.gastos'))

    lista = Gasto.query.filter_by(usuario_id=current_user.id).all()
    return render_template('gastos.html', gastos=lista, categorias=categorias)