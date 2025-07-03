from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Ingreso, Gasto, Presupuesto
from collections import defaultdict
from datetime import datetime

recomendaciones_bp = Blueprint('recomendaciones', __name__, url_prefix='/recomendaciones')

@recomendaciones_bp.route('/')
@login_required
def recomendaciones():
    recomendaciones = []

    # Obtener ingresos y gastos
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()
    presupuestos = Presupuesto.query.filter_by(usuario_id=current_user.id).all()

    total_ingresos = sum(i.monto for i in ingresos)
    total_gastos = sum(g.monto for g in gastos)

    # Consejo general
    if total_gastos > total_ingresos:
        recomendaciones.append("Tus gastos totales superan tus ingresos. Considera reducir algunos gastos.")
    else:
        recomendaciones.append("Buen trabajo: tus ingresos superan tus gastos.")

    # Gastos por categoría
    gastos_cat = defaultdict(float)
    for g in gastos:
        gastos_cat[g.categoria] += g.monto

    for cat, monto in gastos_cat.items():
        if monto > (0.3 * total_gastos):  # Si una categoría ocupa más del 30% de los gastos
            recomendaciones.append(f"Estás gastando mucho en '{cat}'. Revisa si puedes reducir ese gasto.")

    # Comparación con presupuestos
    for p in presupuestos:
        cat_total = sum(g.monto for g in gastos if g.categoria == p.categoria and p.fecha_inicio <= g.fecha <= p.fecha_fin)
        if cat_total > p.monto:
            recomendaciones.append(f"Has superado el presupuesto en la categoría '{p.categoria}'.")

    if not recomendaciones:
        recomendaciones.append("¡Todo se ve bien! Sigue así.")

    return render_template('recomendaciones.html', recomendaciones=recomendaciones)