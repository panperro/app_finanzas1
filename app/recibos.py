from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

recibos_bp = Blueprint('recibos', __name__, url_prefix='/recibos')

@recibos_bp.route('/', methods=['GET', 'POST'])
@login_required
def recibos():
    carpeta = 'static/recibos'
    os.makedirs(carpeta, exist_ok=True)

    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if archivo and archivo.filename != '':
            nombre = secure_filename(archivo.filename)
            ruta = os.path.join(carpeta, f'{current_user.username}_{nombre}')
            archivo.save(ruta)
            flash('Recibo subido correctamente')
        else:
            flash('No se seleccionó ningún archivo')
        return redirect(url_for('recibos.recibos'))

    lista = []
    for archivo in os.listdir(carpeta):
        if archivo.startswith(current_user.username + '_'):
            lista.append(archivo)

    return render_template('recibos.html', recibos=lista)