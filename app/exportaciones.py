from flask import Blueprint, send_file
from flask_login import login_required, current_user
from io import BytesIO
import pandas as pd
from .models import Ingreso, Gasto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

exportar_bp = Blueprint('exportar', __name__, url_prefix='/exportar')

@exportar_bp.route('/excel')
@login_required
def exportar_excel():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()

    df_ingresos = pd.DataFrame([{'Monto': i.monto, 'Categoría': i.categoria, 'Fecha': i.fecha} for i in ingresos])
    df_gastos = pd.DataFrame([{'Monto': g.monto, 'Categoría': g.categoria, 'Fecha': g.fecha} for g in gastos])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_ingresos.to_excel(writer, index=False, sheet_name='Ingresos')
        df_gastos.to_excel(writer, index=False, sheet_name='Gastos')
    output.seek(0)

    return send_file(output, download_name='balance.xlsx', as_attachment=True)

@exportar_bp.route('/pdf')
@login_required
def exportar_pdf():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    gastos = Gasto.query.filter_by(usuario_id=current_user.id).all()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Balance Financiero")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, "Ingresos:")
    y -= 20
    for i in ingresos:
        p.drawString(60, y, f"{i.fecha} - {i.categoria}: ${i.monto}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 40

    y -= 20
    p.setFont("Helvetica", 12)
    p.drawString(50, y, "Gastos:")
    y -= 20
    for g in gastos:
        p.drawString(60, y, f"{g.fecha} - {g.categoria}: ${g.monto}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 40

    p.save()
    buffer.seek(0)
    return send_file(buffer, download_name='balance.pdf', as_attachment=True)