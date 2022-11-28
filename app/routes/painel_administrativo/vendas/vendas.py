from flask import Blueprint, render_template, redirect

vendas_bp = Blueprint(
    'vendas',
    __name__,
    url_prefix='/vendas',
    template_folder='templates',
    static_folder='/app/static'
)

@vendas_bp.route('/')
def vendas():
    return redirect('/painel-administrativo/vendas/nova-venda')

@vendas_bp.route('/nova-venda')
def nova_venda():
    return render_template('/nova-venda.html')

@vendas_bp.route('/em-aberto')
def em_aberto():
    return render_template('/em-aberto.html')

@vendas_bp.route('/concluidas')
def concluidas():
    return render_template('/concluidas.html')