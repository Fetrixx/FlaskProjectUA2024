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
                flash('Sesion iniciada correctamente!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta, intente otra vez.', category='error')
        else:
            flash('El correo no existe.', category='error')

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
        
        
        flashMsg = ''
        if user_by_email:
            flashMsg += 'Error: Este correo ya esta registrado.\n'
            print(flashMsg)
        elif user_by_username:
            flashMsg += 'Error: Este usuario ya esta registrado.\n'
            print(flashMsg)
        elif len(username) < 4:
            # flash('Este correo ya esta registrado.', category='error')
            flashMsg += 'Error: El nombre de usuario debe ser mayor a 3 caracteres.\n'
            print(flashMsg)
        elif len(email) < 4:
            flashMsg += 'Error: El correo debe ser mayor a 3 caracteres.\n'
            print(flashMsg)
        elif len(first_name) < 2:
            flashMsg += 'Error: El Nombre debe ser mayor a 1 caracter.\n'
            print(flashMsg)
        elif password1 != password2:
            flashMsg += 'Error: Las contraseñas no coinciden.\n'
            print(flashMsg)
        elif len(password1) < 7:
            flashMsg += 'Error: La contraseña debe ser de al menos 7 caracteres.\n'
            print(flashMsg)
        
        if user_by_email:
            # flash('Este correo ya esta registrado.', category='error')
            flash(flashMsg, category='error')
        elif user_by_username:
            # flashMsg += 'Error: Este usuario ya esta registrado.\n'
            flash(flashMsg, category='error')
        elif len(username) < 4:
            # flash('Este correo ya esta registrado.', category='error')
            flash(flashMsg, category='error')
        elif len(email) < 4:
            # flash('El correo debe ser mayor a 3 caracteres.', category='error')
            flash(flashMsg, category='error')
        elif len(first_name) < 2:
            # flash('El Nombre debe ser mayor a 1 caracter.', category='error')
            flash(flashMsg, category='error')
        elif password1 != password2:
            # flash('Las contraseñas no coinciden.', category='error')
            flash(flashMsg, category='error')
        elif len(password1) < 7:
            # flash('La contraseña debe ser de al menos 7 caracteres.', category='error')
            flash(flashMsg, category='error')
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
            flash('Cuenta creada correctamente!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
