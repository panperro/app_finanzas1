from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Ingreso, Gasto

balance_bp = Blueprint('balance', __name__, url_prefix='/balance')

@balance_bp.route('/')
@login_required
def balance():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()
    total_ingresos = sum(i.monto for i in ingresos)
    total_gastos = sum(g.monto for g in gastos)
    balance = total_ingresos - total_gastos
    return render_template('balance.html', ingresos=total_ingresos, gastos=total_gastos, balance=balance)