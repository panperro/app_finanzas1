from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
from .models import Ingreso, Gasto

proyecciones_bp = Blueprint('proyecciones', __name__, url_prefix='/proyecciones')

@proyecciones_bp.route('/')
@login_required
def proyecciones():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()

    if not ingresos and not gastos:
        return render_template('proyecciones.html', mensaje="No hay suficientes datos para proyecciones.")

    # Procesar datos
    df_ingresos = pd.DataFrame([{'fecha': i.fecha, 'monto': i.monto} for i in ingresos])
    df_gastos = pd.DataFrame([{'fecha': g.fecha, 'monto': g.monto} for g in gastos])

    # Agrupar por mes
    df_ingresos['fecha'] = pd.to_datetime(df_ingresos['fecha'])
    df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])

    ingresos_mensuales = df_ingresos.groupby(df_ingresos['fecha'].dt.to_period('M')).sum()
    gastos_mensuales = df_gastos.groupby(df_gastos['fecha'].dt.to_period('M')).sum()

    # Promedio mensual
    prom_ingresos = ingresos_mensuales['monto'].mean() if not ingresos_mensuales.empty else 0
    prom_gastos = gastos_mensuales['monto'].mean() if not gastos_mensuales.empty else 0

    # Proyección de próximos 6 meses
    meses = pd.date_range(datetime.today(), periods=6, freq='MS')
    balance_esperado = [prom_ingresos - prom_gastos] * 6

    # Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses, y=balance_esperado, mode='lines+markers', name='Balance Estimado'))

    fig.update_layout(
        title='Proyección de Balance (6 meses)',
        xaxis_title='Mes',
        yaxis_title='Balance ($)',
        template='plotly_white'
    )

    grafica = fig.to_html(full_html=False)

    return render_template('proyecciones.html', grafica=grafica)