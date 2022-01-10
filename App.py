from flask import Flask, session
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from Configs import app_config
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(app_config)
bootstrap = Bootstrap(app)
login_manager=LoginManager()

Session(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:admin@localhost/proyecto'

db=SQLAlchemy(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

from controllers.addController import*
from controllers.authController import*
from controllers.infoController import*
from controllers.updateController import*
if __name__=='__main__':
    app.run(debug=True, host= '192.168.1.12',port=3000)
    app.secret_key = '684651454165416'
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)

