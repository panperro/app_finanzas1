from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Presupuesto

presupuestos_bp = Blueprint('presupuestos', __name__, url_prefix='/presupuestos')

@presupuestos_bp.route('/', methods=['GET', 'POST'])
@login_required
def presupuestos():
    if request.method == 'POST':
        monto = request.form['monto']
        categoria = request.form['categoria']
        inicio = request.form['inicio']
        fin = request.form['fin']
        nuevo = Presupuesto(
            monto=monto,
            categoria=categoria,
            fecha_inicio=inicio,
            fecha_fin=fin,
            usuario_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('presupuestos.presupuestos'))
    lista = Presupuesto.query.filter_by(usuario_id=current_user.id).all()
    return render_template('presupuestos.html', presupuestos=lista)