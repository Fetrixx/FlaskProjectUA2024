from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Profile, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(['Sesion iniciada correctamente!'], category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(['Contraseña incorrecta, intente otra vez.'], category='error')
        else:
            flash(['El correo no existe.'], category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        username = request.form.get('username')
        
        # Verificar si el correo ya está registrado
        user_by_email = User.query.filter_by(email=email).first()
        
        # Verificar si el nombre de usuario ya está registrado
        user_by_username = User.query.filter_by(username=username).first()
        
        errors = []
        if user_by_email:
            errors.append('Error: Este correo ya esta registrado.')
        if user_by_username:
            errors.append('Error: Este usuario ya esta registrado.')
        if len(username) < 4:
            errors.append('Error: El nombre de usuario debe ser mayor a 3 caracteres.')
        if len(email) < 4:
            errors.append('Error: El correo debe ser mayor a 3 caracteres.')
        if len(first_name) < 2:
            errors.append('Error: El Nombre debe ser mayor a 1 caracter.')
        if password1 != password2:
            errors.append('Error: Las contraseñas no coinciden.')
        if len(password1) < 7:
            errors.append('Error: La contraseña debe ser de al menos 7 caracteres.')
        
        if len(errors) > 0:
            flash(errors, category='danger')    
        else:
            new_user = User(email=email, first_name=first_name, username=username, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            #new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            #    password1, method='sha256')) # the method "sha256" is deprecated, use pbkdf2:sha256
            db.session.add(new_user)
            db.session.commit()
                
            # Crear un perfil asociado
            new_profile = Profile(user_id=new_user.id)
            
            login_user(new_user, remember=True)
            msg = ['Cuenta creada correctamente!']
            flash(msg, category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
