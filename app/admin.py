from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Usuario, Ingreso, Gasto, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def panel_admin():
    if current_user.rol != 'admin':
        return redirect(url_for('balance.balance'))

    usuarios = Usuario.query.all()
    ingresos = Ingreso.query.all()
    gastos = Gasto.query.all()

    return render_template('panel_admin.html', usuarios=usuarios, ingresos=ingresos, gastos=gastos)