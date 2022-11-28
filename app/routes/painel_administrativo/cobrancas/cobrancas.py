from flask import Blueprint, render_template, redirect

cobrancas_bp = Blueprint(
    'cobranças',
    __name__,
    url_prefix='/cobrancas',
    template_folder='templates',
    static_folder='/app/static'
)

@cobrancas_bp.route('/')
def cobrancas():
    return redirect('/painel-administrativo/cobrancas/boletos-em-atraso')

@cobrancas_bp.route('/boletos-em-atraso')
def boletos_em_atraso():
    return render_template('/boletos-em-atraso.html')