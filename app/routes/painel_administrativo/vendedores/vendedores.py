from json import dumps, loads
from flask import Blueprint, flash, render_template, redirect, request
from ....providers.functions import get_request, post_request, new_alternative_id
from ....models.basemodels import Person_PF_Complete_, Person_, Person_PF_Data_
from datetime import datetime, date


vendedores_bp = Blueprint(
    'vendedores',
    __name__,
    url_prefix='/vendedores',
    template_folder='templates',
    static_folder='/app/static'
)

@vendedores_bp.route('/')
def vendedores():
    return redirect('/painel-administrativo/vendedores/lista-de-vendedores')

@vendedores_bp.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar_vendedores():
    try:
        if request.method == 'POST':
            complemento = (request.form.get('complemento')).lower() if request.form.get('complemento') else None
            birth = datetime.strptime(request.form.get('nascimento'), '%d/%m/%Y').date()
            send = Person_PF_Complete_(
                new_person= Person_(
                    alternative_id=new_alternative_id(),
                    name=(request.form.get('nome')).lower(),
                    email=(request.form.get('email')),
                    doctype=1,
                    persontype=[3],
                    is_active=True
                ), new_person_data= Person_PF_Data_(
                    cpf=request.form.get('cpf'),
                    gender=(request.form.get('sexo')).lower(),
                    cep=request.form.get('cep'),
                    public_place=(request.form.get('logradouro')).lower(),
                    place_number=request.form.get('numero'),
                    complement=complemento,
                    district=(request.form.get('bairro')).lower(),
                    city=(request.form.get('cidade')).lower(),
                    uf=(request.form.get('uf')).lower(),
                    tel=request.form.get('telefone'),
                    birth=birth
                )
            )
            response = post_request('/persons-service/add-person-pf', send.json())
            if response.status_code == 200:
                flash('Vendedor adicionado.')
            elif response.status_code == 400:
                flash('Erro na requisição. Verifique os dados.')
            else:
                flash('Erro no servidor. Estamos trabalhando para corrigir.')
            return redirect('/painel-administrativo/vendedores/cadastrar')
        else:
            # Transformar cadastro existente em vendedor
            if request.args.get('setPersonToSeller'):
                set_id = int(request.args.get('setPersonToSeller'))
                persontype = request.args.get('persontype')

                # transformando parâmetro recebido em lista
                persontype_list = loads(f'[{persontype}]') 
                if 3 in persontype_list:
                    flash('Essa pessoa já é um vendedor.')
                else:
                    persontype_list.append(3)
                    send = Person_PF_Complete_(
                        new_person=Person_(
                            id=set_id,
                            persontype=persontype_list
                        ),
                        new_person_data=Person_PF_Data_()
                    )
                    response = post_request('/persons-service/update-person-pf', send.json())
                    if response.status_code == 200:
                        flash('Vendedor adicionado com sucesso.')
                    else:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                return redirect('/painel-administrativo/vendedores/cadastrar', code=303)
            return render_template('/cadastrar-vendedores.html')
    except ValueError as error:
        flash('Dados inválidos.')
        return redirect('/painel-administrativo/vendedores/cadastrar', code=303)
    except:
        flash('Erro no servidor. Estamos trabalhando para corrigir')
        return redirect('/painel-administrativo/vendedores/cadastrar', code=303)

@vendedores_bp.route('/lista-de-vendedores', methods=['GET', 'POST'])
def lista_de_vendedores():
    #try:
    if request.method == 200:
        pass
    else:
        response = get_request('/persons-service/get-simple-person?type_data=all_sellers')
        if response.status_code == 200:
            seller_list = []
            person_list = loads(response.text)
            for person in person_list:
                data = Person_(**person)
                seller_list.append(data)
            vendedores = sorted(seller_list, key=lambda row:(row.name).lower())
            flash('Exibindo resultado de todos os vendedores')
        else:
            vendedores = []
            flash('Erro no servidor. Estamos trabalhando para corrigir.')
        return render_template('/lista-de-vendedores.html', vendedores=vendedores)
    '''except:
        flash('Erro no servidor. Estamos trabalhando para corrigir.')
        return redirect('/painel-administrativo')'''

@vendedores_bp.route('/comissoes')
def comissoes():
    return render_template('/comissoes.html')

# Checar se já existe CPF cadastrado, retorna False ou True
@vendedores_bp.route('/cpf-exists')
def cpf_exists():
    cpf = request.args.get('cpf')
    response = get_request(f'/persons-service/get-pf-data?type_data=cpf&cpf={cpf}')
    if response.status_code == 200:
        check = loads(response.text)
        if len(check) > 0:
            for item in check:
                item['person'].pop('hash')
        return dumps(check)
    elif response.status_code == 400:
        pass
    else:
        pass