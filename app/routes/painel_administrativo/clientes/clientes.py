from flask import Blueprint, render_template, redirect, request, flash
from app.models.errors import HTTPResponse
from app.providers.functions import alternative_id_generator, post_request, get_request, delete_request
from app.models.basemodels import Error_Logs_, Person_, Person_PF_Data_, Person_PF_Complete_, Person_PJ_Complete_, Person_PJ_Data_
from datetime import datetime
from json import loads

clientes_bp = Blueprint(
    'clientes',
    __name__,
    url_prefix='/clientes',
    template_folder='templates',
    static_folder='/app/static'
)

@clientes_bp.route('/')
def clientes():
    return redirect('/painel-administrativo/clientes/lista-de-clientes')

@clientes_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    try:
        if request.method == 'POST':
            if request.form.get('cpf'):
                complemento = (request.form.get('complemento')).lower() if request.form.get('complemento') else None
                birth = datetime.strptime(request.form.get('nascimento'), '%d/%m/%Y').date()
                send = Person_PF_Complete_(
                    new_person= Person_(
                        alternative_id=alternative_id_generator(),
                        name=(request.form.get('nome')).lower(),
                        email=(request.form.get('email')),
                        doctype=1,
                        persontype=[4],
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
                    flash('Cadastro efetuado com sucesso!')
                else:
                    flash('Algo deu errado. Confira os dados e tente novamente.')

            elif request.form.get('cnpj'):
                ie = request.form.get('ie') if request.form.get('ie') else None
                complemento = (request.form.get('complemento2')).lower() if request.form.get('complemento2') else None
                send = Person_PJ_Complete_(
                    new_person=Person_(
                        alternative_id=alternative_id_generator(),
                        name=(request.form.get('nome-fantasia')).lower(),
                        email=(request.form.get('email2')).lower(),
                        doctype=2,
                        persontype=[4],
                        is_active=True
                    ),
                    new_person_data=Person_PJ_Data_(
                        cnpj=request.form.get('cnpj'),
                        cp_name=(request.form.get('razao-social')).lower(),
                        ie=ie,
                        tel=request.form.get('telefone2'),
                        cep=request.form.get('cep2'),
                        public_place=(request.form.get('logradouro2')).lower(),
                        place_number=request.form.get('numero2'),
                        complement=complemento,
                        district=(request.form.get('bairro2')).lower(),
                        city=(request.form.get('cidade2')).lower(),
                        uf=(request.form.get('uf2')).lower(),
                    )
                )
                response = post_request('/persons-service/add-person-pj', send.json())
                if response.status_code == 200:
                    flash('Cadastro efetuado com sucesso!')
                else:
                    flash('Algo deu errado. Confira os dados e tente novamente.')
            else:
                flash('Dados inválidos.')
            return redirect('/painel-administrativo/clientes/cadastrar')
        else:
            return render_template('/cadastrar-clientes.html')
    except Exception as error:
        try:
            send = Error_Logs_(
                log=str(error),
                log_datetime=datetime.now(),
                user_id=0, # Corrigir user_id quando current user estiver ativo
                service_id=2,
                endpoint='cadastrar clientes'
            )
            response = post_request('/error-logs-service/add-error-log', send.json())
            flash('Algo deu errado')
            return redirect('/painel-administrativo/clientes/cadastrar')
        except:
            flash('Algo deu errado')
            return redirect('/painel-administrativo/clientes/cadastrar')

@clientes_bp.route('/lista-de-clientes', methods=['GET', 'POST'])
def lista_de_clientes():
    try:
        if request.method == 'POST':
            if request.form.get('type') == 'alterar':
                if int(request.form.get('doctype')) == 1:
                    birth = datetime.strptime(request.form.get('nascimento'), '%d/%m/%Y').date()
                    person = Person_(
                        id=int(request.form.get('id')),
                        name=request.form.get('nome'),
                        email=request.form.get('email')
                    )
                    person_pf_data = Person_PF_Data_(
                        cpf=request.form.get('cpf'),
                        gender=request.form.get('sexo'),
                        cep=request.form.get('cep'),
                        public_place=request.form.get('logradouro'),
                        place_number=request.form.get('numero'),
                        complement=request.form.get('complemento'),
                        district=request.form.get('bairro'),
                        city=request.form.get('cidade'),
                        uf=request.form.get('uf'),
                        tel=request.form.get('telefone'),
                        birth=birth
                    )
                    send = Person_PF_Complete_(
                        new_person=person,
                        new_person_data=person_pf_data
                    )
                    response = post_request('/persons-service/update-person-pf', send.json())
                    if response.status_code == 200:
                        flash('Cadastro alterado com sucesso.')
                    elif response.status_code == 400:
                        flash('Erro na requisição. Verifique os dados e tente novamente.')
                    else:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                elif int(request.form.get('doctype')) == 2:
                    person = Person_(
                        id=int(request.form.get('id')),
                        name=request.form.get('nome-fantasia'),
                        email=request.form.get('email')
                    )
                    person_pj_data = Person_PJ_Data_(
                        cnpj=request.form.get('cnpj'),
                        cp_name=request.form.get('razao-social'),
                        ie=request.form.get('ie'),
                        tel=request.form.get('telefone'),
                        cep=request.form.get('cep'),
                        public_place=request.form.get('logradouro'),
                        place_number=request.form.get('numero'),
                        complement=request.form.get('complemento'),
                        district=request.form.get('bairro'),
                        city=request.form.get('cidade'),
                        uf=request.form.get('uf')
                    )
                    send = Person_PJ_Complete_(
                        new_person=person,
                        new_person_data=person_pj_data
                    )
                    response = post_request('/persons-service/update-person-pj', send.json())
                    if response.status_code == 200:
                        flash('Alteração efetuada com sucesso.')
                    elif response.status_code == 400:
                        flash('Erro na requisição. Verifique os dados e tente novamente.')
                    else:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                else:
                    flash('Erro no servidor. Estamos trabalhando para corrigir.')
                return redirect('/painel-administrativo/clientes/lista-de-clientes')
            elif request.form.get('type') == 'bloquear':
                id = int(request.form.get('id'))
                if int(request.form.get('doctype')) == 1:
                    send = Person_PF_Complete_(
                        new_person=Person_(
                            id=id,
                            is_active=False
                        ),
                        new_person_data=Person_PF_Data_(
                            uf=None
                        )
                    )
                    response = post_request('/persons-service/update-person-pf', send.json())
                    if response.status_code == 200:
                        flash('Usuário bloqueado.')
                    elif response.status_code == 400:
                        flash('Erro na requisição. Verifique os dados e tente novamente.')
                    else:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                elif int(request.form.get('doctype')) == 2:
                    send = Person_PJ_Complete_(
                        new_person=Person_(
                            id=id,
                            is_active=False
                        ),
                        new_person_data=Person_PJ_Data_(
                            uf=None
                        )
                    )
                    response = post_request('/persons-service/update-person-pj', send.json())
                    if response.status_code == 200:
                        flash('Cliente bloqueado.')
                    elif response.status_code == 400:
                        flash('Erro na requisição. Verifique os dados e tente novamente.')
                    else:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                else:
                    flash('Erro no servidor. Estamos trabalhando para corrigir.')
                return redirect('/painel-administrativo/clientes/lista-de-clientes')
            elif request.form.get('type') == 'desbloquear':
                id = int(request.form.get('id'))
                if int(request.form.get('doctype')) == 1:
                    send = Person_PF_Complete_(
                        new_person=Person_(
                            id=id,
                            is_active=True
                        ),
                        new_person_data=Person_PF_Data_(
                            uf=None
                        )
                    )
                    response = post_request('/persons-service/update-person-pf', send.json())
                    if response.status_code == 200:
                        flash('Cliente desbloqueado.')
                    elif response.status_code == 400:
                        flash('Algo deu errado. Estamos trabalhando para corrigir.')
                    else:
                        flash('Algo deu errado. Estamos trabalhando para corrigir.')
                elif int(request.form.get('doctype')) == 2:
                    send = Person_PJ_Complete_(
                        new_person=Person_(
                            id=id,
                            is_active=True
                        ),
                        new_person_data=Person_PJ_Data_(
                            uf=None
                        )
                    )
                    response = post_request('/persons-service/update-person-pj', send.json())
                    if response.status_code == 200:
                        flash('Cliente desbloqueado.')
                    elif response.status_code == 400:
                        flash('Algo deu errado. Estamos trabalhando para corrigir.')
                    else:
                        flash('Algo deu errado. Estamos trabalhando para corrigir.')
                else:
                    flash('Erro no servidor. Estamos trabalhando para corrigir.')
                return redirect('/painel-administrativo/clientes/lista-de-clientes')
            elif request.form.get('type') == 'excluir':
                doctype = int(request.form.get('doctype'))
                id = int(request.form.get('id'))
                response = delete_request(f'/persons-service/delete-person?doctype={doctype}&person_id={id}')
                if response.status_code == 200:
                    flash('Cliente excluído.')
                elif response.status_code == 400:
                    flash('Algo deu errado. Estamos trabalhando para corrigir.')
                else:
                    flash('Algo deu errado. Estamos trabalhando para corrigir.')
            return redirect('/painel-administrativo/clientes/lista-de-clientes')
        else:
            if request.args.get('filter'):
                filter = request.args.get('filter')
                arg = f'%{request.args.get("arg")}%'
                match filter:
                    case 'nome':
                        response = get_request(f'/persons-service/get-simple-person?type_data=name&name={arg}')
                if response.status_code == 200:
                    if filter == 'nome':
                        client_list = []
                        person_list = loads(response.text)
                        for item in person_list:
                            if 4 in item['persontype']:
                                data = Person_(**item)
                                client_list.append(data)
                        clientes = sorted(client_list, key=lambda row:(row.name).lower())
                        flash(f'Exibindo resultado para nomes que contenham "{request.args.get("arg")}"')
                    return render_template('/lista-de-clientes.html', clientes=clientes)
                elif response.status_code == 400:
                    raise HTTPResponse(status_code=400, detail='Erro a requisição. Verifique os dados.')
                else:
                    raise HTTPResponse(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')
                    
            response = get_request('/persons-service/get-simple-person?type_data=all')
            if response.status_code == 200:
                client_list = []
                person_list = loads(response.text)
                for person in person_list:
                    if 4 in person['persontype']:
                        data = Person_(**person)
                        client_list.append(data)
                clientes = sorted(client_list, key=lambda row:(row.name).lower())
                flash('Exibindo resultado de todos os clientes')
            else:
                flash('Algo deu errado. Tente novamente.')
            return render_template('/lista-de-clientes.html', clientes=clientes)
    except Exception as error:
        return render_template('/lista-de-clientes.html')

# Endpoint para Ajax
@clientes_bp.route('/get-person')
def get_person():
    doctype = request.args.get('filter')
    arg = request.args.get('arg')
    if doctype == 'pf':
        response = get_request(f'/persons-service/get-pf-data?type_data=person_id&person_id={arg}')
        person_data = loads(response.text)
        if len(person_data) == 0:
            person = Person_PF_Complete_(
                new_person=Person_(
                    name='Cadastro com dados corrompidos.'
                ),
                new_person_data=Person_PF_Data_()
            )
        else:
            person = Person_PF_Complete_(
                new_person=Person_(**(person_data[0])['person']),
                new_person_data=Person_PF_Data_(**((person_data[0])['person_pf_data']))
            )
            bday = (person.new_person_data.birth).strftime('%d/%m/%Y')
            person.new_person_data.birth = bday
    elif doctype == 'pj':
        response = get_request(f'/persons-service/get-pj-data?type_data=person_id&person_id={arg}')
        person_data = loads(response.text)
        if len(person_data) == 0:
            person = Person_PJ_Complete_(
                new_person=Person_(
                    name='Cadastro com dados corrompidos.'
                ),
                new_person_data=Person_PJ_Data_()
            )
        else:
            person = Person_PJ_Complete_(
                new_person=Person_(**(person_data[0])['person']),
                new_person_data=Person_PJ_Data_(**((person_data[0])['person_pj_data']))
            )
    
    return person.json()