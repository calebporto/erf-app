from flask import Flask
from app.config import *
from app.routes.login.login import login_bp
from app.routes.painel_administrativo.painel_administrativo import painel_adm_bp
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['USE_SESSION_FOR_NEXT'] = USE_SESSION_FOR_NEXT  # Excluindo a variável 'next' da string de recirecionamento do login_required
app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = REMEMBER_COOKIE_REFRESH_EACH_REQUEST

ITEMS_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app\static\media\produtos')  # Definindo pasta de destino dos uploads das imagens dos produtos

app.register_blueprint(login_bp)
app.register_blueprint(painel_adm_bp)