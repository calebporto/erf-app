from flask import Blueprint, render_template
from .vendas.vendas import vendas_bp
from .clientes.clientes import clientes_bp
from .produtos.produtos import produtos_bp
from .vendedores.vendedores import vendedores_bp
from .cobrancas.cobrancas import cobrancas_bp

painel_adm_bp = Blueprint(
    'painel-administrativo',
    __name__,
    url_prefix='/painel-administrativo',
    template_folder='templates',
    static_folder='static'
)

painel_adm_bp.register_blueprint(vendas_bp)
painel_adm_bp.register_blueprint(clientes_bp)
painel_adm_bp.register_blueprint(produtos_bp)
painel_adm_bp.register_blueprint(vendedores_bp)
painel_adm_bp.register_blueprint(cobrancas_bp)


@painel_adm_bp.route('/')
def painel_admnistrativo():
    return render_template('painel-administrativo.html')

@painel_adm_bp.route('/manual-do-usuario')
def manual_do_usuario():
    return render_template('/manual-do-usuario.html')