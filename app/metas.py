from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, MetaAhorro

metas_bp = Blueprint('metas', __name__, url_prefix='/metas')

@metas_bp.route('/', methods=['GET', 'POST'])
@login_required
def metas():
    if request.method == 'POST':
        objetivo = request.form['objetivo']
        monto_objetivo = request.form['monto_objetivo']
        nueva = MetaAhorro(
            objetivo=objetivo,
            monto_objetivo=monto_objetivo,
            usuario_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('metas.metas'))
    lista = MetaAhorro.query.filter_by(usuario_id=current_user.id).all()
    return render_template('metas.html', metas=lista)