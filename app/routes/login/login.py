from flask import Blueprint, render_template

login_bp = Blueprint(
    'login',
    __name__,
    url_prefix='/login',
    template_folder='templates',
    static_folder='static'
)

@login_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    return render_template('entrar.html')