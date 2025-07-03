from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Ingreso, Gasto
import plotly.graph_objs as go
import plotly.offline as pyo

graficas_bp = Blueprint('graficas', __name__, url_prefix='/graficas')

@graficas_bp.route('/')
@login_required
def graficas():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()

    categorias_ing = {}
    for i in ingresos:
        categorias_ing[i.categoria] = categorias_ing.get(i.categoria, 0) + i.monto

    categorias_gas = {}
    for g in gastos:
        categorias_gas[g.categoria] = categorias_gas.get(g.categoria, 0) + g.monto

    fig_ingresos = go.Figure([go.Pie(labels=list(categorias_ing.keys()), values=list(categorias_ing.values()))])
    fig_gastos = go.Figure([go.Bar(x=list(categorias_gas.keys()), y=list(categorias_gas.values()))])

    graf_ingresos = pyo.plot(fig_ingresos, output_type='div')
    graf_gastos = pyo.plot(fig_gastos, output_type='div')

    return render_template('graficas.html', graf_ingresos=graf_ingresos, graf_gastos=graf_gastos)