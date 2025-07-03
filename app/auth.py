from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        contraseña = request.form['contraseña']
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.contraseña, contraseña):
            login_user(user)
            return redirect(url_for('balance.balance'))
        flash('Credenciales inválidas')
    return render_template('login.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        contraseña = request.form['contraseña']
        hashed = generate_password_hash(contraseña)
        nuevo = Usuario(username=username, contraseña=hashed)
        db.session.add(nuevo)
        db.session.commit()
        login_user(nuevo)
        return redirect(url_for('balance.balance'))
    return render_template('registro.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))