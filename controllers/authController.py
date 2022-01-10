from werkzeug.security import check_password_hash
from App import db
from flask import render_template, session, request, redirect, url_for
from App import app
from wtforms import StringField, PasswordField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Required,Length
from models.models import User
from flask import flash
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html', msg='')

@app.route('/admin_profile', methods=['POST','GET'])
def admin_profile():
    return render_template('adminProfile.html', msg='')


@app.route('/login',methods=['POST', 'GET'])
def login():
    class LoginForm(FlaskForm):
        username = StringField(u'', validators=[Length(max=10),Required()])
        password = PasswordField(u'', validators=[Required()])
        submit = SubmitField('Entrar')
    def login_user(User):
        session["id"]=User.user_ci
        session["username"]=User.user_name
        session["type"]=User.user_type
    form = LoginForm()

    if request.method=='POST':
        user_ci=request.form['login_ci']
        user=User.query.filter_by(user_ci=user_ci).first()
        if user and check_password_hash(str(user.password_hash),form.password.data):
            login_user(user)
            return redirect(url_for('admin_profile'))
        else:
            flash('Usuario o Contraseña Incorrecto')
    return render_template('login.html', form=form)

@app.route('/change_password',methods=['POST', 'GET'])
def change_password():
    if request.method=='POST':
        previous=request.form['previous']
        new=request.form['new']
        user=User.query.filter_by(user_ci=session["id"]).first()
        if user and check_password_hash(str(user.password_hash),previous):
            db.session.query(User).filter(User.user_ci==session["id"]).update(dict(password_hash=generate_password_hash(new, method='sha256')))
            db.session.commit()
            flash('Contraseña cambiada con exito')
        else:
            flash('Contraseña antigua es incorrecta')
    return render_template('changePassword.html')


@app.route('/logout')
def logout():
    def logout_user():
        session.pop("id",None)
        session.pop("username",None)
        session.pop("admin",None)
    logout_user()
    return redirect(url_for('index'))